from fastapi import HTTPException, status, Depends, APIRouter
from sqlmodel import Session, select
from Models.user_register_model import UserRegisterMaster
from database import get_session
from schemas import SaveUpdatedPassword, UserRegisterCreate, UserValidate
from sqlalchemy.exc import SQLAlchemyError, DisconnectionError


user_reg_route = APIRouter()

@user_reg_route.post("/userregister/", status_code=status.HTTP_201_CREATED)
async def user_master_info(usermaster: UserRegisterCreate, db: Session = Depends(get_session)):
    print(usermaster)
    try:
        existing_user = db.exec(
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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong unable to save")

    except DisconnectionError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Connection has lost please try again")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error occured {str(e)}")


@user_reg_route.post("/userlogin/")
async def user_login(user: UserValidate, db: Session = Depends(get_session)):
    try:
        print(user.model_dump())
        query = select(UserRegisterMaster).where(UserRegisterMaster.Mobile_No == user.Mobile_No, UserRegisterMaster.Password == user.Password)
        user_data = db.exec(query).first()

        user_mobile_no = db.exec(select(UserRegisterMaster).where(UserRegisterMaster.Mobile_No == user.Mobile_No)).first()
        
        if not user_mobile_no:
            return {"message": "You mobile number is not registered please sign up"}

        if not user_data:
            return {"message": "Invalid mobile number or pin"}

        return {"message": "User validation successful"}

    except Exception as e:
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occured")


@user_reg_route.patch("/resetpassword/", status_code=status.HTTP_200_OK)
async def update_password(get_password: SaveUpdatedPassword, db: Session = Depends(get_session)):
    try:
        user_mobile_no = select(UserRegisterMaster).where(UserRegisterMaster.Mobile_No == get_password.Mobile_No)
        user = db.exec(user_mobile_no).first()

        if not user:
            return {"message": "Mobile number does not exists, please register"}

        user.UpdatePassword = get_password.UpdatePassword

        db.commit()
        db.refresh(user)

        return {"message": "PIN updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
