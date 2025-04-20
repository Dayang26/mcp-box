# app/models/types.py
from typing import List, Optional

from pydantic import BaseModel, Field


class LaunchConfig(BaseModel):
    command: str = Field(..., examples=["npx"])
    args: List[str] = Field(
        examples=[
            "-y",
            "@modelcontextprotocol/server-filesystem",
            "/Users/aaronhu/PycharmProjects/mcp-box"
        ]
    )
    port: Optional[int] = Field(
        default=None,
        examples=[8001],
        ge=1024,
        le=65535
    )
