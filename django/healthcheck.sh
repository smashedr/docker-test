#!/usr/bin/env bash

set -e

function trap_exit() { [[ "$?" = "0" ]] && exit 0 || exit 1 ; }
trap trap_exit EXIT SIGHUP SIGINT SIGTERM

/usr/bin/pgrep gunicorn >/dev/null 2>&1
[[ "$?" != "0" ]] && exit 1

/usr/bin/curl -s "http://localhost:9000" >/dev/null 2>&1
[[ "$?" != "0" ]] && exit 1

exit 0
