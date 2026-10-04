# 08 - Required failure demonstrations (brief section 6.3)

| File | Failure | Last layer that worked | First layer that failed |
| --- | --- | --- | --- |
| `H1_wrong_dns_server.png` | Client uses 8.8.8.8 instead of Mac 1 | IP (ping still works) | DNS: NXDOMAIN |
| `H2_wrong_record.png` | `app.team1.test` points to Mac 3 | DNS (answers, but wrongly) | TCP: connection refused on 10.7.22.147:443 |
| `H3_one_backend_down.png` | Backend A stopped | Everything; nginx retries on B | None for the user: all requests served by B |
| `H4_both_backends_down.png` | Both backends stopped | DNS, TCP, TLS to the edge | Behind the edge: HTTP 502 Bad Gateway |
| `H5_wrong_port.png` | Client connects to port 4443 | IP (ping, port 443 works) | TCP: connection refused (RST) on 4443 |
