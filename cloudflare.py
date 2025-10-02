from aiohttp import ClientSession
import json

class Cloudflare:
    def __init__(self, zone_id, api_token):
        self.base_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/origin_tls_client_auth"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

    # Push the certificate
    async def upload_cert(self, cert_path, key_path):
        url = self.base_url + "/hostnames/certificates"
        # MYCERT="$(cat cert.crt|perl -pe 's/\r?\n/\\n/'|sed -e 's/..$//')"
        cert = open(cert_path).read()
        key = open(key_path).read()
        data = {
            "certificate": cert,
            "private_key": key,
        }
        async with ClientSession() as session:
            async with session.post(url, json=data, headers=self.headers) as response:
                return await response.json()

    # TODO: Implement PUT to enable Authenticated Origin Pulls for specific hostnames