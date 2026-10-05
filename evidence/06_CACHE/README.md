# 06 - HTTP caching (Task F)

Endpoint used: `GET https://app.team1.test/api/info` (identical on both backends).

| File | What it proves |
| --- | --- |
| `F1_cache_headers.txt` | `/api/info` returns `Cache-Control: public, max-age=60` and `ETag: "d45923083f0a9a28"` |
| `F2_304_curl.txt` | Conditional request with `If-None-Match` returns `304 Not Modified` from both Backend A and Backend B; a non-matching ETag returns a full `200` |

Three cases:

| Case | What happens |
| --- | --- |
| Fresh cache hit | Within `max-age` (60 s) the browser reuses its copy; no request reaches the server |
| Conditional request | After expiry the client sends `If-None-Match`; unchanged content returns `304` with no body |
| Full request | No (or a non-matching) validator; the server returns `200` with the full body |

`/api/status` uses `Cache-Control: no-store`, so load balancing is never hidden by caching.
