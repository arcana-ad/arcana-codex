from typing import Literal

import httpx

from ._internals import _handle_response
from ._utils import Result
from .exceptions import APIException
from .models import AdUnitsFetchModel, AdUnitsIntegrateModel


class ArcanaCodexClient:
    def __init__(self, api_key: str):
        self.base_url = "http://api-forge.arcana.ad/api/public"
        self.headers = {"x-arcana-api-key": api_key, "Content-Type": "application/json"}

    def _make_request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE"],
        endpoint: str,
        json_payload: dict | None = None,
        is_streaming_request: bool = False,
    ):
        with httpx.Client(
            base_url=self.base_url,
            headers=self.headers,
            timeout=httpx.Timeout(timeout=15),
        ) as client:
            if is_streaming_request:
                match method:
                    case "GET":
                        with client.stream(
                            method,
                            endpoint,
                            headers={"Accept": "text/event-stream"},
                            timeout=httpx.Timeout(timeout=45),
                        ) as stream_response:
                            return _handle_response(
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
                        response = client.get(
                            endpoint, timeout=httpx.Timeout(timeout=15)
                        )
                    case "POST":
                        response = client.post(
                            endpoint,
                            json=json_payload,
                            timeout=httpx.Timeout(timeout=15),
                        )
                    case "PUT":
                        response = client.put(
                            endpoint,
                            json=json_payload,
                            timeout=httpx.Timeout(timeout=15),
                        )
                    case "DELETE":
                        if json_payload is not None:
                            response = client.request(
                                method,
                                endpoint,
                                json=json_payload,
                                timeout=httpx.Timeout(timeout=15),
                            )
                        else:
                            response = client.delete(
                                endpoint, timeout=httpx.Timeout(timeout=15)
                            )

                return _handle_response(response)

    def fetch_ad_units(self, payload: AdUnitsFetchModel):
        response = self._make_request(
            "POST",
            endpoint="/ad-units/fetch",
            json_payload=payload.model_dump(mode="json"),
            is_streaming_request=False,
        )

        if response.error is not None:
            raise response.error

        task_id = response.value["message"]["task_id"]

        streaming_response = self._make_request(
            "GET", f"/ad-units/fetch/response/{task_id}", is_streaming_request=True
        )

        if streaming_response.error is not None:
            raise streaming_response.error

        return streaming_response.value

    def integrate_ad_units(self, payload: AdUnitsIntegrateModel):
        response = self._make_request(
            "POST",
            endpoint="/ad-units/integrate",
            json_payload=payload.model_dump(mode="json"),
            is_streaming_request=False,
        )

        if response.error is not None:
            raise response.error

        task_id = response.value["message"]["task_id"]

        streaming_response = self._make_request(
            "GET", f"/ad-units/integrate/response/{task_id}", is_streaming_request=True
        )

        if streaming_response.error is not None:
            raise streaming_response.error

        return streaming_response.value
