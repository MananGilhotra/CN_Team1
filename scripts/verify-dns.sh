#!/usr/bin/env bash
# Run on a client Mac: checks that names resolve through Mac 1.
DNS=10.7.24.11
echo "== Configured DNS servers =="
networksetup -getdnsservers Wi-Fi
echo
echo "== Direct query to Mac 1 =="
dig @"$DNS" app.team1.test +short
dig @"$DNS" api.team1.test +short
echo
echo "== System resolver (what curl and browsers use) =="
dscacheutil -q host -a name app.team1.test
echo
echo "== Full dig answer =="
dig app.team1.test | grep -E "ANSWER SECTION|IN[[:space:]]+A|SERVER"
