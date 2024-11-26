from sqlalchemy import TIMESTAMP, Column, text
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, datetime


class UserRegisterMaster(SQLModel, table=True):

    __tablename__ = "user_master"

    UID: Optional[int] = Field(default=None,primary_key=True)
    RegistrationDate: datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
            server_onupdate=text("CURRENT_TIMESTAMP")
        )
    )
    First_Name:str = Field(max_length=50, nullable=False)
    Last_Name:str = Field(max_length=50, nullable=False)
    Gender:Optional[str] = Field(max_length=1, nullable=True, default=None)
    Date_of_birth: date = Field(nullable=False)
    Mobile_No:str = Field(max_length=20, nullable=False, sa_column_kwargs={"unique": True})
    Email_Address:str = Field(max_length=20, nullable=False, sa_column_kwargs={"unique": True})
    Password:str = Field(max_length=20, nullable=False)
    User_Type: Optional[str] = Field(default=None, max_length=1, nullable=True, description="u - user, A - Agent")
    IMEI: str = Field(default="na", max_length=50)
    RegistetedBy: str = Field(default="U", max_length=1, description="0 - Self, > 0 Agent")
    Source: str = Field(default="m", max_length=1, nullable=False)
    DeviceType: Optional[str] = Field(default=None, max_length=3, nullable=True)
    ActiveStatus: str = Field(default="n", max_length=1, nullable=False)
    ModifiedDate: Optional[datetime] = Field(default=None, nullable=True)
    TransactionPin: Optional[str] = Field(default=None, max_length=10, nullable=True)
    UpdateEmail: Optional[str] = Field(default=None, max_length=200, nullable=True)
    UpdateMobileNo: Optional[str] = Field(default=None, max_length=50, nullable=True)
    UpdatePassword: Optional[str] = Field(default=None, max_length=20, nullable=True)
    Access_Token: Optional[str] = Field(default=None, max_length=45, nullable=True)
    Acc_Token_Expiry_Date: Optional[datetime] = Field(default=None, nullable=True)
    Last_Login_Time: Optional[datetime] = Field(default=None, nullable=True)
    Device_Info: Optional[str] = Field(default=None, max_length=300, nullable=True)
    Email_Update: Optional[str] = Field(default=None, max_length=1, nullable=True, description="Y for Yes, N for No")
    Mob_Update: Optional[str] = Field(default=None, max_length=1, nullable=True, description="Y for Yes, N for No")
    Password_Update: Optional[str] = Field(default=None, max_length=1, nullable=True, description="Y for Yes, N for No")
    Alt_EmailId: Optional[str] = Field(default=None, nullable=True, max_length=200)
    Device_Token: Optional[str] = Field(default=None, nullable=True, max_length=200)

