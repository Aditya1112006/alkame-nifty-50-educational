import sys

file_path = "nginx/nginx.conf"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

security_headers = """
            add_header X-Content-Type-Options "nosniff" always;
            add_header X-Frame-Options "DENY" always;
            add_header X-XSS-Protection "1; mode=block" always;
            add_header Referrer-Policy "strict-origin-when-cross-origin" always;
            add_header Content-Security-Policy "default-src 'self'; frame-ancestors 'none';" always;
            add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
            
            proxy_pass http://fastapi_app;"""

if "X-Content-Type-Options" not in content:
    content = content.replace("            proxy_pass http://fastapi_app;", security_headers)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
