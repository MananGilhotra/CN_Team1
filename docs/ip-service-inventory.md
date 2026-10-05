# IP and service inventory

All four Macs are on the same private Wi-Fi LAN.

- Network: 10.7.0.0/19 (subnet mask 255.255.224.0)
- Usable range: 10.7.0.1 - 10.7.31.254
- Default gateway: 10.7.0.1
- Interface on every Mac: en0 (Wi-Fi)
- Private domain: team1.test (`.test` is reserved for testing; `.local` is avoided because macOS uses it for mDNS)

## Machines

| Mac | Role | Owner | IPv4 | Mask / prefix | Gateway | MAC address |
| --- | --- | --- | --- | --- | --- | --- |
| Mac 1 | Private DNS server + test client | Harshita | 10.7.24.11 | 255.255.224.0 (/19) | 10.7.0.1 | 7a:ce:a3:b1:ac:0c |
| Mac 2 | Edge reverse proxy + load balancer (TLS) | Yashi | 10.7.21.240 | 255.255.224.0 (/19) | 10.7.0.1 | 6e:52:40:c4:65:03 |
| Mac 3 | Backend A | Manan | 10.7.22.147 | 255.255.224.0 (/19) | 10.7.0.1 | 46:c0:ce:cd:b4:e4 |
| Mac 4 | Backend B + main test client | Akhil | 10.7.19.69 | 255.255.224.0 (/19) | 10.7.0.1 | 9e:92:d0:0e:ab:aa |

## Services and ports

| Mac | Service | Software | Port / protocol | Listens on |
| --- | --- | --- | --- | --- |
| Mac 1 | DNS for `team1.test` | dnsmasq 2.93 | 53 / UDP + TCP | 127.0.0.1, 10.7.24.11 |
| Mac 2 | HTTP redirect | nginx | 80 / TCP | all interfaces |
| Mac 2 | HTTPS edge + load balancer | nginx (HTTP/1.1 + HTTP/2, TLS 1.2/1.3) | 443 / TCP | all interfaces |
| Mac 3 | Backend A REST API | Python `http.server` | 3001 / TCP | 0.0.0.0 |
| Mac 4 | Backend B REST API | Python `http.server` | 3002 / TCP | 0.0.0.0 |

## DNS records (served by Mac 1)

| Name | Type | Value | TTL |
| --- | --- | --- | --- |
| app.team1.test | A | 10.7.21.240 (Mac 2) | 30 s |
| api.team1.test | A | 10.7.21.240 (Mac 2) | 30 s |

## Client DNS settings

| Mac | DNS server |
| --- | --- |
| Mac 1 | 10.7.24.11 (itself) |
| Mac 2 | 10.7.24.11 |
| Mac 3 | 10.7.24.11 |
| Mac 4 | 10.7.24.11 |

## Backend endpoints

| Endpoint | Response | Cache header |
| --- | --- | --- |
| `GET /` | HTML page "Backend A/B is running" | `Cache-Control: no-store` |
| `GET /api/status` | `{"backend": "A", "status": "ok", ...}` | `Cache-Control: no-store` |
| `GET /api/info` | Identical JSON on both backends | `Cache-Control: public, max-age=60` + `ETag` |
| every response | header `X-Backend: A` or `X-Backend: B` | - |
