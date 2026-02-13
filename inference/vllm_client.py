from typing import Dict, Any

class VLLMClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def complete(self, prompt: str) -> Dict[str, Any]:
        # TODO: call your vLLM server
        return {"text": "stub completion", "tokens": 0}
