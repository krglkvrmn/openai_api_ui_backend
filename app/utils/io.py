import json
from pathlib import Path
from typing import Optional


def read_oauth2_config_file(oauth2_config_file: str | Path | None) -> tuple[str | None, str | None]:
    if oauth2_config_file is None:
        return None, None
    oauth2_config_file = Path(oauth2_config_file)
    if oauth2_config_file is not None and oauth2_config_file.exists():
        config = json.loads(oauth2_config_file.read_text())
        return config.get("client_id"), config.get("client_secret")
    return None, None
