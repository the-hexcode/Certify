# Enabling `ssl_verify_client` on NGINX

To require client certificate authentication in NGINX, use the `ssl_verify_client` directive. Below is a sample configuration:

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate     /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;

    ssl_client_certificate /etc/nginx/ssl/ca.crt;
    ssl_verify_client on;

    location / {
        # Your configuration here
    }
}
```

**Key points:**
- `ssl_client_certificate` specifies the CA certificate used to verify client certificates.
- `ssl_verify_client on;` enforces client certificate verification.

Reload NGINX after making changes:

```sh
sudo nginx -s reload
OR
sudo systemctl reload nginx
```