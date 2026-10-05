# 04 - Reverse proxy and load balancing (Task D)

| File | What it proves |
| --- | --- |
| `D1_round_robin.png` | Six requests from Mac 4 to `https://app.team1.test` alternate A, B, A, B, A, B (header and JSON body show Mac 3 / Mac 4) |
| `D2_http_versions.png` | The edge serves both `HTTP/1.1 200 OK` and `HTTP/2 200` |
| `D3_access_log.png` | nginx access log on Mac 2: requests from Mac 4 (10.7.19.69) alternate between Backend A (10.7.22.147:3001) and Backend B (10.7.19.69:3002). The line `10.7.22.147:3001, 10.7.19.69:3002` (15:18:45) is the H3 test: nginx tried A, it was down, and the request was retried on B |
| `D4_nginx_config_test_and_local_lb.png` | `nginx -t` passes on Mac 2, and a local test alternates A, B, A, B |

Round-robin from Mac 1 is also visible at the top of `../02_DNS/B2_dnsmasq_conf.png`.

Configuration: [../../nginx/nginx.conf](../../nginx/nginx.conf)
