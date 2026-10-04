# 02 - Private DNS (Task B)

| File | What it proves |
| --- | --- |
| `B1_dig_on_mac1.png` | dnsmasq on Mac 1 answers `app.team1.test -> 10.7.21.240` and forwards other names |
| `B2_dnsmasq_conf.png` | The DNS configuration (also in [../../dns/team-dnsmasq.conf](../../dns/team-dnsmasq.conf)) |
| `B3_dns_settings_mac3.png`, `B3_dns_settings_mac4.png` | Client Macs use 10.7.24.11 (Mac 1) as their DNS server |
| `B4_dig_from_mac3.png`, `B4_dig_from_mac4.png` | Clients resolve the name; `SERVER: 10.7.24.11#53` shows Mac 1 answered |
| `B5_dnsmasq_log.png` | The query arriving live on Mac 1: `query[A] app.team1.test from 10.7.x.x` |
