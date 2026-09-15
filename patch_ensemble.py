import sys

file_path = "ensemble_manager.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update save_ensemble to calculate hash of bundle
if 'artifact_sha256 = hashlib.sha256(open(run_dir / "ensemble.joblib", "rb").read()).hexdigest()' not in content:
    content = content.replace(
        'joblib.dump(bundle, run_dir / "ensemble.joblib")',
        'joblib.dump(bundle, run_dir / "ensemble.joblib")\n            import hashlib\n            artifact_sha256 = hashlib.sha256(open(run_dir / "ensemble.joblib", "rb").read()).hexdigest()',
    )
    content = content.replace(
        '"feature_schema_hash": schema_hash,',
        '"feature_schema_hash": schema_hash,\n                "artifact_sha256": artifact_sha256,',
    )

# 2. Update load_ensemble to verify hash
if 'artifact_sha256 = metadata.get("artifact_sha256")' not in content:
    load_code = """                    import hashlib
                    artifact_sha256 = metadata.get("artifact_sha256")
                    if artifact_sha256:
                        current_hash = hashlib.sha256(open(ensemble_file, "rb").read()).hexdigest()
                        if current_hash != artifact_sha256:
                            logger.error(f"Integrity failure! Model {curr_run_id} checksum mismatch.")
                            raise ValueError(f"Artifact integrity failure for {symbol} ({horizon})")
                    bundle = joblib.load(ensemble_file)"""
    content = content.replace("                    bundle = joblib.load(ensemble_file)", load_code)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
