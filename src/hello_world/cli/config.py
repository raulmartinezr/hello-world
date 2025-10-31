from pydantic import BaseModel
from pathlib import Path
import json

class Settings(BaseModel):
    greeting_prefix: str = "Hello"

    @classmethod
    def from_file(cls, path: str) -> "Settings":
        p = Path(path)
        data = json.loads(p.read_text(encoding="utf-8"))
        return cls(**data)

