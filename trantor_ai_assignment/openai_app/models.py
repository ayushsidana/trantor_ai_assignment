from sqlmodel import SQLModel, Field
from datetime import datetime

class Question(SQLModel, table=True):
    id: int = Field(primary_key=True, description="Unique identifier for the question")
    text: str = Field(
        max_length=500,
        description="The question text",
        unique=True,
    )
    answer: str = Field(max_length=1000, description="The generated answer for the question")
    created_at: datetime = Field(sa_column_kwargs={"default": datetime.utcnow()}, description="Timestamp for when the question was created")
    is_active: bool = Field(default=True, description="Whether the question is active or not")

    class Config:
        orm_mode = True

