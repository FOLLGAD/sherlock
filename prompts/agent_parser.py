from typing import Any
from langchain.agents.conversational_chat.base import (
    AgentOutputParser,
)
from prompts.prompt import (
    FORMAT_INSTRUCTIONS,
)


class SherlockOutputParser(AgentOutputParser):
    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> Any:
        cleaned_output = text.strip().splitlines()
        if len(cleaned_output) < 2:
            return {"action": "Final Answer", "action_input": text}

        if "yes" in cleaned_output[0].lower():
            tool = cleaned_output[1].replace("Which tool should I use?", "", 1).strip()
            tool_action = "\n".join(cleaned_output[2:]).replace("Input:", "", 1).strip()
            return {"action": tool, "action_input": tool_action}
        elif cleaned_output[1].lower().startswith("response"):
            return {
                "action": "Final Answer",
                "action_input": "\n".join(cleaned_output[1:])
                .replace("Response:", "", 1)
                .strip(),
            }
        elif cleaned_output[2].lower().startswith("response"):
            return {
                "action": "Final Answer",
                "action_input": "\n".join(cleaned_output[2:])
                .replace("Response:", "", 1)
                .strip(),
            }
        else:
            return {
                "action": "Final Answer",
                "action_input": "\n".join(cleaned_output),
            }
