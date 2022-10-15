# Copyright (c) 2022 Amigos Development Inc.
#
# MIT License - See LICENSE file accompanying this package.
#

"""Manipulation of a local layer directory derived from an existing virtualenv"""

from .logging import logger

from typing import Optional, Type, Any, Dict, Tuple, Generator, IO, List, Union
from .internal_types import Jsonable, JsonableDict

import os
import sys
import boto3
import botocore
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

class LayerDir:
  dir_path: str
  