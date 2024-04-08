from typing import Optional, Any, Dict, List
from pydantic import BaseModel
import asyncio
import httpx
import time

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
PATCH = 'PATCH'
DELETE = 'DELETE'
HEAD = 'HEAD'
OPTIONS = 'OPTIONS'
TRACE = 'TRACE'


class RequestSchema(BaseModel):
    idx: int
    url: str
    method: str = GET
    data: dict = {}
    cookies: dict = {}
    headers: dict = {}
    sch: Any


class RequestListSchema(BaseModel):
    items: List[RequestSchema] = []


class ResponseSchema(BaseModel):
    idx: int
    request: RequestSchema
    _response: Any
    status_code: int
    data: Any


class ResponseListSchema(BaseModel):
    items: List[ResponseSchema] = []
    elapsed_time: Optional[float] = 0


class AsyncoRequestManager:
    def __init__(self):
        self.__requests: RequestListSchema = RequestListSchema(items=[])
        self.__request_id_counter: int = 0
        self.__elapsed_time: float = 0
        self.__responses: ResponseListSchema = ResponseListSchema()
        self.__incomplete_requests: Dict[int, RequestSchema] = {}
        self.__incomplete_requests_temporary: Dict[int, RequestSchema] = {}

    def __add_to_incomplete_requests(self, item: RequestSchema):
        self.__incomplete_requests[item.idx] = item
        self.__incomplete_requests_temporary[item.idx] = item

    def __remove_from_incomplete_requests_temporary(self, item: RequestSchema):
        if item.idx in self.__incomplete_requests_temporary:
            del self.__incomplete_requests_temporary[item.idx]

    def __reset_incomplete_requests(self):
        self.__incomplete_requests = self.__incomplete_requests_temporary.copy()

    def add_to_requests(
        self, url, method=None, data=None, headers=None, cookies=None, schema=None):
        idx = self.__request_id_counter

        req = RequestSchema(
            idx=idx,
            url=url,
            method=method or GET,
            data=data or {},
            cookies=cookies or {},
            headers=headers or {},
            sch=schema,
        )

        self.__requests = req
        self.__add_to_incomplete_requests(req)

        self.__request_id_counter += 1
        return idx

    def __add_to_responses(self, request: RequestSchema, _response):
        idx = request.idx
        status_code = _response.status_code
        data = request.sch(**_response.json()) if request.sch else _response.json()

        rsp = ResponseSchema(
            idx=idx,
            request=request,
            _response=_response,
            status_code=status_code,
            data=data,
        )

        self.__responses.items.append(rsp)

        self.__remove_from_incomplete_requests_temporary(request)

        return idx

    async def __asyncio_request(self, client, request: RequestSchema):
        ret = False
        try:
            if request.method.upper() == GET:
                rsp = await client.get(
                    request.url,
                    cookies=request.cookies or {},
                    headers=request.headers or {}
                )
                self.__add_to_responses(request=request, _response=rsp)
                ret = True

            elif request.method.upper() == POST:
                rsp = await client.post(
                    request.url,
                    data=request.data,
                    cookies=request.cookies or {},
                    headers=request.headers or {},
                )
                self.__add_to_responses(request=request, _response=rsp)
                ret = True
            else:
                raise Exception("method not define.")
        except:
            pass
        finally:
            return ret

    def __is_completed(self):
        ret = False
        if len(self.__incomplete_requests) == 0:
            ret = True
        return ret

    async def __engine(self):
        async with httpx.AsyncClient() as client:
            await asyncio.gather(
                *[
                    self.__asyncio_request(client, i)
                    for i in self.__incomplete_requests.values()
                ]
            )
        self.__reset_incomplete_requests()

    def start(self):
        start_time = time.perf_counter()
        __stopper = 0
        while True:
            __stopper += 1
            if __stopper > 5:
                break
            if self.__is_completed():
                break
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.__engine())

        end_time = time.perf_counter()
        self.__responses.elapsed_time = end_time - start_time
        return self

    def export(self):
        _sort_response = self.__responses.copy()
        _sort_response.items = sorted(self.__responses.items, key=lambda item: item.idx)
        return _sort_response
