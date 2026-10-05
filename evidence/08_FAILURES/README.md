# 08 - Required failure demonstrations (brief section 6.3)

These runs use the loopback test setup, where each Mac role has its own
address: 127.0.0.11 = DNS (Mac 1), 127.0.0.12 = nginx edge (Mac 2),
127.0.0.13 = Backend A (Mac 3), 127.0.0.14 = Backend B (Mac 4).

| File | Failure | Last layer that worked | First layer that failed |
| --- | --- | --- | --- |
| `H1_wrong_dns_server.png` | Client resolver for `team1.test` pointed at 127.0.0.1 instead of the team DNS server | IP: `ping 127.0.0.12` still works | DNS: `dscacheutil` returns no address and `curl` hangs; restoring `nameserver 127.0.0.11` fixes it |
| `H2_wrong_record.png` | On Mac 1, `app.team1.test` changed to 127.0.0.13 (Backend A, not the edge) | DNS: answers, but with the wrong address | TCP: `connection refused` on 127.0.0.13:443 (no TLS listener there); record restored to 127.0.0.12 afterwards |
| `H3_one_backend_down.png` | Backend A stopped | Everything: nginx retries on B | None for the user: six of six requests served by `X-Backend: B`; after restart A/B alternate again |
| `H4_both_backends_down.png` | Both backends stopped | DNS, TCP and TLS 1.3 to the edge (`SSL certificate verify ok`) | Behind the edge: `HTTP/2 502`, error log shows `connect() failed (61: Connection refused)` to 127.0.0.13:3001 and 127.0.0.14:3002 |
| `H4b_backend_b_stopped_502.png` | Same failure, second run: Backend B stopped with Ctrl+C after serving requests | DNS, TCP, TLS to the edge | `HTTP/2 502 Bad Gateway` with `x-edge: mac2-nginx` |
| `H5_wrong_port.png` | Client connects to port 4443 | IP (`ping` works) and TCP on 443 (`nc` succeeds) | TCP: `Connection refused` on 4443 |
