#!/usr/bin/env python3
#
# Copyright (c) 2022 Amigos Development, Inc.
#
# MIT License - See LICENSE file accompanying this package.
#

"""Command-line interface for this package"""

# This module is run as a script or with "python3 -m"; all imports must be absolute

import sys
from lambda_venv.cli import run

# allow running with "python3 -m", or as a standalone script
if __name__ == "__main__":
  sys.exit(run())
