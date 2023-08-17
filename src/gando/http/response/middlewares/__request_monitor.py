from typing import Any


class Monitor:
    def __int__(self):
        self.__monitor = {}

    def add(self, key: str, value: Any):
        self.__monitor[key] = value

    def delete(self, key):
        self.__monitor.pop(key, None)

    def export(self):
        return self.__monitor
