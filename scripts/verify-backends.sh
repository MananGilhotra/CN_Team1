#!/usr/bin/env bash
# Run on Mac 2: checks that both backends answer directly by IP.
for target in 10.7.22.147:3001 10.7.19.69:3002; do
  echo "== $target =="
  curl -s -i "http://$target/api/status" | grep -iE "^HTTP|x-backend"
done
