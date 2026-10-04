# TLS certificate setup

We act as our own small Certificate Authority (CA). A root CA created on
Mac 2 signs the server certificate for `app.team1.test`, and every client
Mac trusts that root CA. No certificate warnings, and no `-k` / skipped
validation anywhere in the demo.

## Files

| File | What it is | Where it lives |
| --- | --- | --- |
| `team1-rootCA.key` | Root CA private key | Mac 2 only. Never shared, never committed. |
| `team1-rootCA.pem` | Root CA certificate (public) | Copied to Mac 1, Mac 3, Mac 4 and trusted |
| `app.team1.test.key` | Server private key | Mac 2: `/opt/homebrew/etc/nginx/certs/` |
| `app.team1.test.crt` | Server certificate signed by the root CA | Mac 2: `/opt/homebrew/etc/nginx/certs/` |
| `openssl-san.cnf` | SAN extensions (in this folder) | Used while signing |

## 1. Create the root CA and server certificate (Mac 2)

```bash
mkdir -p ~/team1-certs && cd ~/team1-certs

# Root CA
openssl genrsa -out team1-rootCA.key 4096
openssl req -x509 -new -nodes -key team1-rootCA.key -sha256 -days 365 \
  -out team1-rootCA.pem \
  -subj "/C=IN/O=Team1 CN Project/CN=Team1 Local Root CA"

# Server key + signing request
openssl genrsa -out app.team1.test.key 2048
openssl req -new -key app.team1.test.key -out app.team1.test.csr \
  -subj "/C=IN/O=Team1 CN Project/CN=app.team1.test"

# Root CA signs the server certificate (SANs from openssl-san.cnf)
openssl x509 -req -in app.team1.test.csr \
  -CA team1-rootCA.pem -CAkey team1-rootCA.key -CAcreateserial \
  -out app.team1.test.crt -days 365 -sha256 \
  -extfile openssl-san.cnf

# Give nginx the server certificate + key
mkdir -p /opt/homebrew/etc/nginx/certs
cp app.team1.test.crt app.team1.test.key /opt/homebrew/etc/nginx/certs/
```

## 2. Verify

```bash
openssl verify -CAfile team1-rootCA.pem app.team1.test.crt
# app.team1.test.crt: OK

openssl x509 -in app.team1.test.crt -noout -subject -issuer -ext subjectAltName
# subject=C=IN, O=Team1 CN Project, CN=app.team1.test
# issuer=C=IN, O=Team1 CN Project, CN=Team1 Local Root CA
# X509v3 Subject Alternative Name: DNS:app.team1.test, DNS:api.team1.test
```

## 3. Trust the root CA on every client (Mac 1, Mac 3, Mac 4)

Copy only `team1-rootCA.pem` (AirDrop), then:

```bash
sudo security add-trusted-cert -d -r trustRoot \
  -k /Library/Keychains/System.keychain ~/Downloads/team1-rootCA.pem
```

Check in Keychain Access → System → "Team1 Local Root CA" → Trust →
"Always Trust".

## 4. curl with real validation

Some macOS curl builds do not read the Keychain, so we pass the CA file.
This is full certificate validation, not a bypass:

```bash
cp ~/Downloads/team1-rootCA.pem ~/team1-rootCA.pem
echo "alias tcurl='curl --cacert ~/team1-rootCA.pem'" >> ~/.zshrc
source ~/.zshrc

tcurl -v https://app.team1.test/api/status
# ... SSL certificate verify ok.
```

## TLS handshake (what the Wireshark capture shows, TLS 1.2)

ClientHello (SNI = app.team1.test) → ServerHello → Certificate →
ServerKeyExchange → ServerHelloDone → ClientKeyExchange →
ChangeCipherSpec → Finished → encrypted Application Data.

With TLS 1.3 the Certificate message is encrypted, which is why the
evidence capture was taken with `curl --tls-max 1.2`.
