# CN Project - Private Network Service Platform (Team 1)

Computer Networks course project, Phase 1: **Build & Observe**.

Four Macs on one private Wi-Fi LAN provide a small HTTPS service at
`https://app.team1.test`. The name is resolved by our own DNS server, TLS
terminates at an nginx edge, and nginx load-balances requests across two
backends. The application is deliberately simple; the network is the
project.

![Topology](docs/topology.png)

## Team and machines

| Mac | Role | Team member | IP | Service |
| --- | --- | --- | --- | --- |
| Mac 1 | Private DNS server + test client | Harshita | 10.7.24.11 | dnsmasq, port 53 |
| Mac 2 | Edge reverse proxy + load balancer (TLS) | Yashi | 10.7.21.240 | nginx, ports 80 / 443 |
| Mac 3 | Backend A | Manan | 10.7.22.147 | Python REST API, port 3001 |
| Mac 4 | Backend B + main test client | Akhil | 10.7.19.69 | Python REST API, port 3002, Wireshark |

Network: 10.7.0.0/19 (mask 255.255.224.0), gateway 10.7.0.1.
Domain: `team1.test` (`app.team1.test`, `api.team1.test` -> Mac 2).

## Request flow

```
Client (Mac 4) --DNS query, UDP 53--> Mac 1 (dnsmasq)   answer: 10.7.21.240
Client (Mac 4) --HTTPS, TCP 443-----> Mac 2 (nginx, TLS terminates here)
                                        |--plain HTTP--> Mac 3  Backend A :3001
                                        |--plain HTTP--> Mac 4  Backend B :3002
```

![Request flow](docs/request-flow.png)

## Repository layout

| Path | Contents |
| --- | --- |
| [`backend/`](backend) | `server.py` (both backends), `run-backend-a.sh`, `run-backend-b.sh` |
| [`dns/`](dns) | `team-dnsmasq.conf` - DNS configuration for Mac 1 |
| [`nginx/`](nginx) | `nginx.conf` - edge, TLS and load-balancer configuration for Mac 2 |
| [`tls/`](tls) | `certificate-setup.md` (CA + certificate steps), `openssl-san.cnf` |
| [`scripts/`](scripts) | `verify-lan.sh`, `verify-dns.sh`, `verify-backends.sh`, `verify-edge.sh` |
| [`docs/`](docs) | `architecture.md`, `ip-service-inventory.md`, `topology.png`, `request-flow.png` |
| [`evidence/`](evidence) | Screenshots and packet captures for every task (see below) |

## Running it

**Mac 1 - DNS**

```bash
brew install dnsmasq
cp dns/team-dnsmasq.conf /opt/homebrew/etc/dnsmasq.conf
sudo brew services start dnsmasq
sudo tail -f /tmp/dnsmasq.log
```

**Mac 2 - Edge** (certificate first, see [`tls/certificate-setup.md`](tls/certificate-setup.md))

```bash
brew install nginx
cp nginx/nginx.conf /opt/homebrew/etc/nginx/servers/team1.conf
sudo nginx -t && sudo nginx
tail -f /opt/homebrew/var/log/nginx/team1_access.log
```

**Mac 3 - Backend A**

```bash
./backend/run-backend-a.sh
```

**Mac 4 - Backend B**

```bash
./backend/run-backend-b.sh
```

**Every client** - DNS points at Mac 1, and the Team 1 root CA is trusted:

```bash
sudo networksetup -setdnsservers Wi-Fi 10.7.24.11
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
```

## Verifying

| Script | Run on | Checks |
| --- | --- | --- |
| `scripts/verify-lan.sh` | any Mac | IP details + ping to all four Macs |
| `scripts/verify-dns.sh` | client | Name resolves to 10.7.21.240 via 10.7.24.11 |
| `scripts/verify-backends.sh` | Mac 2 | Both backends answer directly by IP |
| `scripts/verify-edge.sh` | client | TLS validation, round-robin A/B, HTTP/1.1 and HTTP/2 |

## Evidence index

| Folder | Brief task | Marks |
| --- | --- | --- |
| [`evidence/01_LAN`](evidence/01_LAN) | Task A - private LAN, IP inventory, ping | 10 (with Task B) |
| [`evidence/02_DNS`](evidence/02_DNS) | Task B - private DNS server and client resolvers | |
| [`evidence/03_BACKENDS`](evidence/03_BACKENDS) | Task C - two REST backends | 10 (with Task D) |
| [`evidence/04_NGINX`](evidence/04_NGINX) | Task D - reverse proxy and round-robin load balancing | |
| [`evidence/05_TLS`](evidence/05_TLS) | Task E - HTTPS with our own CA | 8 |
| [`evidence/06_CACHE`](evidence/06_CACHE) | Task F - Cache-Control, ETag, 304 | 5 |
| [`evidence/07_WIRESHARK`](evidence/07_WIRESHARK) | Task G - DNS, TCP, TLS, ports in packet captures | 7 |
| [`evidence/08_FAILURES`](evidence/08_FAILURES) | Section 6.3 - five required failure demonstrations | live demo |

Each evidence folder has a README that lists every file and what it proves.

## Security note

Private keys (`*.key`) are excluded by `.gitignore` and never leave Mac 2.
Only the public root CA certificate is shared with client Macs.
