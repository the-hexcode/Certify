# OpenSSL Certificate Generation Guide

This guide covers generating a local Root CA and issuing a server certificate for local development or internal use.

## 1. Generate the Root CA private key
Encrypted (you will be prompted for a passphrase):
```bash
openssl genrsa -aes256 -out rootca.key 4096
```
(Use `-aes256` to protect the key; remove it for an unencrypted key.)

## 2. Create the self-signed Root CA certificate
Common Name (CN) = your domain (e.g., example.com), not a host or wildcard.
```bash
openssl req -x509 -new -nodes -key rootca.key -sha256 -days 1826 -out rootca.crt
```
This produces `rootca.crt` (valid ~5 years).

## 3. Create server private key and CSR
Common Name (CN) = hostname (e.g., www.example.com).
```bash
openssl req -new -nodes -out cert.csr -newkey rsa:4096 -keyout cert.key
```

## 4. Create certificate extensions file
File: `cert.v3.ext` (must include at least the required basic constraint):
```
basicConstraints=CA:FALSE
authorityKeyIdentifier=keyid,issuer
subjectKeyIdentifier=hash
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = DNS:localhost, DNS:example.com
```
Adjust SAN entries as needed.

## 5. Sign the server certificate with the Root CA
```bash
openssl x509 -req -in cert.csr \
    -CA rootca.crt -CAkey rootca.key -CAcreateserial \
    -out cert.crt -days 730 -sha256 -extfile ./cert.v3.ext
```
Outputs:
- `cert.crt` (server certificate, ~2 years)
- `rootca.srl` (serial tracking file)

## 6. Verify artifacts
```bash
openssl x509 -in cert.crt -noout -text
openssl verify -CAfile rootca.crt cert.crt
```

## 7. (Optional) Create a full chain file
Some servers expect a bundle:
```bash
cat cert.crt rootca.crt > fullchain.crt
```

## 8. Trust the Root CA (local development)
- macOS: Keychain Access > System > Certificates > import `rootca.crt` > mark as trusted.
- Linux: Copy to `/usr/local/share/ca-certificates/` then `sudo update-ca-certificates`.
- Windows: Manage Computer Certificates > Trusted Root Certification Authorities > Certificates > Import.

## 9. File permissions
```bash
chmod 400 rootca.key cert.key
```

## 10. Renewal
Regenerate only the server CSR + signed cert before expiry. Keep `rootca.key` secure; compromise requires re-issuing all certs.

## Cleanup (optional)
Remove CSR after signing:
```bash
shred -u cert.csr
```

## Summary of core commands
```
openssl genrsa -aes256 -out rootca.key 4096
openssl req -x509 -new -nodes -key rootca.key -sha256 -days 1826 -out rootca.crt
openssl req -new -nodes -out cert.csr -newkey rsa:4096 -keyout cert.key
openssl x509 -req -in cert.csr -CA rootca.crt -CAkey rootca.key -CAcreateserial -out cert.crt -days 730 -sha256 -extfile ./cert.v3.ext
```

Minimum required in cert.v3.ext:
```
basicConstraints=CA:FALSE
```
