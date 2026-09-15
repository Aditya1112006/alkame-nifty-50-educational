file_path = 'predictor.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_lines = '''    model_id: str | None = None
    code_commit: str | None = None
    data_snapshot_id: str | None = None\n'''

content = content.replace(bad_lines, '')

good_lines = '''    suppression_reasons: list[str] = field(default_factory=list)
    target_price: float | None = None
    stop_loss_price: float | None = None
    model_id: str | None = None
    code_commit: str | None = None
    data_snapshot_id: str | None = None'''

content = content.replace('    suppression_reasons: list[str] = field(default_factory=list)\n    target_price: float | None = None\n    stop_loss_price: float | None = None', good_lines)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
