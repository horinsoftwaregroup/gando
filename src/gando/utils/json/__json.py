from typing import Any
import json

from .encoders import Encoder


class JSON:

    @staticmethod
    def loads(value: str) -> Any:
        return json.loads(value)

    @staticmethod
    def dumps(value: Any) -> str:
        return json.dumps(value, cls=Encoder)
