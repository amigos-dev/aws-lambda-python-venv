lambda-venv: Easy creation of virtualenv layers for [AWS Lambda](https://docs.aws.amazon.com/lambda/index.html)
==============================================================

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Latest release](https://img.shields.io/github/v/release/amigos-dev/aws-step-activity.svg?style=flat-square&color=b44e88)](https://github.com/amigos-dev/lambda-venv/releases)

A commandline tool and API for turning virtualenv directories into
[AWS Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html#gettingstarted-package-layers)
for Python handlers.

Table of contents
-----------------

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
  * [Command line](#command-line)
  * [API](api)
* [Known issues and limitations](#known-issues-and-limitations)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Authors and history](#authors-and-history)


Introduction
------------

Python package `lambda-venv` provides a command-line tool as well as a runtime API for managing and deploying
AWS lambda layers from python virtualenv's.

Some key features of lambda-venv:

* Turns any standard virtualenv into a zippable directory artifact suitable for turning into an
  [AWS Lambda Layer](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html#gettingstarted-package-layers)
* Redundant packages implicitly available to Python AWS Lambda Functions, as well as
  packages unnecessary at runtime (e.g., "pip") are excluded from the layers
* Allows explicit exclusion/inclusion of Python packages
* Provides a repeatable hash of the artifact. This allows the user to decide when a deployed layer
  is stale and needs to be redeployed
* If separate layers are not desired, the zippable directory artifact can be merged directly
  into an AWS Lambda Function package
* Provides helpers for creating ZIP files, uploading to S3 on hash change, and deploying
  to AWS Lambda Layers and FUnctions


Installation
------------

### Prerequisites

**Python**: Python 3.7+ is required. See your OS documentation for instructions.

**AWS Client**: boto3 is used for AWS access. A proper AWS profile with credentials must be configured. If the profile is not _default_, it can be selected with environment variable AWS_PROFILE or provided to the API or on the command line. The AWS CLI tool is not required, but it is recommended.

### From GitHub

[Poetry](https://python-poetry.org/docs/master/#installing-with-the-official-installer) is required; it can be installed with:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Clone the repository and install lambda-venv into a private virtualenv with:

```bash
cd <parent-folder>
git clone https://github.com/amigos-dev/lambda-venv.git
cd lambda-venv
poetry install
```

You can then launch a bash shell with the virtualenv activated using:

```bash
poetry shell
```

Example
========

TBD

Usage
=====

Command Line
------------

There is a single command tool `lambda-venv` that is installed with the package.


API
---

TBD

Known issues and limitations
----------------------------

TBD

Getting help
------------

Please report any problems/issues [here](https://github.com/amigos-dev/lambda-venv/issues).

Contributing
------------

Pull requests welcome.

License
-------

lambda-venv is distributed under the terms of the [MIT License](https://opensource.org/licenses/MIT).  The license applies to this file and other files in the [GitHub repository](http://github.com/amigos-dev/lambda-venv) hosting this file.

Authors and history
---------------------------

The initial author of aws-step-activity is [Sam McKelvie](https://github.com/sammck).
It is maintained by [Amigos Development, Inc.](https://amigos.dev).
