import base64,os
from fastapi import HTTPException, status, Depends, APIRouter
from sqlmodel import Session, select
from Models.user_feedback_model import UserFeedback
from database import get_session
from schemas import UserFeedbackCreate, UserFeedbackItemResponse, UserFeedbackResponse


feedback_router = APIRouter()

@feedback_router.post("/feedback", status_code=status.HTTP_201_CREATED)
async def get_feedback(feedback_data: UserFeedbackCreate, db: Session = Depends(get_session)):

    try:
        image_name = feedback_data.Image["name"]
        base64_image = feedback_data.Image["content"]
        
        image_data = base64.b64decode(base64_image)

        folder_path = "D:/shivat/Metroapp/app/images"

        image_path = os.path.join(folder_path, image_name)
        
        with open(image_path, "wb") as file:
            file.write(image_data)

        image_url = f"http://localhost:8000/images/{image_name}"

        feedback_data.Image = image_url
        
        feedback = UserFeedback(**feedback_data.model_dump())
        
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
        return feedback

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Something went wrong {str(e)}")

@feedback_router.get("/feedbackinfo", status_code=status.HTTP_200_OK, response_model=list[UserFeedbackResponse])
async def get_feedback_data(db: Session = Depends(get_session)):
    try:

        feedback = db.exec(select(UserFeedback)).all()

        if feedback is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No feedback is found")
        
        return feedback

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(e)}")

@feedback_router.get("/feedback/{uid}", status_code=status.HTTP_200_OK, response_model=UserFeedbackItemResponse)
async def get_feedback_by_uid(uid:int, db: Session = Depends(get_session)):
    try:
        user_uid = db.exec(select(UserFeedback).where(UserFeedback.UID == uid)).first()

        if not user_uid:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found with the id")
        
        return user_uid
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(e)}")
