#!/usr/bin/env bash
# Backend A - runs on Mac 3 (10.7.22.147), port 3001
cd "$(dirname "$0")"
exec python3 server.py A 3001
