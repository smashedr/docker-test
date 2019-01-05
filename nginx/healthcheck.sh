#!/usr/bin/env bash

set -e

function trap_exit() { [[ "$?" = "0" ]] && exit 0 || exit 1 ; }
trap trap_exit EXIT SIGHUP SIGINT SIGTERM

curl -k "https://localhost:443" >/dev/null 2>&1
[[ "$?" != "0" ]] && exit 1

exit 0
