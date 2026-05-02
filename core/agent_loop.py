import json
from core.llm_client import chat


def run(
    system_prompt: str,
    user_message: str,
    tools: list[dict],
    tool_handlers: dict[str, callable],
    history: list[dict] | None = None,
) -> str:
    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    while True:
        response = chat(messages, tools if tools else None)

        if response.tool_calls:
            messages.append({
                "role": "assistant",
                "content": response.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in response.tool_calls
                ],
            })
            for tc in response.tool_calls:
                name = tc.function.name
                args = json.loads(tc.function.arguments)
                result = tool_handlers[name](**args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": str(result),
                })
        else:
            return response.content
