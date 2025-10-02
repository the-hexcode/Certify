# Cloudflare Origin TLS Client Auth Wrapper

This module provides async helper methods to manage Origin TLS Client Authentication certificates and hostnames via Cloudflare's API.

## Features
- Upload (create) client auth certificates
- List uploaded certificates
- Enable/disable Authenticated Origin Pulls per hostname with a specific certificate
- Query existing hostname configuration

## Prerequisites
- Python 3.11+
- `aiohttp` (see project `requirements.txt`)
- Cloudflare API Token with permissions for: Zone > Origin TLS Client Auth (Edit / Read as needed)
- Your Zone ID

## Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

## Environment / Setup
Export (or otherwise supply) the following values securely:
- CLOUDFLARE_API_TOKEN
- CLOUDFLARE_ZONE_ID

Never commit secrets. Prefer environment variables or a secrets manager.

## Usage Example
```python
import asyncio
from cloudflare import Cloudflare

ZONE_ID = "<your-zone-id>"
API_TOKEN = "<your-api-token>"

async def main():
    cf = Cloudflare(ZONE_ID, API_TOKEN)

    # 1. Upload a certificate + private key
    upload_resp = await cf.upload_cert("pki/cert.crt", "pki/cert.key")
    print("Upload:", upload_resp)

    # Extract cert_id (adjust according to actual response schema)
    cert_id = upload_resp.get("result", {}).get("id")

    # 2. List certificates
    certs = await cf.get_certs()
    print("Certificates:", certs)

    # 3. Enable Authenticated Origin Pulls for a hostname
    if cert_id:
        enable_resp = await cf.enable_aop("example.com", cert_id, enable=True)
        print("Enable AOP:", enable_resp)

    # 4. Fetch hostnames configuration
    host_cfg = await cf.get_aop_hostnames()
    print("Hostnames:", host_cfg)

asyncio.run(main())
```

## API Reference
### Class: `Cloudflare(zone_id: str, api_token: str)`
Creates a client bound to a zone.

### Methods
#### `upload_cert(cert_path: str, key_path: str)`
Uploads a certificate + private key for Origin TLS Client Auth.
Returns JSON response from Cloudflare.

#### `get_certs()`
Lists certificates uploaded for the zone.

#### `enable_aop(hostname: str, cert_id: str, enable: bool = True)`
Enables or disables AOP for a hostname with the specified `cert_id`.

#### `get_aop_hostnames(hostname: str | None = None)`
Fetches all hostnames (or a single one if provided) with AOP configuration.

## Notes
- The response JSON structure may change; inspect responses when integrating.
- Consider adding retries / error handling in production (HTTP failures, rate limiting).
- Avoid reading key/cert files into memory in multi-tenant environments; use secure storage abstractions.

## Future Improvements
- Add delete / rotate certificate method.
- Add structured response models (e.g., with `pydantic`).
