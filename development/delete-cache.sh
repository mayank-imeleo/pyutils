#!/bin/bash

set -eu

# https://setuptools.pypa.io/en/latest/userguide/datafiles.html
# https://setuptools.pypa.io/en/latest/userguide/miscellaneous.html#caching-and-troubleshooting

rm build/ -rf
rm dist/ -rf
rm pyutils.egg-info/ -rf