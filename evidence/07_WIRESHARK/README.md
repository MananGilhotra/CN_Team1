# 07 - Packet capture and protocol flow (Task G)

| File | What it proves |
| --- | --- |
| `G1_client_tls12.pcapng` | Full capture on Mac 4 of one request (TLS 1.2, so the Certificate message is visible) |
| `G2_client_tls13.pcapng` | Same request with TLS 1.3, for comparison |
| `G3_dns.png` | DNS query 10.7.19.69 -> 10.7.24.11:53 (UDP) and the answer 10.7.21.240 |
| `G4_tcp_handshake.png` | SYN -> SYN-ACK -> ACK to port 443, client ephemeral source port |
| `G5_tls_handshake.png` | ClientHello (SNI), ServerHello, Certificate, key exchange, ChangeCipherSpec |
| `G6_encrypted_http.png` | HTTP is only visible as encrypted Application Data |
| `G7_ports.png` | Socket pairs: client:ephemeral <-> 53/UDP and client:ephemeral <-> 443/TCP |
| `G8_flow_graph.png` | Whole flow in order: DNS -> TCP -> TLS -> data |
| `G9_plain_backend_hop.png` | On Mac 2, the edge-to-backend hop is plain HTTP (`X-Backend: A/B` readable), proving TLS terminates at the edge |

Wireshark display filters used: `dns.qry.name == "app.team1.test"`,
`tcp.port == 443`, `tls.handshake`, `tls.app_data`.
