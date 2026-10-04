#!/usr/bin/env bash
# Backend B - runs on Mac 4 (10.7.19.69), port 3002
cd "$(dirname "$0")"
exec python3 server.py B 3002
