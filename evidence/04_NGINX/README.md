# 04 - Reverse proxy and load balancing (Task D)

| File | What it proves |
| --- | --- |
| `D1_round_robin.png` | Six requests from Mac 4 alternate `x-backend: A, B, A, B...` |
| `D1b_round_robin_from_mac1.png` | The same from Mac 1 |
| `D2_http_versions.png` | HTTP/1.1 and HTTP/2 both served by the edge |
| `D3_nginx_log.png` | nginx access log on Mac 2 alternating between `:3001` and `:3002` |

Configuration: [../../nginx/nginx.conf](../../nginx/nginx.conf)
