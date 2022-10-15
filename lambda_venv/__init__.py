# Copyright (c) 2022 Amigos Development Inc.
#
# MIT License - See LICENSE file accompanying this package.
#

"""A package for creating virtualenv layers for AWS lambda python handlers"""

from .version import __version__
from .constants import *
from .exceptions import *
from .util import (
    create_aws_session,
    get_aws_caller_identity,
    get_aws_account,
    full_name_of_type,
    full_type,
  )
