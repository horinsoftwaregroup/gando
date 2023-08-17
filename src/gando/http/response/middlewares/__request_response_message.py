from typing import List, Dict, Optional

from pydantic import BaseModel


class MessagesSchema(BaseModel):
    log_messages: Optional[List[Dict[str, str]]] = list()
    info_messages: Optional[List[Dict[str, str]]] = list()
    warning_messages: Optional[List[Dict[str, str]]] = list()
    error_messages: Optional[List[Dict[str, str]]] = list()
    exception_messages: Optional[List[Dict[str, str]]] = list()


class ResponseMessages:
    def __int__(self):
        self.__log = []
        self.__info = []
        self.__warning = []
        self.__error = []
        self.__exception = []

    @property
    def log(self):
        return self.__log

    @property
    def info(self):
        return self.__info

    @property
    def warning(self):
        return self.__warning

    @property
    def error(self):
        return self.__error

    @property
    def exception(self):
        return self.__exception

    def add2logs(self, msg_title: str, msg_content: str):
        self.__log.append({msg_title: msg_content})

    def add2infos(self, msg_title: str, msg_content: str):
        self.__info.append({msg_title: msg_content})

    def add2warnings(self, msg_title: str, msg_content: str):
        self.__warning.append({msg_title: msg_content})

    def add2errors(self, msg_title: str, msg_content: str):
        self.__error.append({msg_title: msg_content})

    def add2exceptions(self, msg_title: str, msg_content: str):
        self.__exception.append({msg_title: msg_content})

    def export(self):
        ret = MessagesSchema(
            log_messages=self.__log,
            info_messages=self.__info,
            warning_messages=self.__warning,
            error_messages=self.__error,
            exception_messages=self.__exception,
        )
        return ret
