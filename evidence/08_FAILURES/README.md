# 08 - Required failure demonstrations (brief section 6.3)

All runs on the four-Mac LAN. Client: Mac 4 (10.7.19.69).

| File | Failure | Last layer that worked | First layer that failed |
| --- | --- | --- | --- |
| `H1_wrong_dns_server.png` | Mac 4 uses 8.8.8.8 instead of Mac 1 (10.7.24.11) | IP: `ping 10.7.21.240` still works | DNS: NXDOMAIN from 8.8.8.8, curl cannot resolve the host |
| `H2_wrong_record.png` | On Mac 1, `app.team1.test` changed to point at Mac 3 (10.7.22.147) | DNS: answers, but with the wrong address | TCP: connection refused on 10.7.22.147:443 |
| `H3_one_backend_down.png` | Backend A on Mac 3 stopped | Everything: nginx retries on B | None for the user: all six requests served by `X-Backend: B`; the nginx access log shows the first request tried A, failed, and was retried on B |
| `H4_both_backends_down.png` | Backends on Mac 3 and Mac 4 stopped | DNS, TCP and TLS to the edge (Mac 2) | Behind the edge: HTTP 502 Bad Gateway; nginx error log shows `connect() failed` to 10.7.22.147:3001 and 10.7.19.69:3002 |
| `H5_wrong_port.png` | Mac 4 connects to port 4443 instead of 443 | IP (`ping`) and TCP on 443 | TCP: connection refused on 10.7.21.240:4443 |

After each test the change was undone (DNS server, DNS record, backends restarted).
