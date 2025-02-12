from typing import Literal

import httpx

from ._internals import _handle_response
from ._utils import Result
from .exceptions import APIException
from .models import AdUnitsFetchModel


class ArcanaCodexClient:
    def __init__(self, api_key: str):
        # self.base_url = "http://api-forge.arcana.ad/api/public"
        self.base_url = "http://0.0.0.0:3281/api/public"
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
                            method, endpoint, headers={"Accept": "text/event-stream"}
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
                        response = client.get(endpoint)
                    case "POST":
                        response = client.post(endpoint, json=json_payload)
                    case "PUT":
                        response = client.put(endpoint, json=json_payload)
                    case "DELETE":
                        if json_payload is not None:
                            response = client.request(
                                method, endpoint, json=json_payload
                            )
                        else:
                            response = client.delete(endpoint)

                return _handle_response(response)

    def fetch_ad_units(self, payload: AdUnitsFetchModel):
        response = self._make_request(
            "POST",
            endpoint="/ad-units/",
            json_payload=payload.model_dump(mode="json"),
            is_streaming_request=False,
        )

        if response.error is not None:
            raise response.error

        task_id = response.value["message"]["task_id"]

        streaming_response = self._make_request(
            "GET", f"/ad-units/response/{task_id}", is_streaming_request=True
        )

        if streaming_response.error is not None:
            raise streaming_response.error

        return streaming_response.value
