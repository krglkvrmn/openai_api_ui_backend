from pydantic import BaseModel


class SystemPromptCreate(BaseModel):
    content: str
    popularity: int


class SystemPrompt(SystemPromptCreate):
    id: int

    class Config:
        from_attributes = True


SystemPromptResponse = SystemPromptCreate
