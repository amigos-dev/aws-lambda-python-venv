# Copyright (c) 2022 Amigos Development Inc.
#
# MIT License - See LICENSE file accompanying this package.
#

"""Manipulation of a virtualenv that will be turned into a layer"""

from .logging import logger

from typing import Mapping, Optional, Type, Any, Dict, Tuple, Generator, IO, List, Union
from .internal_types import Jsonable, JsonableDict

import os
import json
import sys
import boto3
import botocore
import subprocess
import botocore.session
from boto3 import Session
from mypy_boto3_s3.client import S3Client, Exceptions as S3Exceptions
from mypy_boto3_s3.type_defs import ObjectTypeDef
from botocore.exceptions import ClientError
from urllib.parse import urlparse
import urllib.parse
import requests

from io import StringIO
from io import BytesIO

from .util import create_aws_session, full_type, normalize_jsonable_dict

class LayerVenv:
  venv_dir: str
  parent_env: Dict[str, str]
  venv_bin_dir: str
  venv_activate_script: str
  venv_python_cmd: str
  venv_pip_cmd: str
  venv_env: Dict[str, str]
  _pip_freeze_output: Optional[str] = None
  _frozen_packages: Optional[Dict[str, str]] = None
  python_version: str
  python_short_version: str
  site_packages_dir: str

  def __init__(self, venv_dir: str, parent_env: Optional[Mapping[str, str]]=None):
    self.venv_dir = os.path.abspath(venv_dir)
    if parent_env is None:
      parent_env = os.environ
    self.parent_env = dict(parent_env)
    self.venv_bin_dir = os.path.join(self.venv_dir, 'bin')
    self.venv_activate_script = os.path.join(self.venv_bin_dir, 'activate')
    self.venv_python_cmd = os.path.join(self.venv_bin_dir, 'python')
    self.venv_pip_cmd = os.path.join(self.venv_bin_dir, 'pip')
    # Activate the virtualenv in a subshell, and capture all the environment
    # variables so we can subsequently run subprocesses within the virtualenv.
    venv_env_bytes = subprocess.check_output(
        f". '{self.venv_activate_script}'; '{self.venv_python_cmd}' -c "
          f"'import json, os; print(json.dumps(dict(os.environ), indent=2))'",
        shell=True,
        env=self.parent_env)
    venv_env = json.loads(venv_env_bytes)
    if '_' in venv_env:
      del venv_env['_']
    self.venv_env = venv_env
    version_output = subprocess.check_output(
        [self.venv_python_cmd, '-V'],
        env=self.venv_env
      ).decode('utf-8').strip()
    self.python_version = version_output.split()[-1]
    self.python_short_version = '.'.join(self.python_version.split('.')[:2])
    self.site_packages_dir = os.path.join(self.venv_dir, 'lib', f'python{self.python_short_version}', 'site-packages')

  def get_package_import_name(self, package_name: str) -> str:
    return package_name.replace('-', '_')

  def get_package_dir(self, package_name: str) -> str:
    return os.path.join(self.site_packages_dir, self.get_package_import_name(package_name))

  def ensure_pip(self) -> None:
    if not os.path.exists(self.venv_pip_cmd):
      subprocess.check_call([self.venv_python_cmd, '-m', 'ensurepip'], env=self.venv_env)

  def get_freeze_output(self) -> str:
    if self._pip_freeze_output is None:
      self.ensure_pip()
      self._pip_freeze_output = subprocess.check_output(
          [self.venv_pip_cmd, 'freeze'], env=self.venv_env
        ).decode('utf-8')
    return self._pip_freeze_output

  def freeze(self) -> Dict[str, str]:
    if self._frozen_packages is None:
      result: Dict[str, str] = {}
      freeze_output = self.get_freeze_output()
      for line in freeze_output.split('\n'):
        line = line.strip()
        if line != '' and not line.startswith('#'):
          v: str
          k: str
          if line.startswith('-e '):
            v, k = line.rsplit('=', 1)
          elif ' @ ' in line:
            k, v = line.split(' @ ', 1)
            v = '@ ' + v
          else:
            k, v = line.split('==', 1)
          result[k] = v
      self._frozen_packages = result
    return self._frozen_packages

  def get_frozen_package_dirs(self) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for package_name, package_version in self.freeze().items():
      package_dir = self.get_package_dir(package_name)
      result[package_name] = package_dir
    return result

