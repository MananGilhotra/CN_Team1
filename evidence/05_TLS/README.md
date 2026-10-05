# 05 - HTTPS / TLS (Task E)

| File | What it proves |
| --- | --- |
| `E1_cert_details.txt` | `openssl verify` returns OK against our root CA; subject, issuer and SANs (`app.team1.test`, `api.team1.test`) |
| `E2_keychain_trusted_root_ca.png` | Keychain Access (System keychain): "Team1 Local Root CA" set to Always Trust, "marked as trusted for all users", expires 5 Oct 2027 |
| `E3_browser_certificate.png` | Browser certificate viewer: issued to `app.team1.test`, issued by Team1 Local Root CA, valid one year |
| `E4_curl_verbose.png` | `curl -v`: TCP connect to 10.7.21.240:443 -> TLS 1.3 handshake -> `SSL certificate verify ok` -> HTTP/2 request |
| `E5_curl_tls12_verbose.png` | Same request forced to TLS 1.2 (used for the Wireshark capture): verify ok, `x-backend`, `x-edge: mac2-nginx` |

No validation is skipped anywhere: curl uses `--cacert` with our root CA, never `-k`.

Setup steps: [../../tls/certificate-setup.md](../../tls/certificate-setup.md)
