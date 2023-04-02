"""Lightweight wrapper around requests library, with async support."""
from typing import Any, Dict, Optional

import aiohttp
import requests
from pydantic import BaseModel, Extra

from chatgpt_tool_hub.tools.web_requests import DEFAULT_HEADER


class RequestsWrapper(BaseModel):
    """Lightweight wrapper around requests library."""

    headers: Optional[Dict[str, str]] = dict()
    aiosession: Optional[aiohttp.ClientSession] = None

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    def get(self, url: str, params: Dict[str, Any] = None, raise_for_status: bool = False) -> str:
        """GET the URL and return the text."""
        self.headers.update(DEFAULT_HEADER)
        response = requests.get(url, headers=self.headers, params=params)
        if raise_for_status:
            response.raise_for_status()
        return response.text

    def post(self, url: str, data: Dict[str, Any]) -> str:
        """POST to the URL and return the text."""
        self.headers = dict().update(DEFAULT_HEADER) if not self.headers else self.headers.update(DEFAULT_HEADER)
        return requests.post(url, data=data, headers=self.headers).text

    def patch(self, url: str, data: Dict[str, Any]) -> str:
        """PATCH the URL and return the text."""
        self.headers = dict().update(DEFAULT_HEADER) if not self.headers else self.headers.update(DEFAULT_HEADER)
        return requests.patch(url, json=data, headers=self.headers).text

    def put(self, url: str, data: Dict[str, Any]) -> str:
        """PUT the URL and return the text."""
        self.headers = dict().update(DEFAULT_HEADER) if not self.headers else self.headers.update(DEFAULT_HEADER)
        return requests.put(url, json=data, headers=self.headers).text

    def delete(self, url: str) -> str:
        """DELETE the URL and return the text."""
        self.headers = dict().update(DEFAULT_HEADER) if not self.headers else self.headers.update(DEFAULT_HEADER)
        return requests.delete(url, headers=self.headers).text

    async def _arequest(self, method: str, url: str, **kwargs: Any) -> str:
        """Make an async request."""
        self.headers = dict().update(DEFAULT_HEADER) if not self.headers else self.headers.update(DEFAULT_HEADER)
        if not self.aiosession:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method, url, headers=self.headers, **kwargs
                ) as response:
                    return await response.text()
        else:
            async with self.aiosession.request(
                method, url, headers=self.headers, **kwargs
            ) as response:
                return await response.text()

    async def aget(self, url: str) -> str:
        """GET the URL and return the text asynchronously."""
        return await self._arequest("GET", url)

    async def apost(self, url: str, data: Dict[str, Any]) -> str:
        """POST to the URL and return the text asynchronously."""
        return await self._arequest("POST", url, json=data)

    async def apatch(self, url: str, data: Dict[str, Any]) -> str:
        """PATCH the URL and return the text asynchronously."""
        return await self._arequest("PATCH", url, json=data)

    async def aput(self, url: str, data: Dict[str, Any]) -> str:
        """PUT the URL and return the text asynchronously."""
        return await self._arequest("PUT", url, json=data)

    async def adelete(self, url: str) -> str:
        """DELETE the URL and return the text asynchronously."""
        return await self._arequest("DELETE", url)
