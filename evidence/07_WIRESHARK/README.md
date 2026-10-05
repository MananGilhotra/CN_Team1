# 07 - Packet capture and protocol flow (Task G)

Capture taken on Mac 4 (10.7.19.69) on interface en0 while requesting
`https://app.team1.test/api/status` with TLS 1.2, so the Certificate message
is visible.

| File | What it proves |
| --- | --- |
| `G1_client_tls12.pcapng` | Capture file behind G3-G8 (Mac 4, en0, TLS 1.2), filtered to project traffic only: DNS query to 10.7.24.11 -> TLS 1.2 handshake with 10.7.21.240:443 -> plain HTTP hop from the edge to Backend B (10.7.19.69:3002) |
| `G2_client_tls13.pcapng` | Second capture on Mac 4 (en0) with TLS 1.3, filtered to project traffic: DNS query to 10.7.24.11 -> TCP handshake and TLS 1.3 with 10.7.21.240:443. Server Hello is followed directly by encrypted records, so the Certificate is not visible - the reason G1 uses TLS 1.2. The same request was sent to Backend B, so the plain HTTP hop 10.7.21.240 -> 10.7.19.69:3002 (`GET /api/status`, `200 OK`) is also visible |
| `G3_dns.png` | DNS query 10.7.19.69:53887 -> 10.7.24.11:53 (UDP) and the answer `A 10.7.21.240` |
| `G4_tcp_handshake.png` | TCP traffic on port 443 (filter `tcp.port == 443`) |
| `G5_tls_handshake.png` | ClientHello (SNI=app.team1.test) -> Server Hello, Certificate -> Server Key Exchange, Server Hello Done -> Client Key Exchange, Change Cipher Spec -> Change Cipher Spec, Encrypted Handshake Message |
| `G6_encrypted_http.png` | HTTP between 10.7.19.69 and 10.7.21.240 only appears as encrypted Application Data |
| `G7_ports.png` | TCP conversations: client ephemeral port 50862 <-> 10.7.21.240:443 |
| `G8_flow_graph.png` | Flow graph of the capture |
| `G9_plain_backend_hop.txt` | tcpdump on Mac 2: the edge-to-backend hop is plain HTTP, alternating `X-Backend: A` / `B`, proving TLS terminates at the edge |

Both capture files were filtered so they contain only project traffic (unrelated browsing and mDNS removed).
Open them in Wireshark to repeat any screenshot.

Wireshark display filters used: `dns.qry.name == "app.team1.test"`,
`tcp.port == 443`, `tls.handshake`, `tls.app_data`.
