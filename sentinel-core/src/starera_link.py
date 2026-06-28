# starera_link.py – bridge to external AI services (Microsoft Copilot, etc.)

import aiohttp
import asyncio
from typing import Optional

class CopilotBridge:
    """
    A bridge that sends prompts to Microsoft Copilot (or a mock for testing).
    """
    def __init__(self, bearer_token: Optional[str] = None, conversation_id: Optional[str] = None):
        self.bearer_token = bearer_token
        self.conversation_id = conversation_id
        self.api_url = None
        if bearer_token and conversation_id:
            self.api_url = f"https://graph.microsoft.com/beta/copilot/conversations/{conversation_id}/chat"

    async def send_prompt(self, prompt: str, location_hint: str = "en-US") -> Optional[str]:
        """Send a prompt to Copilot API. Returns the assistant's reply."""
        if not self.api_url:
            # Mock response for testing (since real API needs authentication)
            return f"[MOCK] Copilot would respond to: {prompt}"
        headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "message": {"role": "user", "content": prompt},
            "locationHint": location_hint
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, headers=headers, json=payload) as resp:
                    if resp.status != 200:
                        return f"[Error] Status {resp.status}"
                    data = await resp.json()
                    return data.get("messages", [{}])[-1].get("content", "")
        except Exception as e:
            return f"[Exception] {e}"

# For synchronous usage (if needed)
def sync_send_prompt(prompt: str) -> str:
    bridge = CopilotBridge()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(bridge.send_prompt(prompt))
    loop.close()
    return result
