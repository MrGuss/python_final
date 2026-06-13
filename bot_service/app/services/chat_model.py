from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: str


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: list[ChatChoice]
    usage: Usage
    system_fingerprint: str | None
