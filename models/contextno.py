from pydantic import BaseModel


class ContextnoSession(BaseModel):
    challenge_id: str
    chat_id: str = None  # type: ignore

class ContextnoSessionIn(BaseModel):
    id: str
    name: str

class WordRank(BaseModel):
    completed: bool
    details: str
    error: bool
    rank: int
    tips: int
    tries: int
    word: str


class Tip(WordRank):
    pass