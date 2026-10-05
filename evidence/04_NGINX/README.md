# 04 - Reverse proxy and load balancing (Task D)

| File | What it proves |
| --- | --- |
| `D1_round_robin.png` | Six requests from Mac 4 to `https://app.team1.test` alternate A, B, A, B, A, B (header and JSON body show Mac 3 / Mac 4) |
| `D2_http_versions.png` | The edge serves both `HTTP/1.1 200 OK` and `HTTP/2 200` |
| `D4_nginx_config_test_and_local_lb.png` | `nginx -t` passes on Mac 2, and a local test alternates A, B, A, B |

Round-robin from Mac 1 is also visible at the top of `../02_DNS/B2_dnsmasq_conf.png`.

Configuration: [../../nginx/nginx.conf](../../nginx/nginx.conf)
