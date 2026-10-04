# 06 - HTTP caching (Task F)

| File | What it proves |
| --- | --- |
| `F1_cache_headers.png` | `/api/info` returns `Cache-Control: public, max-age=60` and an `ETag` |
| `F2_304_curl.png` | Conditional request with `If-None-Match` returns `304 Not Modified` from both backends |
| `F3_browser_full.png` | Full request: `200` with body |
| `F4_browser_cache_hit.png` | Fresh cache hit: `(memory cache)` / `(disk cache)`, no request reaches the server |
| `F5_browser_304.png` | Reload sends a conditional request and gets `304` |
