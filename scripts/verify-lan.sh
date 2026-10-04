#!/usr/bin/env bash
# Run on any Mac: shows this Mac's network details and pings all four Macs.
IF=$(route -n get default | awk '/interface:/{print $2}')
echo "Computer : $(scutil --get ComputerName)"
echo "Interface: $IF"
echo "IPv4     : $(ipconfig getifaddr "$IF")"
echo "Mask     : $(ipconfig getoption "$IF" subnet_mask)"
echo "Gateway  : $(route -n get default | awk '/gateway:/{print $2}')"
echo "MAC      : $(ifconfig "$IF" | awk '/ether/{print $2}')"
echo
for ip in 10.7.24.11 10.7.21.240 10.7.22.147 10.7.19.69; do
  echo "== $ip =="
  ping -c 3 "$ip" | tail -2
done
