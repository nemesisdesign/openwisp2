#!/bin/bash
set -e

# TODO: remove when openwisp-notifications 0.2 is released
pip install -U https://github.com/openwisp/openwisp-notifications/tarball/issues/38-disable-object-notification

# TODO: can be remove when openwisp-users 0.4.1 is released
# Commit needed for failures in tests:
# https://github.com/openwisp/openwisp-users/commit/ef347927136ddb4676479cb54cdc7cd08049e2e5
pip install -U --no-deps https://github.com/openwisp/openwisp-users/tarball/master
