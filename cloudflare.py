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

    # Get the certificates
    async def get_certs(self):
        url = self.base_url + "/hostnames/certificates"
        async with ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                return await response.json()

    # Enable Authenticated Origin Pulls for specific hostnames
    async def enable_aop(self, hostname, cert_id, enable=True):
        url = self.base_url + "/hostnames"
        data = {
            "config": [
                {
                    "cert_id": cert_id,
                    "hostname": hostname,
                    "enabled": enable
                }
            ]
        }
        async with ClientSession() as session:
            async with session.put(url, json=data, headers=self.headers) as response:
                return await response.json()

    # Get the hostnames with Authenticated Origin Pulls enabled
    async def get_aop_hostnames(self, hostname=None):
        url = self.base_url + "/hostnames"
        if hostname:
            url += f"/{hostname}"
        async with ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                return await response.json()
