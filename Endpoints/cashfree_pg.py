import os
from fastapi import APIRouter, HTTPException
from schemas import CashFreeTransactionDetails
from dotenv import load_dotenv
import json
import requests

# Loading environment variables
load_dotenv()

# FastAPI Router for Endpoint
cfpg_router = APIRouter()

XClientId = os.getenv("CLIENT_ID")
XClientSecret = os.getenv("CLIENT_SECRET_KEY")
x_api_version = os.getenv("X_API_VERSION")

@cfpg_router.post("/cashfree/createOrder")
async def create_order(details: CashFreeTransactionDetails):
    url = "https://sandbox.cashfree.com/pg/orders"
    
   
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-version": x_api_version,
        "x-client-id": XClientId,  
        "x-client-secret": XClientSecret
        }

    
    data = {
        "customer_details": {
            "customer_id": details.customer_details.customer_id,
            "customer_email": details.customer_details.customer_email,
            "customer_phone": details.customer_details.customer_phone,
            "customer_name": details.customer_details.customer_name
        },
        "order_meta": {
            "return_url": details.order_meta.return_url,
            "notify_url": details.order_meta.notify_url
            },
        "order_id": details.order_id,
        "order_amount": details.order_amount,
        "order_currency": details.order_currency,
        
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@cfpg_router.get("/cashfree/getOrder/{order_id}")
async def fetch_order(order_id: str):

    url = f"https://sandbox.cashfree.com/pg/orders/{order_id}"

    headers = {
        "accept": "application/json",
        "x-api-version": x_api_version,
        "x-client-id": XClientId,
        "x-client-secret": XClientSecret
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))