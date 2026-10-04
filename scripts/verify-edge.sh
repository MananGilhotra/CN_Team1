#!/usr/bin/env bash
# Run on a client Mac (after trusting the CA): HTTPS + load balancing.
CA="$HOME/team1-rootCA.pem"
URL="https://app.team1.test/api/status"

echo "== TLS + headers =="
curl -sv --cacert "$CA" "$URL" -o /dev/null 2>&1 \
  | grep -iE "Connected to|SSL connection|verify ok|< HTTP|< x-backend"

echo
echo "== Six requests (round-robin) =="
for i in 1 2 3 4 5 6; do
  curl -si --cacert "$CA" "$URL" | grep -i x-backend
done

echo
echo "== HTTP versions =="
curl -sI --http1.1 --cacert "$CA" https://app.team1.test/ | head -1
curl -sI --cacert "$CA" https://app.team1.test/ | head -1
