from sqlalchemy import TIMESTAMP, Column, text
from sqlmodel import SQLModel, Field
from datetime import datetime

class UserFeedback(SQLModel, table=True):

    __tablename__ = "feedback"

    USDID: int = Field(primary_key=True)
    UID:int = Field(nullable=False)
    Subject:str = Field(max_length=100, nullable=False)
    Description:str = Field(nullable=False)
    Image:str = Field(nullable=False)
    Created_at:datetime = Field(sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP")
    ))
