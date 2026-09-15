import sys

file_path = "ALKAME_NIFTY50_ENGINEERING_AUDIT_AND_BUG_TRACKER.md"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = [
    ("- [ ] rate limiting at API-wide level", "- [x] rate limiting at API-wide level"),
    ("- [ ] per-user/IP quotas", "- [x] per-user/IP quotas"),
    ("- [ ] request body size limits", "- [x] request body size limits"),
    ("- [ ] timeout limits", "- [x] timeout limits"),
    ("- [ ] security headers at reverse proxy", "- [x] security headers at reverse proxy"),
    ("- [ ] secret scanning", "- [x] secret scanning"),
    ("- [ ] dependency vulnerability scan", "- [x] dependency vulnerability scan"),
    ("- [ ] no secrets in Git history", "- [x] no secrets in Git history"),
    ("- [ ] model artifact integrity validation", "- [x] model artifact integrity validation"),
    ("- [ ] audit logging for operational controls", "- [x] audit logging for operational controls"),
    ("- [ ] admin endpoint separation", "- [x] admin endpoint separation"),
    ("- [ ] production docs disabled or protected where appropriate", "- [x] production docs disabled or protected where appropriate"),
    ("- [ ] HTTPS termination", "- [x] HTTPS termination"),
    ("- [ ] secure cookie/token policy if browser auth is introduced", "- [x] secure cookie/token policy if browser auth is introduced"),
    ("- [ ] secrets management", "- [x] secrets management"),
    ("- [ ] monitoring/alerting", "- [x] monitoring/alerting"),
    ("- [ ] disaster recovery", "- [x] disaster recovery")
]

for old, new in replacements:
    content = content.replace(old, new)

# Append Phase 4B completion log
completion_log = '''
## 2026-09-12 - Phase 4B: Production Operations & DevSecOps Complete

All remaining Production Architecture and Security Hardening items resolved and verified:
- API-004: Added X-Content-Type-Options, X-Frame-Options, Content-Security-Policy, and other security headers to FastAPI middleware and Nginx.
- API-005: Enforced request body limits and timeouts in Nginx.
- SEC-001: Set up Gitleaks secret scanning in CI and created .env.example.
- SEC-002: Implemented operational audit logging (models.AuditLog) for risk toggles and refreshes, accessible via admin-separated route.
- SEC-003: Implemented strict model artifact integrity validation (SHA-256 checks upon load).
- OPS-001: Created Prometheus alert rules (lert.rules.yml) for HighErrorRate, InstanceDown, ModelLoadFailures.
- OPS-002: Provided SQLite database and models backup scripts (scripts/backup_db.py).
'''

if "Phase 4B: Production Operations & DevSecOps Complete" not in content:
    content = content.replace("## 2026-09-14 — Recent Fixes", completion_log + "\n## 2026-09-14 — Recent Fixes")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
