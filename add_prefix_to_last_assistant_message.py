"""
title: Add Prefix to last assistant message
author: ico
author_url: https://github.com/vincentchwong
version: 0.1
"""

from pydantic import BaseModel, Field
from typing import Optional
from open_webui.utils.misc import get_last_user_message, get_last_assistant_message


class Filter:
    class Valves(BaseModel):
        prefix: str = Field(
            default="[Prefix]", description="prefix to last assistant message."
        )
        pass

    class UserValves(BaseModel):
        pass

    def __init__(self):
        # Indicates custom file handling logic. This flag helps disengage default routines in favor of custom
        # implementations, informing the WebUI to defer file-related operations to designated methods within this class.
        # Alternatively, you can remove the files directly from the body in from the inlet hook
        # self.file_handler = True

        # Initialize 'valves' with specific configurations. Using 'Valves' instance helps encapsulate settings,
        # which ensures settings are managed cohesively and not confused with operational flags like 'file_handler'.
        self.valves = self.Valves()
        pass

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # Modify or analyze the response body after processing by the API.
        # This function is the post-processor for the API, which can be used to modify the response
        # or perform additional checks and analytics.
        # print(f"outlet:{__name__}")
        # print(f"outlet:body:{body}")
        # print(f"outlet:user:{__user__}")

        print(f"*** patch last assistant message with prefix:{self.valves.prefix}")

        messages = body["messages"]
        assistant_message = get_last_assistant_message(messages)

        if assistant_message is not None:
            # Do something

            for message in reversed(messages):
                if message["role"] == "assistant":
                    message["content"] = self.valves.prefix + assistant_message
                    break

        body = {**body, "messages": messages}
        # print(f"outlet:body:{body}")
        return body
