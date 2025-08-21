from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_core import CancellationToken
from autogen_core.models import ChatCompletionClient
from pydantic import BaseModel
from typing import Dict, List, Literal
from DocManager.chatbot_backend.backend_data import ConversationMessage, ComponentStyle
from DocManager.chatbot_backend.prompt import document_assistant_prompt, query_generator_prompt
from DocManager.chatbot_backend.temp_database import TempDatabase
from DocManager.chatbot_backend.tree_components import TreeComponents
from DocManager.chatbot_backend.style_filtering import filter_default_styles
import re
import json

class ChatbotFeature:
    def __init__(self, model_client: ChatCompletionClient, small_model_client: ChatCompletionClient, temp_database: TempDatabase):
        self.temp_database = temp_database
        self.agent = AssistantAgent(
            name="document_assistant",
            model_client=model_client,
            system_message=document_assistant_prompt,
        )

        self.temp_agent = AssistantAgent(
            name="query_agent",
            model_client=small_model_client,
            system_message=query_generator_prompt
        )

    async def llm_response(self, conversation_message: ConversationMessage) -> ConversationMessage:
        if conversation_message.components:
            for component in conversation_message.components:
                if component.styles:
                    for style_name, style_values in component.styles.items():
                        component.styles[style_name] = filter_default_styles(style_values)

        html_dict = {}
        for component in conversation_message.components:
            html_dict[component.component_name] = component.html

        treeComponents = TreeComponents(conversation_message.html_content)
        conversation_message.components = treeComponents.merge_components(conversation_message.components)
        
        conversation_message.html_content = None
        message_string = conversation_message.model_dump_json(indent=2)
        print("Tool Response: ")
        print(message_string)

        response = await self.agent.run(task=message_string)

        print("Agent Response: ")
        print(response.messages[-1].content)
        print(f"tokens used : {response.messages[-1].models_usage}")

        try:
            parsed_json = json.loads(response.messages[-1].content)
            parsed_json["tag"] = "llm_response"
            parsed_json["rag_range"] = None
            parsed_json["html_content"] = None

            results = ConversationMessage(**parsed_json)

            for component in results.components:
                if component.html != None:
                    self.temp_database.delete_memory_from_html(html_dict[component.component_name], component.page)
                    self.temp_database.add_memory_from_html(component.html, component.page)

            return results
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            return ConversationMessage(
                message=f"Error: {e}" + response.messages[-1].content,
                components=None,
                tag="llm_response",
                rag_range=None,
                html_content=None
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