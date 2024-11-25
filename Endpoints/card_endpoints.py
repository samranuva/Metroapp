from fastapi import APIRouter,HTTPException,Depends
import httpx 
import json
from Endpoints.log_handling import logger
# from Endpoints.token_handler import get_bearer_token, URL


