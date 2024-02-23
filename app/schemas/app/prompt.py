from pydantic import BaseModel


class SystemPromptCreate(BaseModel):
    content: str


class SystemPromptRead(SystemPromptCreate):
    id: int
    user_id: int
    popularity: int

    class Config:
        from_attributes = True
