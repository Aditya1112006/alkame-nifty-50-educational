import sys
import re

file_path = "api.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add imports if missing
if "from database import SessionLocal" not in content:
    content = content.replace("from fastapi.responses import", "from database import SessionLocal\nfrom models import AuditLog\nfrom fastapi.responses import")

if "from datetime import datetime, timezone" not in content:
    content = content.replace("import logging", "import logging\nfrom datetime import datetime, timezone")

# Add middleware for security headers
middleware_code = '''
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none';"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

def log_audit_event(client: ClientAuth, action: str, resource: str, status: str, details: str, request: Request):
    ip_address = request.client.host if request and request.client else "unknown"
    key_prefix = client.key[:6] if client.key else "none"
    try:
        with SessionLocal() as db:
            audit = AuditLog(
                timestamp=datetime.now(timezone.utc).isoformat(),
                client_key_prefix=key_prefix,
                client_role=client.role,
                action=action,
                resource=resource,
                status=status,
                details=details,
                ip_address=ip_address
            )
            db.add(audit)
            db.commit()
    except Exception as e:
        logger.error(f"Failed to record audit log: {e}")
'''
if "security_headers_middleware" not in content:
    content = content.replace("app.add_middleware(", f"{middleware_code}\napp.add_middleware(")

# Update set_risk_toggle to include request and log_audit_event
if "request: Request," not in content.split("def set_risk_toggle(")[1].split(")")[0]:
    content = content.replace(
        "def set_risk_toggle(enabled: bool, client: ClientAuth = Depends(require_role(\"ADMIN\"))):",
        "def set_risk_toggle(enabled: bool, request: Request, client: ClientAuth = Depends(require_role(\"ADMIN\"))):"
    )
    content = content.replace(
        "return {\"status\": \"success\", \"enabled\": state.enabled}",
        "log_audit_event(client, 'TOGGLE_RISK', 'global_risk', 'SUCCESS', f'Set enabled={enabled}', request)\n    return {\"status\": \"success\", \"enabled\": state.enabled}"
    )

# Update refresh_backtest similarly
if "def refresh_backtest(symbol: str, response: Response = Response(), client: ClientAuth = Depends(get_current_client)):" in content:
    content = content.replace(
        "def refresh_backtest(symbol: str, response: Response = Response(), client: ClientAuth = Depends(get_current_client)):",
        "def refresh_backtest(symbol: str, request: Request, response: Response = Response(), client: ClientAuth = Depends(get_current_client)):"
    )
    content = content.replace(
        "return {\"status\": \"success\", \"symbol\": symbol, \"refreshed\": refreshed}",
        "log_audit_event(client, 'REFRESH', f'symbol={symbol}', 'SUCCESS', f'Refreshed {refreshed} horizons', request)\n        return {\"status\": \"success\", \"symbol\": symbol, \"refreshed\": refreshed}"
    )

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
