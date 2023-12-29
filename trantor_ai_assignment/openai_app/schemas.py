from pydantic import BaseModel, validator

class QuestionCreate(BaseModel):
    text: str

    @validator("text")
    def validate_text_length(cls, v):
        if len(v) < 10 or len(v) > 500:
            raise ValueError("Question length must be between 10 and 500 characters.")
        return v

    @validator("text")
    def validate_text_content(cls, v):
        if "spam" in v.lower():
            raise ValueError("Spam content is not allowed in questions.")
        return v

class QuestionResponse(BaseModel):
    text: str
    answer: str
