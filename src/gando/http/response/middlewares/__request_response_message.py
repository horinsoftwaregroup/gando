from typing import List, Dict, Optional

from pydantic import BaseModel


class MessagesSchema(BaseModel):
    log_messages: Optional[List[Dict[str, str]]] = list()
    info_messages: Optional[List[Dict[str, str]]] = list()
    warning_messages: Optional[List[Dict[str, str]]] = list()
    error_messages: Optional[List[Dict[str, str]]] = list()
    exception_messages: Optional[List[Dict[str, str]]] = list()


class ResponseMessages:
    log: list = []
    info: list = []
    warning: list = []
    error: list = []
    exception: list = []

    def __int__(self):
        self.log = []
        self.info = []
        self.warning = []
        self.error = []
        self.exception = []

    def add2logs(self, msg_title: str, msg_content: str):
        self.log.append({msg_title: msg_content})

    def add2infos(self, msg_title: str, msg_content: str):
        self.info.append({msg_title: msg_content})

    def add2warnings(self, msg_title: str, msg_content: str):
        self.warning.append({msg_title: msg_content})

    def add2errors(self, msg_title: str, msg_content: str):
        self.error.append({msg_title: msg_content})

    def add2exceptions(self, msg_title: str, msg_content: str):
        self.exception.append({msg_title: msg_content})

    def export(self):
        ret = MessagesSchema(
            log_messages=self.log,
            info_messages=self.info,
            warning_messages=self.warning,
            error_messages=self.error,
            exception_messages=self.exception,
        )
        return ret
