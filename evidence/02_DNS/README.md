# 02 - Private DNS (Task B)

| File | What it proves |
| --- | --- |
| `B1_dig_on_mac1.png` | dnsmasq starts on Mac 1 and answers `app.team1.test -> 10.7.21.240`; other names (google.com) are forwarded |
| `B2_dnsmasq_conf.png` | The DNS configuration on Mac 1 (also in [../../dns/team-dnsmasq.conf](../../dns/team-dnsmasq.conf)) |
| `B3_dns_settings_mac3.png` | Client DNS server set to 10.7.24.11 (Mac 1) |
| `B4_dig_from_mac3.png` | Mac 3 resolves `app.team1.test -> 10.7.21.240`, TTL 30, `SERVER: 10.7.24.11#53`, `aa` flag |
| `B4_dig_from_mac4.png` | Mac 4 resolves the same name through Mac 1 |
