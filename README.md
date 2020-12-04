# Syscoin Sentinel

[![Build Status](https://travis-ci.org/syscoin/sentinel.svg?branch=master)](https://travis-ci.org/syscoin/sentinel)

> An automated governance helper for Syscoin Masternodes.

Sentinel is an autonomous agent for persisting, processing and automating Syscoin governance objects and tasks. It is a Python application which runs alongside the Syscoin instance on each Syscoin Masternode.

## Table of Contents
- [Install](#install)
  - [Dependencies](#dependencies)
- [Usage](#usage)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Maintainer](#maintainer)
- [Contributing](#contributing)
- [License](#license)

## Install

These instructions cover installing Sentinel on Ubuntu 18.04 / 20.04.

### Dependencies

Update system package list and install dependencies:

    $ sudo apt-get update
    $ sudo apt-get -y install git python3 virtualenv

Make sure Python version 3.6.x or above is installed:

    python3 --version

Make sure the local Syscoin daemon running is at least version 4.2.0.

    $ syscoind --version | head -n1

### Install Sentinel

Clone the Sentinel repo and install Python dependencies.

    $ git clone https://github.com/syscoin/sentinel.git && cd sentinel
    $ virtualenv -p $(which python3) ./venv
    $ ./venv/bin/pip install -r requirements.txt

## Usage

Sentinel is "used" as a script called from cron every minute.

### Set up Cron

Set up a crontab entry to call Sentinel every minute:

    $ crontab -e

In the crontab editor, add the lines below, replacing '/path/to/sentinel' to the path where you cloned sentinel to:

    * * * * * cd /path/to/sentinel && ./venv/bin/python bin/sentinel.py >/dev/null 2>&1

### Test Configuration

Test the config by running tests:

    $ ./venv/bin/py.test ./test

With all tests passing and crontab setup, Sentinel will stay in sync with syscoind and the installation is complete

## Configuration

An alternative (non-default) path to the `syscoin.conf` file can be specified in `sentinel.conf`:

    syscoin_conf=/path/to/syscoin.conf

## Troubleshooting

To view debug output, set the `SENTINEL_DEBUG` environment variable to anything non-zero, then run the script manually:

    $ SENTINEL_DEBUG=1 ./venv/bin/python bin/sentinel.py

## Maintainer

[@sidhujag](https://github.com/sidhujag)

## Contributing

Please follow the [Syscoin guidelines for contributing](https://github.com/syscoin/syscoin/blob/master/CONTRIBUTING.md).

Specifically:

* [Contributor Workflow](https://github.com/syscoin/syscoin/blob/master/CONTRIBUTING.md#contributor-workflow)

    To contribute a patch, the workflow is as follows:

    * Fork repository
    * Create topic branch
    * Commit patches

    In general commits should be atomic and diffs should be easy to read. For this reason do not mix any formatting fixes or code moves with actual code changes.

    Commit messages should be verbose by default, consisting of a short subject line (50 chars max), a blank line and detailed explanatory text as separate paragraph(s); unless the title alone is self-explanatory (like "Corrected typo in main.cpp") then a single title line is sufficient. Commit messages should be helpful to people reading your code in the future, so explain the reasoning for your decisions. Further explanation [here](http://chris.beams.io/posts/git-commit/).

## License

Released under the MIT license, under the same terms as Syscoin itself. See [LICENSE](LICENSE) for more info.
