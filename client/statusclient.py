import asyncio
import aiohttp
from typing import Optional, Callable

class StatusClient:
    def __init__(self, base_url: str = "http://127.0.0.1:5000",
                 initial_delay: float = 0.1,
                 max_delay: float = 5.0,
                 backoff_factor: float = 2.0):
        self.base_url = base_url
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    async def wait_for_completion(self, task_id: str, callback: Optional[Callable] = None) -> dict:
        """
        Wait for a task to complete using exponential backoff.
        
        Args:
            task_id: The ID of the task to wait for
            callback: Optional callback function that receives status updates
        
        Returns:
            The final task status
        """
        if not self._session:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")

        current_delay = self.initial_delay
        initial_status = None

        while True:
            async with self._session.get(f"{self.base_url}/status", params={"task_id": task_id}) as response:
                # Add error handling for non-200 responses
                if response.status != 200:
                    error_text = await response.text()
                    raise RuntimeError(f"Server returned {response.status}: {error_text}")
                
                # Verify content type before parsing JSON
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' not in content_type:
                    error_text = await response.text()
                    raise RuntimeError(f"Unexpected content type '{content_type}': {error_text}")
                    
                status_data = await response.json()
                
                if callback and status_data != initial_status:
                    callback(status_data)
                initial_status = status_data

                if status_data["status"] == "completed":
                    return status_data
                
                # Exponential backoff with max delay
                await asyncio.sleep(current_delay)
                current_delay = min(current_delay * self.backoff_factor, self.max_delay)