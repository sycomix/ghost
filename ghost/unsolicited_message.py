from textwrap import dedent

from langchain import OpenAI
from langchain.agents.agent import AgentExecutor

from utils import format_prompt_components_without_tools


def _extract_first_message(message: str) -> str:
    """The LLM can continue the conversation from the recipient. So extract just the first line."""

    return message.split("\n")[0]


def get_unsolicited_message_prompt(ai_prefix: str, human_prefix: str) -> str:
    """Get prompt for unsolicited message."""
    inspirational_thought = f"""
    *{ai_prefix} then drew on their past experiences with {human_prefix} and continued the conversation*"""

    return dedent(inspirational_thought)


def generate_unsolicited_message(
    prompt: str,
    agent: AgentExecutor,
    ai_settings: dict,
    contact_settings: dict,
    temperature: int = 0,
) -> str:
    """Generate AI message without message from user."""

    ai_prefix, _, prefix, suffix = format_prompt_components_without_tools(
        ai_settings, contact_settings
    )

    prompt = "\n".join([prefix, suffix, prompt, "", f"{ai_prefix}:"]).format(
        chat_history=agent.memory.buffer
    )
    llm = OpenAI(temperature=temperature)
    message = llm(prompt)
    message = _extract_first_message(message)

    agent.memory.chat_memory.add_ai_message(message)

    return message
