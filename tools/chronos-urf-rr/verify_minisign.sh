#!/usr/bin/env sh
set -e
minisign -Vm "$1" -P "$(tail -n 1 certs/chronos-urf-rr/CHRONOS_URF_RR_CERT.pub)"
