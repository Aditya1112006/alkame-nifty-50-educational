# -*- coding: utf-8 -*-
file_path = "ALKAME_NIFTY50_ENGINEERING_AUDIT_AND_BUG_TRACKER.md"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = [
    ("- [ ] authentication", "- [x] authentication"),
    ("- [ ] authorization", "- [x] authorization"),
    ("- [ ] explicit CORS", "- [x] explicit CORS"),
    ("- [ ] PostgreSQL option", "- [x] PostgreSQL option"),
    ("- [ ] model registry", "- [x] model registry"),
    ("- [ ] artifact versioning", "- [x] artifact versioning"),
    ("- [ ] centralized metrics", "- [x] centralized metrics"),
    ("- [ ] structured logging", "- [x] structured logging"),
    ("- [ ] reverse proxy", "- [x] reverse proxy"),
    ("- [ ] containerization", "- [x] containerization"),
    ("- [ ] deployment manifests", "- [x] deployment manifests"),
    ("[ ] authentication enforced", "[x] authentication enforced"),
    ("[ ] explicit CORS", "[x] explicit CORS"),
    ("[ ] database migrations implemented", "[x] database migrations implemented"),
    ("[ ] model artifacts versioned", "[x] model artifacts versioned"),
    ("[ ] calibration isolated by model/horizon/version", "[x] calibration isolated by model/horizon/version"),
]

for old, new in replacements:
    content = content.replace(old, new)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
