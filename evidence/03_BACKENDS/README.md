# 03 - Backends (Task C)

| File | What it proves |
| --- | --- |
| `C1_backends_from_mac2.png` | Mac 2 reaches Backend A (10.7.22.147:3001) and Backend B (10.7.19.69:3002) over the LAN; `X-Backend: A` / `B` |
| `C2_backend_a_on_mac3.png` | Backend A running on Mac 3, port 3001, `X-Backend: A`, `Cache-Control: no-store` |
| `C3_backend_b_on_mac4.png` | Backend B running on Mac 4, port 3002, `X-Backend: B` |

Source code: [../../backend/server.py](../../backend/server.py)
