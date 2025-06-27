from typing import Literal

import httpx

from ._internals import _handle_async_response
from ._utils import Result
from .exceptions import APIException
from .models import AdUnitsFetchModel, AdUnitsIntegrateModel


class AsyncAtheonCodexClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.atheon.ad/v1",
        headers: dict[str, str] | None = None,
        **kwargs,
    ):
        if headers is None:
            headers = {}

        self.base_url = base_url
        self.headers = {
            "x-atheon-api-key": api_key,
            "Content-Type": "application/json",
            **headers,
        }
        self.kwargs = kwargs  # TODO: Come up with better name for this

    async def _make_request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE"],
        endpoint: str,
        json_payload: dict | None = None,
        is_streaming_request: bool = False,
    ):
        async with httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=httpx.Timeout(timeout=15),
            **self.kwargs,
        ) as client:
            if is_streaming_request:
                match method:
                    case "GET":
                        async with client.stream(
                            method,
                            endpoint,
                            headers={"Accept": "text/event-stream"},
                            timeout=httpx.Timeout(timeout=45),
                        ) as stream_response:
                            return await _handle_async_response(
                                stream_response, is_streaming_response=True
                            )
                    case _:
                        return Result(
                            value=None,
                            error=APIException(
                                "Streaming requests only support GET method"
                            ),
                        )
            else:
                match method:
                    case "GET":
                        response = await client.get(endpoint)
                    case "POST":
                        response = await client.post(endpoint, json=json_payload)
                    case "PUT":
                        response = await client.put(endpoint, json=json_payload)
                    case "DELETE":
                        if json_payload is not None:
                            response = await client.request(
                                method, endpoint, json=json_payload
                            )
                        else:
                            response = await client.delete(endpoint)

                return await _handle_async_response(response)

    async def fetch_ad_units(self, payload: AdUnitsFetchModel):
        response = await self._make_request(
            "POST",
            endpoint="/ad-units/fetch",
            json_payload=payload.model_dump(mode="json"),
            is_streaming_request=False,
        )

        if response.error is not None:
            raise response.error

        task_id = response.value["message"]["task_id"]

        streaming_response = await self._make_request(
            "GET", f"/ad-units/fetch/response/{task_id}", is_streaming_request=True
        )

        if streaming_response.error is not None:
            raise streaming_response.error

        return streaming_response.value

    async def integrate_ad_units(self, payload: AdUnitsIntegrateModel):
        response = await self._make_request(
            "POST",
            endpoint="/ad-units/integrate",
            json_payload=payload.model_dump(mode="json"),
            is_streaming_request=False,
        )

        if response.error is not None:
            raise response.error

        task_id = response.value["message"]["task_id"]

        streaming_response = await self._make_request(
            "GET", f"/ad-units/integrate/response/{task_id}", is_streaming_request=True
        )

        if streaming_response.error is not None:
            raise streaming_response.error

        return streaming_response.value
