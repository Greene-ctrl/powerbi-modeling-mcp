import httpx
import os
from typing import Any, Dict, List, Optional

class ClickUpClient:
    def __init__(self, api_key: Optional[str] = None):
        # Use CLICKUP_API_TOKEN as provided by user
        self.api_key = api_key or os.getenv("CLICKUP_API_TOKEN") or os.getenv("CLICKUP_API_KEY")
        if not self.api_key:
            raise ValueError("CLICKUP_API_TOKEN must be set")
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

    async def get_tasks(self, list_id: str, archived: bool = False) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/list/{list_id}/task",
                headers=self.headers,
                params={"archived": str(archived).lower()}
            )
            response.raise_for_status()
            return response.json().get("tasks", [])

    async def get_task(self, task_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/task/{task_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def create_task(self, list_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/list/{list_id}/task",
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json()

    async def update_task(self, task_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.base_url}/task/{task_id}",
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
