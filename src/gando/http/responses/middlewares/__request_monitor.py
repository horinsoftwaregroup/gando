from typing import Any


class Monitor:
    monitor: dict = {}

    def __int__(self):
        self.monitor = {}

    def add(self, key: str, value: Any):
        self.monitor[key] = value

    def delete(self, key):
        self.monitor.pop(key, None)

    def export(self):
        return self.monitor
