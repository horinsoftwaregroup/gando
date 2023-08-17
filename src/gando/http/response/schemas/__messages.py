from typing import List, Dict, Optional

from pydantic import BaseModel


class Messages(BaseModel):
    log: Optional[List[Dict[str, str]]] = list()
    info: Optional[List[Dict[str, str]]] = list()
    warning: Optional[List[Dict[str, str]]] = list()
    error: Optional[List[Dict[str, str]]] = list()
    exception: Optional[List[Dict[str, str]]] = list()
