from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_core import CancellationToken
from autogen_core.models import ChatCompletionClient
from pydantic import BaseModel
from typing import Dict, List, Literal
from DocManager.chatbot_backend.prompt import document_assistant_prompt
from DocManager.chatbot_backend.temp_database import TempDatabase
import re
import json


class ComponentStyle(BaseModel):
    page: int
    component_name: str
    html: str | None
    styles: Dict[str, Dict[str, str]] | None


class ConversationMessage(BaseModel):
    components: List[ComponentStyle] | None
    tag: Literal["llm_call", "llm_response", "tool_call", "tool_response"]
    message: str | None
    rag_range: List[int] | None


class ChatbotFeature:
    def __init__(self, model_client: ChatCompletionClient, temp_database: TempDatabase):
        self.model_client = model_client
        self.temp_database = temp_database
        self.agent = AssistantAgent(
            name="document_assistant",
            model_client=model_client,
            system_message=document_assistant_prompt,
        )

        self.temp_agent = AssistantAgent(
            name="query_agent",
            model_client=model_client,
            system_message="""
            You will receive the user instruction. You have to generate the query to search information from the database.

            For example, Change the color of the paragraph about "women in senior leadership" to blue.
            Response: women in senior leadership
            Example of wrong response: "blue", "color of the paragraph"

            You can use some common sense to decide the query. The instruction will be like retrieval some part of data and edit that part. So some style editing should not be the query, instead you should query the content of the data.
            Just give me only the query context, no other text.
            """
        )

    async def llm_response(self, conversation_message: ConversationMessage) -> ConversationMessage:
        if conversation_message.components:
            for component in conversation_message.components:
                if component.styles:
                    for style_name, style_values in component.styles.items():
                        component.styles[style_name] = self.filter_default_styles(style_values)

        message_string = conversation_message.model_dump_json(indent=2)
        print("Tool Response: ")
        print(message_string)

        response = await self.agent.run(task=message_string)

        print("Agent Response: ")
        print(response.messages[-1].content)
        print(f"tokens used : {response.messages[-1].models_usage}")

        try:
            parsed_json = json.loads(response.messages[-1].content)
            results = ConversationMessage(**parsed_json)

            for component in results.components:
                if component.html != None and component.html.strip() != "":
                    self.temp_database.delete_memory_from_html(component.html, component.page)
                    self.temp_database.add_memory_from_html(component.html, component.page)

            return results
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            return ConversationMessage(
                message=f"Error: {e}" + response.messages[-1].content,
                components=None,
                tag="llm_response",
                rag_range=None
            )


    async def tool_call(self, conversation_message: ConversationMessage) -> ConversationMessage:
        query = await self.temp_agent.run(task=conversation_message.message)
        message = query.messages[-1].content
        print("Query: ")
        print(message)

        conversation_message.tag = "tool_call"
        search_result = self.temp_database.query_memory(message, conversation_message.rag_range)
        if conversation_message.components is None:
            conversation_message.components = []
        for result in search_result:
            conversation_message.components.append(ComponentStyle(
                page=result["page"],
                component_name=result["class_name"],
                html=None,
                styles=None
            ))
        print("Tool Call: ")
        print(conversation_message.model_dump_json(indent=2))
        return conversation_message

    async def chat(self, conversation_message: ConversationMessage) -> ConversationMessage:
        if conversation_message.tag == "llm_call" and conversation_message.rag_range is not None:
            return await self.tool_call(conversation_message)
        else:
            return await self.llm_response(conversation_message)

    def filter_default_styles(self, style_values: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, str]]:
        
        default_values = {
            'auto', 'none', 'normal', 'initial', 'inherit', 'unset',
            '0', '0px', '0s', '0%', '0deg',
            'transparent', 'rgba(0, 0, 0, 0)', 'rgb(0, 0, 0)',
            'visible', 'static', 'start', 'baseline', 'stretch',
            'repeat', 'scroll', 'border-box', 'ease', 'running',
            'replace', '1', '100%', 'fill', 'butt', 'miter',
            'horizontal-tb', 'ltr', 'wrap', 'collapse', 'isolate',
            'slice', 'show', 'disc', 'outside', 'clip', 'economy',
            'over', 'space-around', 'luminance', 'add', 'match-source',
            'numeric-only', 'manual', 'from-image', 'srgb', 'linearrgb',
            'nonzero', 'separate', 'row', 'nowrap', 'fixed', 'no-limit',
            'logical',
        }

        default_properties = {
            'corner-bottom-left-shape', 'corner-bottom-right-shape',
            'corner-end-end-shape', 'corner-end-start-shape',
            'corner-start-end-shape', 'corner-start-start-shape',
            'corner-top-left-shape', 'corner-top-right-shape',

            'perspective-origin', 'transform-origin', 'outline-color',
            'outline-offset', 'outline-style', 'outline-width',
            'lighting-color', 'object-position', 'offset-rotate',
            'orphans', 'widows', 'tab-size', 'stroke-miterlimit',
            'stroke-width', 'scroll-timeline-axis', 'view-timeline-axis',
            'position-visibility', 'transform-style', 'transition-property',
        }
        
        # skip browser default values and webkit internal properties
        return {prop: value for prop, value in style_values.items() if value not in default_values and not prop.startswith("-") and prop not in default_properties}