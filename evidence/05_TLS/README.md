# 05 - HTTPS / TLS (Task E)

| File | What it proves |
| --- | --- |
| `E1_cert_details.png` | Server certificate verified against our root CA; SANs `app.team1.test`, `api.team1.test` |
| `E2_keychain_trust.png` | Team1 Local Root CA set to "Always Trust" on a client |
| `E3_browser_padlock.png` | Browser opens `https://app.team1.test` with no warning; issued by Team1 Local Root CA |
| `E4_curl_verbose.png` | `curl -v`: TCP connect -> TLS 1.3 -> `SSL certificate verify ok` -> HTTP/2 request |

Setup steps: [../../tls/certificate-setup.md](../../tls/certificate-setup.md)
