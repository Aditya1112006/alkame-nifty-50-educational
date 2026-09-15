import sys

file_path = "api.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

audit_endpoint = '''
@app.get("/api/v1/admin/audit-logs", tags=["Admin"])
def get_audit_logs(limit: int = 50, client: ClientAuth = Depends(require_role("ADMIN"))):
    try:
        with SessionLocal() as db:
            logs = db.query(AuditLog).order_by(AuditLog.id.desc()).limit(limit).all()
            return {"status": "success", "logs": [{"id": l.id, "timestamp": l.timestamp, "action": l.action, "resource": l.resource, "status": l.status, "client_role": l.client_role, "ip_address": l.ip_address} for l in logs]}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch audit logs")
'''

if "def get_audit_logs(" not in content:
    content += audit_endpoint

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
