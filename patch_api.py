"""
patch_api.py - Restore api.py from the last clean git commit, then apply
three targeted fixes:
  1. Fix CSP header so Swagger /docs works (allow jsdelivr.net CDN)
  2. Add /healthz endpoint
  3. Remove duplicate return StreamingResponse(...) line outside a function
Run with: python patch_api.py
"""

import subprocess
import py_compile
import sys

# 1. Restore clean version from HEAD
result = subprocess.run(
    ["git", "show", "HEAD:api.py"],
    capture_output=True,
    text=True,
    encoding="utf-8",
)
if result.returncode != 0:
    raise RuntimeError("git show failed: " + result.stderr)

src = result.stdout
print("Restored api.py from HEAD: " + str(src.count("\n")) + " lines")

# 2. Fix CSP to allow Swagger UI CDN scripts
old_csp = "response.headers[\"Content-Security-Policy\"] = \"default-src 'self'; frame-ancestors 'none';\""
new_csp = (
    'response.headers["Content-Security-Policy"] = (\n'
    "        \"default-src 'self'; \"\n"
    "        \"script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; \"\n"
    "        \"style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; \"\n"
    "        \"img-src 'self' data: https://fastapi.tiangolo.com; \"\n"
    "        \"frame-ancestors 'none';\"\n"
    "    )"
)
if old_csp in src:
    src = src.replace(old_csp, new_csp)
    print("OK: CSP fixed")
else:
    print("WARN: CSP line not found - check manually")

# 3. Add /healthz endpoint after get_health (before /api/v1/symbols)
healthz_block = (
    "\n\n"
    '@app.get("/healthz", tags=["Health"], response_model=HealthResponse)\n'
    "def healthz():\n"
    '    """Kubernetes-style liveness probe - alias for /api/v1/health."""\n'
    "    return get_health()\n"
)
symbols_marker = '@app.get("/api/v1/symbols"'
if symbols_marker in src and "def healthz" not in src:
    src = src.replace(symbols_marker, healthz_block + symbols_marker, 1)
    print("OK: /healthz endpoint added")
elif "def healthz" in src:
    print("OK: /healthz already present - skipped")
else:
    print("WARN: Could not find symbols marker to insert /healthz")

# 4. Remove duplicate return StreamingResponse outside a function
dup = (
    '    return StreamingResponse(generate(), media_type="text/event-stream")\n'
    "\n"
    '    return StreamingResponse(generate(), media_type="text/event-stream")'
)
single = '    return StreamingResponse(generate(), media_type="text/event-stream")'
if dup in src:
    src = src.replace(dup, single)
    print("OK: Duplicate StreamingResponse return removed")
else:
    print("INFO: No duplicate StreamingResponse found (may already be clean)")

# 5. Add root endpoint if missing
root_route = '@app.get("/", tags=["Root"])'
if root_route not in src:
    root_block = (
        "\n\n"
        '@app.get("/", tags=["Root"])\n'
        "def read_root():\n"
        '    """Welcome endpoint."""\n'
        '    return {"message": "Welcome to Nifty50 API. Visit /docs for Swagger UI."}\n'
    )
    src = src.rstrip() + root_block
    print("OK: Root / endpoint added")
else:
    print("OK: Root / endpoint already present - skipped")

# 6. Write patched file
with open("api.py", "w", encoding="utf-8", newline="\n") as f:
    f.write(src)
print("Patched api.py written: " + str(src.count("\n")) + " lines")

# 7. Syntax check
try:
    py_compile.compile("api.py", doraise=True)
    print("Syntax check PASSED")
except py_compile.PyCompileError as e:
    print("Syntax check FAILED: " + str(e))
    sys.exit(1)
