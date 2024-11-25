import os
from fastapi import HTTPException,Depends
import httpx
from datetime import datetime, timedelta
from Endpoints.log_handling import logger
from dotenv import load_dotenv
import json

load_dotenv('config.env')


# Metro  API details
URL_TAG = os.getenv("URL_TAG")
UAT_API_URL = os.getenv("BASE_URL_UAT")
PROD_API_URL = os.getenv("BASE_URL_PROD")

# Load generate token credentials
username = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
grant_type  = os.getenv("GRANT_TYPE")
merchant_id = os.getenv("MERCHANT_ID")

payload = {"username":username,"password":password,"grant_type":grant_type,"merchant_id":merchant_id}

json_payload = json.dumps(payload)

# Global variables for token management
bearer_token = None
token_expiration = None

if URL_TAG == "UAT":
    URL = f'{UAT_API_URL}/api/v3'
    TOKEN_URL = f'{UAT_API_URL}/api/connect/token'
    
else:
    URL = PROD_API_URL
    TOKEN_URL = f'{PROD_API_URL}/api/connect/token'
    

async def get_bearer_token():
    global bearer_token, token_expiration


    # Checking token validation 
    if bearer_token and token_expiration and datetime.now() < token_expiration:
        logger.info("Using cached bearer token")
        return bearer_token
    
   
    logger.info("Fetching new token")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                TOKEN_URL,
                headers = {"Content-Type": "application/json"},
                data=json_payload)
                
        if response.status_code == 200:
            token_data = response.json()
            bearer_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 3600)
            token_expiration = datetime.now() + timedelta(seconds=expires_in)
            logger.info(f"New token fetched. Expires in {expires_in} seconds.")
            return bearer_token
        else:
            logger.error(f"Failed to fetch token: {response.status_code}")
            raise HTTPException(status_code=500, detail="Failed to fetch token from Metro service url")
    
    except Exception as e:
        logger.error(f"Error fetching token: {e}")
        raise HTTPException(status_code=500, detail="Error fetching token")

# Common token handler dependency

async def token_handler():
    token = await get_bearer_token()
    return token


