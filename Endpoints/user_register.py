from fastapi import HTTPException, status, Depends, APIRouter
from sqlmodel import Session, select
from Models.user_register_model import UserRegisterMaster
from database import get_session
from schemas import UserRegisterCreate
from sqlalchemy.exc import SQLAlchemyError, DisconnectionError


user_reg_route = APIRouter()

@user_reg_route.post("/userregister", status_code=status.HTTP_201_CREATED)
async def user_master_info(usermaster: UserRegisterCreate, db: Session = Depends(get_session)):
    print(usermaster)
    try:
        existing_user = await db.exec(
                select(UserRegisterMaster).filter(
                    (UserRegisterMaster.Mobile_No == usermaster.Mobile_No) |
                    (UserRegisterMaster.Email_Address == usermaster.Email_Address)
                )
        ).first()

        if existing_user:
            if existing_user.Mobile_No == usermaster.Mobile_No:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mobile number already exists.")
            if existing_user.Email_Address == usermaster.Email_Address:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email address already exists.")


        user_data = UserRegisterMaster(**usermaster.dict())

        db.add(user_data)
        db.commit()
        db.refresh(user_data)
        return user_data

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occured")

    except DisconnectionError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Connection has lost please try again")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error occured {str(e)}")


