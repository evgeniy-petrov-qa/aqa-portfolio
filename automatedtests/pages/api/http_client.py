import json
import logging
from enum import Enum
from typing import Any

import requests
from pydantic import ValidationError
from requests import Response, ReadTimeout
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from automatedtests.pages.api.api_registry import api_registry

logger = logging.getLogger(__name__)


class HttpMethod(str, Enum):

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

    @classmethod
    def _missing_(cls, value: object) -> None:
        valid = [m.value for m in cls]
        raise ValueError(f"Invalid HTTP method '{value}'. Allowed values: {valid}")


class API:
    """
    Base HTTP client for API tests.

    Wraps requests.Session with support for:
    - automatic retries on network errors (Retry)
    - response status code validation
    - request/response body validation via Pydantic models from api_registry
    - detailed request and error logging
    """

    def __init__(self, timeout: int = 60) -> None:
        """
        :param timeout: Response timeout in seconds (default 60).
        """
        self.timeout = timeout
        self.session = requests.Session()

        retries = Retry(
            total=3,
            backoff_factor=1,  # delays between retries: 1s → 2s → 4s
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST", "PATCH"],
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def make_request(
        self,
        url: str,
        expected_status_code: int = 200,
        registry_key: str = "",
        method: HttpMethod | None = None,
        body: Any = None,
        params: Any = None,
        headers: dict | None = None,
        validate_status: bool = True,
        validate_response: bool = True,
        validate_request: bool = False,
    ) -> Response:
        """
        Executes an HTTP request and returns the response.

        :param url: Endpoint URL.
        :param expected_status_code: Expected response status code.
        :param registry_key: Key in api_registry for looking up Pydantic models.
        :param method: HTTP method from HttpMethod enum. If not provided — taken from api_registry.
        :param body: Request body (serialized to JSON).
        :param params: Query parameters.
        :param headers: Request headers.
        :param validate_status: Validate response status code (default True).
        :param validate_response: Validate response body via Pydantic (default True).
        :param validate_request: Validate request body via Pydantic (default False).
        :return: Response object.
        :raises ReadTimeout: If response timeout is exceeded.
        :raises ValueError: If an unknown HTTP method is provided.
        """
        if method is None:
            method = HttpMethod(api_registry[registry_key]['method'])
        logger.info("Request %s %s | params: %s | body: %s", method.value, url, params, body)

        request_kwargs = dict(
            url=url,
            params=params,
            headers=headers,
            timeout=self.timeout,
        )

        try:
            if method == HttpMethod.GET:
                response = self.session.get(**request_kwargs)
            elif method == HttpMethod.POST:
                response = self.session.post(**request_kwargs, json=body)
            elif method == HttpMethod.PUT:
                response = self.session.put(**request_kwargs, json=body)
            elif method == HttpMethod.PATCH:
                response = self.session.patch(**request_kwargs, json=body)
            elif method == HttpMethod.DELETE:
                response = self.session.delete(**request_kwargs, json=body)
            else:
                raise ValueError(f"Unknown HTTP method: {method}")

        except ReadTimeout:
            raise ReadTimeout(
                f"Response timeout exceeded: {self.timeout}s | URL: {url}"
            )

        logger.info(
            "Response %s %s | status: %s", method.value, url, response.status_code
        )

        if validate_status:
            self._validate_status(response, expected_status_code)

        if validate_request and registry_key and api_registry[registry_key].get("request_model"):
            self._validate_request_body(response, registry_key)

        if validate_response and registry_key:
            self._validate_response_body(response, registry_key)

        return response

    def _validate_status(self, response: Response, expected_status_code: int) -> None:
        """
        Validates response status code against the expected value.

        :param response: Response object.
        :param expected_status_code: Expected status code.
        :raises AssertionError: If status code does not match expected.
        """
        actual = response.status_code
        content_type = response.headers.get("content-type", "")

        if "application/json" in content_type:
            try:
                body = response.json()
            except ValueError:
                body = response.text
        else:
            body = response.text

        assert actual == expected_status_code, AssertionError(
            self._format_error(
                url=response.url,
                status=actual,
                request_body=response.request.body,
                response_body=body,
            )
        )

    def _validate_request_body(self, response: Response, registry_key: str) -> None:
        """
        Validates request body against the Pydantic model from api_registry.

        :param response: Response object (contains the original request).
        :param registry_key: Method key in api_registry.
        :raises Exception: If request body does not match the schema.
        """
        try:
            raw_body = response.request.body
            payload = json.loads(raw_body.decode("utf-8") if isinstance(raw_body, bytes) else raw_body)
            api_registry[registry_key]["request_model"].model_validate(payload)
        except ValidationError as exc:
            raise Exception(
                self._format_error(
                    url=response.url,
                    status=response.status_code,
                    request_body=response.request.body,
                    response_body=response.json(),
                    error=exc.json(),
                )
            )

    def _validate_response_body(self, response: Response, registry_key: str) -> None:
        """
        Validates response body against the Pydantic model from api_registry.

        :param response: Response object.
        :param registry_key: Method key in api_registry.
        :raises Exception: If response body does not match the schema.
        """
        content_type = response.headers.get("content-type", "")
        if "application/json" not in content_type:
            raise Exception(
                self._format_error(
                    url=response.url,
                    status=response.status_code,
                    request_body=response.request.body,
                    response_body=response.text,
                    error=f"Expected JSON response, got Content-Type: '{content_type}'",
                )
            )

        body = response.json()
        try:
            api_registry[registry_key]["model"].model_validate(body)
        except ValidationError as exc:
            raise Exception(
                self._format_error(
                    url=response.url,
                    status=response.status_code,
                    request_body=response.request.body,
                    response_body=body,
                    error=exc.json(),
                )
            )

    @staticmethod
    def _format_error(
        url: str,
        status: int,
        request_body: Any = None,
        response_body: Any = None,
        error: Any = None,
    ) -> str:
        """
        Formats a readable error message for logging and exceptions.

        :param url: Request URL.
        :param status: Response status code.
        :param request_body: Request body.
        :param response_body: Response body.
        :param error: Validation error text.
        :return: Formatted error string.
        """
        parts = [f"URL: {url}", f"Status: {status}"]
        if request_body:
            parts.append(f"Request: {request_body}")
        if response_body:
            parts.append(f"Response: {response_body}")
        if error:
            parts.append(f"Error: {error}")
        return " | ".join(parts)

    def __repr__(self) -> str:
        return f"API(timeout={self.timeout})"