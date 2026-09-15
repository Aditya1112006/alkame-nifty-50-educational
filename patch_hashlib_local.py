import sys

file_path = "ensemble_manager.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace local imports that shadow the module scope
content = content.replace("joblib.dump(bundle, run_dir / \"ensemble.joblib\")\n            import hashlib\n            artifact_sha256", "joblib.dump(bundle, run_dir / \"ensemble.joblib\")\n            artifact_sha256")
content = content.replace("                    import hashlib\n                    artifact_sha256", "                    artifact_sha256")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
