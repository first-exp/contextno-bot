from pydantic import BaseModel


class ContextnoSession(BaseModel):
    challenge_id: str
    chat_id: str


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