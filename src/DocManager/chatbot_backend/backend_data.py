from pydantic import BaseModel
from typing import Dict, List, Literal

class ComponentStyle(BaseModel):
    page: int
    component_name: str
    html: str | None
    styles: Dict[str, Dict[str, str]] | None

class ConversationMessage(BaseModel):
    components: List[ComponentStyle] | List[List[ComponentStyle]] | None
    tag: Literal["llm_call", "llm_response", "tool_call", "tool_response"]
    message: str | None
    rag_range: List[int] | None
    html_content: str | None # Not none when the tag is llm_call or tool_response