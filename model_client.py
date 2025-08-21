from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from autogen_core.models import ModelInfo
import os

def get_model_client():
    model_client = AnthropicChatCompletionClient(
        model="anthropic/claude-sonnet-4",
        auth_token=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL"),
        model_info=ModelInfo(
            vision=True,
            function_calling=True,
            json_output=False,
            family="unknown",
            structured_output=True,
        ),
        max_tokens=20000,
    )
    return model_client

def get_small_model_client():
    small_model_client = AnthropicChatCompletionClient(
        model="claude-3-5-haiku-20241022",
        auth_token=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL"),
        model_info=ModelInfo(
            vision=True,
            function_calling=True,
            json_output=False,
            family="unknown",
            structured_output=True,
        ),
        max_tokens=20000,
    )
    return small_model_client