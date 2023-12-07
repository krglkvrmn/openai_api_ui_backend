import enum


class Author(enum.Enum):
    user = "user"
    assistant = "assistant"
    system = "system"
    function = "function"
