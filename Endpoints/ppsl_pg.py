from fastapi import APIRouter, HTTPException
from schemas import PpslTransactionDetails
import requests
import json
from dotenv import load_dotenv
from Paytm_Python_Checksum.paytmchecksum import PaytmChecksum


# FastAPI router for endpoint
ppslpg_router = APIRouter()

@ppslpg_router.post("/ppsl/payment_request/")
async def payment_request(details: PpslTransactionDetails):
    callbackurl = details.callbackUrl+details.orderId
    # The parameters as required by Paytm
    paytmParams = {
        "body": {
            "requestType": details.requestType,
            "mid": details.mid,
            "websiteName": details.websiteName,
            "orderId": details.orderId,
            "callbackUrl": callbackurl,
            "txnAmount": {
                "value": details.txnAmount_value,
                "currency": details.txnAmount_currency,
            },
            "userInfo": {
                "custId": details.custId,
            },
        }
    }

    # Actual Paytm merchant key
    merchant_key = details.merchant_key

    # Generate the checksum
    checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), merchant_key)

    # Add the checksum to the header
    paytmParams["head"] = {
        "signature": checksum
    }

    post_data = json.dumps(paytmParams)

    url = f"https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=LTMetr30291036236389&orderId={details.orderId}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(url, data=post_data, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            return response_data
        else:
            raise HTTPException(status_code=response.status_code, detail="Check Params")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



