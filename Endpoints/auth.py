# import os
# from fastapi import FastAPI, HTTPException, Depends, status
# from pydantic import BaseModel
# import boto3
# import random 
# from typing import Dict
# from datetime import datetime, timedelta
# from schemas import SendOTPRequest, VerifyOTPRequest
# from dotenv import load_dotenv
# from Endpoints.log_handling import logger, log_router
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from fastapi.security import OAuth2PasswordBearer

# # Load environment variables
# load_dotenv()

# app = FastAPI()

# # Include the log configuration router
# app.include_router(log_router, tags=["logging"])

# # AWS credentials and region
# AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
# AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
# AWS_REGION = os.getenv("AWS_REGION")

# # Initialize AWS SNS client
# sns_client = boto3.client(
#     "sns",
#     aws_access_key_id=AWS_ACCESS_KEY,
#     aws_secret_access_key=AWS_SECRET_KEY,
#     region_name=AWS_REGION
# )

# logger.info("AWS SNS client initialized")

# # In-memory storage for OTPs
# otp_store: Dict[str, Dict] = {}

# # Secret key and algorithm (store these securely in production)
# SECRET_KEY = "your-secret-key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
# REFRESH_TOKEN_EXPIRE_DAYS = 7

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# class Token(BaseModel):
#     access_token: str
#     refresh_token: str
#     token_type: str

# class TokenData(BaseModel):
#     username: str | None = None

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire, "type": "access"})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# def create_refresh_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
#     to_encode.update({"exp": expire, "type": "refresh"})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     # Here you would typically get the user from the database
#     # For this example, we'll just return the username
#     return token_data.username

# # Function to validate refresh token
# def validate_refresh_token(refresh_token: str):
#     try:
#         payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         token_type: str = payload.get("type")
#         if username is None or token_type != "refresh":
#             return None
#         return username
#     except JWTError:
#         return None

# def send_sms(phone_number: str, message: str):
#     """
#     Send an SMS message using AWS SNS.
    
#     :param phone_number: The recipient's phone number
#     :param message: The message content
#     """
#     try:
#         sns_client.publish(
#             PhoneNumber=phone_number,
#             Message=message
#         )
#         logger.info(f"SMS sent to {phone_number}: {message}")
#     except Exception as e:
#         logger.error(f"Failed to send SMS to {phone_number}: {str(e)}")
#         raise

# def generate_otp():
#     """
#     Generate a random 6-digit OTP.
    
#     :return: A string containing the generated OTP
#     """
#     otp = str(random.randint(100000, 999999))
#     logger.debug(f"Generated OTP: {otp}")
#     return otp

# async def send_otp(request: SendOTPRequest):
#     otp = generate_otp()
#     otp_expiry = datetime.utcnow() + timedelta(minutes=5)  # OTP expires in 5 minutes

#     # Store the OTP and its expiry time
#     otp_store[request.phone_number] = {"otp": otp, "expiry": otp_expiry}

#     message = f"Your OTP code is {otp}. It will expire in 5 minutes."

#     try:
#         send_sms(request.phone_number, message)
#         return {"message": "OTP sent successfully"}
#     except Exception as e:
#         logger.error(f"Failed to send OTP: {str(e)}")
#         raise HTTPException(status_code=500, detail="Failed to send OTP")

# async def verify_otp(request: VerifyOTPRequest):
#     stored_otp = otp_store.get(request.phone_number)
#     if not stored_otp:
#         raise HTTPException(status_code=400, detail="No OTP found for this phone number")

#     if datetime.utcnow() > stored_otp["expiry"]:
#         del otp_store[request.phone_number]
#         raise HTTPException(status_code=400, detail="OTP has expired")

#     if request.otp != stored_otp["otp"]:
#         raise HTTPException(status_code=400, detail="Invalid OTP")

#     del otp_store[request.phone_number]
#     return {"message": "OTP verified successfully"}







