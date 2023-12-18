from pydantic import BaseModel


class SystemPromptCreate(BaseModel):
    content: str
    popularity: int


class SystemPromptRead(SystemPromptCreate):
    id: int

    class Config:
        from_attributes = True


SystemPromptResponse = SystemPromptRead
