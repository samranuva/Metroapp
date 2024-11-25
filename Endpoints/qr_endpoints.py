from fastapi import APIRouter,HTTPException,Depends
import httpx 
import json
from Endpoints.log_handling import logger
from Endpoints.token_handler import get_bearer_token, URL
from schemas import GetFarePayload, GetTicketRequestPayload, GetStationsByzonePayload, TokenPayload, \
                    GetTicketTypesPayload, GetTicketDetailsByIdPayload, ChangeDestinationPreviewPayload, ChangeDestinationPayload, \
                    TicketUsedStatusPayload, GetTicketDetailsByPhoneMerchantIdPayload, RefundPayload, GetOrderStatusByMerchantOrderIdPayload, \
                    RefundOnRequestByMerchantPayload, ChangePasswordPayload
                    


# FastAPI router for endpoint
qr_router = APIRouter()

# Endpoint - Get Token
@qr_router.get("/getToken")
async def get_token():
    token = await get_bearer_token()
    return {"access_token": token}

# Endpoint - Get Business Operation Date Hour
@qr_router.post("/getBusinessOperationDateHour")
async def get_business_operation_date_hour(payload: TokenPayload):

    token = payload.token

    try:
        async with httpx.AsyncClient() as client:

            response =  await client.get(
                url = f'{URL}/Operation/GetBusinessOperationDateHour',
                headers={"Authorization": f"Bearer {token}"}
            )
        
        if response.status_code == 200:
            logger.info("Successfully fetched data from external server.")
            return response.json()
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint - Get Business Name
@qr_router.post("/getBusinessName")
async def get_business_name(payload: TokenPayload):

    token = payload.token

    try:
        async with httpx.AsyncClient() as client:

            response =  await client.get(
                url = f'{URL}/Operation/GetBusinessName',
                headers={"Authorization": f"Bearer {token}"}
            )
        
        if response.status_code == 200:
            logger.info("Successfully fetched data from external server.")
            return response.json()
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    
# Endpoint - Get Stations
@qr_router.post("/getStations")
async def get_station_list(payload: TokenPayload):

    token = payload.token

    try:
        async with httpx.AsyncClient() as client:

            response =  await client.get(
                url = f'{URL}/Stations/getStations',
                headers={"Authorization": f"Bearer {token}"}
            )

        station_list = response.json()

        dict_list = station_list["stations"]
                
        for d in dict_list:
            if d['corridorId'] == 1:
                d["corridorColor"] = 'Red'
            elif d['corridorId'] == 2:
                d["corridorColor"] = 'Green'
            else:
                d["corridorColor"] = 'Blue'

        
        if response.status_code == 200:
            logger.info("Successfully fetched data from external server.")
            return station_list
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint - Get Stations by Zone
@qr_router.post("/getStationsByZone")
async def get_stations_by_zone (payload : GetStationsByzonePayload):

    token = payload.token
    fromStationId = payload.fromStationId
    zoneNumber = payload.zoneNumber
    
    try:
        async with httpx.AsyncClient() as client:

            response =  await client.get(
                url = f'{URL}/Stations/getStationsbyzone',
                headers={"Authorization": f"Bearer {token}"},
                params= {"fromStationId": fromStationId,"zoneNumber":zoneNumber}
            )
        
        if response.status_code == 200:
            logger.info("Successfully fetched data from external server.")
            return response.json()
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

# Endpoint - Get Ticket Types
@qr_router.post("/getTicketTypes")
async def get_ticket_types (payload: GetTicketTypesPayload):
    
    token = payload.token
    merchantId = payload.merchantId

    try:
        async with httpx.AsyncClient() as client:

            response =  await client.get(
                url = f'{URL}/Tickets/GetTicketTypes',
                headers={"Authorization": f"Bearer {token}"},
                params= {"merchantId": merchantId}
            )
        
        if response.status_code == 200:
            logger.info("Successfully fetched data from external server.")
            return response.json()
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Endpoint - Get Ticket Fare
@qr_router.post("/getTicketFare")
async def get_ticket_fare(farePayload: GetFarePayload):
    
    token = farePayload.token
    fromStationId = farePayload.fromStationId
    toStationId = farePayload.toStationId
    zoneNumberOrStored_ValueAmount = farePayload.zoneNumberOrStored_ValueAmount
    ticketTypeId = farePayload.ticketTypeId
    merchant_id = farePayload.merchant_id
    travelDatetime = farePayload.travelDatetime

    payload={
            "fromStationId": fromStationId,
            "toStationId": toStationId,
            "zoneNumberOrStored_ValueAmount": zoneNumberOrStored_ValueAmount,
            "ticketTypeId": ticketTypeId,
            "merchant_id": merchant_id,
            "travelDatetime": travelDatetime
            }
    
    try:
        async with httpx.AsyncClient() as client:
            response =  await client.post(
                url = f'{URL}/Tickets/GetFare',
                headers={"Authorization": f"Bearer {token}"},
                json = payload)

        # json_response = json.dumps(response.json())
     
        if response.status_code == 200:
            logger.info("Successfully fetched data from Metro server.")
            return response.json()[0]
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

# Endpoint - Generate Ticket 
@qr_router.post("/generateTicket")
async def generate_ticket(ticketPayload: GetTicketRequestPayload):
    
    token = ticketPayload.token
    merchantOrderId = ticketPayload.merchantOrderId
    merchantId = ticketPayload.merchantId
    transType = ticketPayload.transType
    fromStationId = ticketPayload.fromStationId
    toStationid = ticketPayload.toStationid
    ticketTypeId = ticketPayload.ticketTypeId
    noOfTickets = ticketPayload.noOfTickets
    travelDateTime = ticketPayload.travelDateTime
    merchantEachTicketFareBeforeGst = ticketPayload.merchantEachTicketFareBeforeGst
    merchantEachTicketFareAfterGst = ticketPayload.merchantEachTicketFareAfterGst
    merchantTotalFareBeforeGst = ticketPayload.merchantTotalFareBeforeGst
    merchantTotalCgst = ticketPayload.merchantTotalCgst
    merchantTotalSgst = ticketPayload.merchantTotalSgst
    merchantTotalFareAfterGst = ticketPayload.merchantTotalFareAfterGst
    ltmrhlPassId = ticketPayload.ltmrhlPassId
    patronPhoneNumber = ticketPayload.patronPhoneNumber
    fareQuoteIdforOneTicket = ticketPayload.fareQuoteIdforOneTicket

    payload={
            "merchantOrderId": merchantOrderId,
            "merchantId": merchantId,
            "transType": transType,
            "fromStationId": fromStationId,
            "toStationid": toStationid,
            "ticketTypeId": ticketTypeId,
            "noOfTickets": noOfTickets,
            "travelDateTime": travelDateTime,
            "merchantEachTicketFareBeforeGst": merchantEachTicketFareBeforeGst,
            "merchantEachTicketFareAfterGst": merchantEachTicketFareAfterGst,
            "merchantTotalFareBeforeGst": merchantTotalFareBeforeGst,
            "merchantTotalCgst": merchantTotalCgst,
            "merchantTotalSgst": merchantTotalSgst,
            "merchantTotalFareAfterGst": merchantTotalFareAfterGst,
            "ltmrhlPassId": ltmrhlPassId,
            "patronPhoneNumber": patronPhoneNumber,
            "fareQuoteIdforOneTicket": fareQuoteIdforOneTicket
            }
    
    try:
        async with httpx.AsyncClient() as client:
            response =  await client.post(
                url = f'{URL}/Tickets/GenerateTicket',
                headers={"Authorization": f"Bearer {token}"},
                json = payload)
     
        if response.status_code == 200:
            logger.info("Successfully fetched data from Metro server.")
            return response.json()
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
# Endpoint - Get Ticket Details By ID
@qr_router.post("/getTicketDetailsById")
async def get_ticket_details_by_id(payload: GetTicketDetailsByIdPayload):
    
    token = payload.token
    ticketId = payload.ticketId
    ltmrhlPurchaseId = payload.ltmrhlPurchaseId
    rjtID = payload.rjtID
    ticketTypeid = payload.ticketTypeid
    queringStationID = payload.queringStationID

    payload={
            "ticketId": ticketId,
            "ltmrhlPurchaseId": ltmrhlPurchaseId,
            "rjtID": rjtID,
            "ticketTypeId": ticketTypeid,
            "queringStationID": queringStationID            
            }
    
    try:
        async with httpx.AsyncClient() as client:
            response =  await client.post(
                url = f'{URL}/Tickets/GetTicketDetailsById',
                headers={"Authorization": f"Bearer {token}"},
                json = payload)
     
        if response.status_code == 200:
            logger.info("Successfully fetched data from Metro server.")
            return response.json()
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint - Change Destination Preview
@qr_router.post("/changeDestinationPreview")
async def change_destination_preview(payload: ChangeDestinationPreviewPayload):
    
    token = payload.token
    ticketId = payload.ticketId
    newDestination = payload.newDestination
   
    payload={
            "ticketId": ticketId,
            "newDestination": newDestination          
            }
    
    try:
        async with httpx.AsyncClient() as client:
            response =  await client.post(
                url = f'{URL}/Tickets/ChangeOfDestinationPreview',
                headers={"Authorization": f"Bearer {token}"},
                json = payload)
     
        if response.status_code == 200:
            logger.info("Successfully fetched data from Metro server.")
            return response.json()
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint - Change Destination 
@qr_router.post("/changeDestination")
async def change_destination(payload: ChangeDestinationPayload):
    
    token = payload.token
    ticketId = payload.ticketId
    newDestinationId = payload.newDestinationId
    newOrderId= payload.newOrderId
    codQuoteId= payload.codQuoteId

    payload={
            "ticketId": ticketId,
            "newDestinationId": newDestinationId,
            "newOrderId": newOrderId,
            "codQuoteId": codQuoteId
            }
    
    try:
        async with httpx.AsyncClient() as client:
            response =  await client.post(
                url = f'{URL}/Tickets/ChangeOfDestination',
                headers={"Authorization": f"Bearer {token}"},
                json = payload)
     
        if response.status_code == 200:
            logger.info("Successfully fetched data from Metro server.")
            return response.json()
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    
# Endpoint - Get Entry Ticket Used Status
@qr_router.post("/getEntryTicketUsedStatus")
async def get_entry_ticket_used_status(payload: TicketUsedStatusPayload):
    
    token = payload.token
    ticketId = payload.ticketId
    merchantId = payload.merchantId

    try:
        async with httpx.AsyncClient() as client:

            response =  await client.get(
                url = f'{URL}/Tickets/EntryTicketUsedStatus',
                headers={"Authorization": f"Bearer {token}"},
                params= {"token":token,"ticketId":ticketId,"merchantId": merchantId}
            )
        
        if response.status_code == 200:
            logger.info("Successfully fetched data from external server.")
            return response.json()
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
# Endpoint - Get Exit Ticket Used Status
@qr_router.post("/getExitTicketUsedStatus")
async def get_exit_ticket_used_status(payload: TicketUsedStatusPayload):
    
    token = payload.token
    ticketId = payload.ticketId
    merchantId = payload.merchantId

    try:
        async with httpx.AsyncClient() as client:

            response =  await client.get(
                url = f'{URL}/Tickets/ExitTicketUsedStatus',
                headers={"Authorization": f"Bearer {token}"},
                params= {"token":token,"ticketId":ticketId,"merchantId": merchantId}
            )
        
        if response.status_code == 200:
            logger.info("Successfully fetched data from external server.")
            return response.json()
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint - Get Ticket Details By Phone MerchantId
@qr_router.post("/getTicketDetailsByPhoneMerchantId")
async def get_ticket_details_by_phone_merchant_id(payload: GetTicketDetailsByPhoneMerchantIdPayload):
    
    token = payload.token
    patornPhoneNumber = payload.patornPhoneNumber
    merchantId = payload.merchantId
    selectedMonthYear= payload.selectedMonthYear
    

    payload={
            "patornPhoneNumber": patornPhoneNumber,
            "merchantId": merchantId,
            "selectedMonthYear": selectedMonthYear
            }
    
    try:
        async with httpx.AsyncClient() as client:
            response =  await client.post(
                url = f'{URL}/Tickets/GetTicketDetailsByPhoneMerchantId',
                headers={"Authorization": f"Bearer {token}"},
                json = payload)
     
        if response.status_code == 200:
            logger.info("Successfully fetched data from Metro server.")
            return response.json()
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint - Refund Preview
@qr_router.post("/refunPreview")
async def refund_preview(payload: RefundPayload):
    
    token = payload.token
    ticketId = payload.ticketId
    rjtId = payload.rjtId
    passId = payload.passId
    merchantId = payload.merchantId
    ltmrhlPurchaseId = payload.ltmrhlPurchaseId
    transactionType = payload.transactionType
    refundQuoteId = payload.refundQuoteId
   
    payload={
            "ticketId": ticketId,
            "rjtId": rjtId,
            "passId": passId,
            "merchantId":merchantId,
            "ltmrhlPurchaseId":ltmrhlPurchaseId,
            "transactionType":transactionType,
             "refundQuoteId":refundQuoteId
            }
    
    try:
        async with httpx.AsyncClient() as client:
            response =  await client.post(
                url = f'{URL}/Refund/RefundPreview',
                headers={"Authorization": f"Bearer {token}"},
                json = payload)
     
        if response.status_code == 200:
            logger.info("Successfully fetched data from Metro server.")
            return response.json()
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint - Refund Confirmed
@qr_router.post("/refunConfirmed")
async def refund_confirmed(payload: RefundPayload):
    
    token = payload.token
    ticketId = payload.ticketId
    rjtId = payload.rjtId
    passId = payload.passId
    merchantId = payload.merchantId
    ltmrhlPurchaseId = payload.ltmrhlPurchaseId
    transactionType = payload.transactionType
    refundQuoteId = payload.refundQuoteId
   
    payload={
            "ticketId": ticketId,
            "rjtId": rjtId,
            "passId": passId,
            "merchantId":merchantId,
            "ltmrhlPurchaseId":ltmrhlPurchaseId,
            "transactionType":transactionType,
             "refundQuoteId":refundQuoteId
            }
    
    try:
        async with httpx.AsyncClient() as client:
            response =  await client.post(
                url = f'{URL}/Refund/RefundConfirmed',
                headers={"Authorization": f"Bearer {token}"},
                json = payload)
     
        if response.status_code == 200:
            logger.info("Successfully fetched data from Metro server.")
            return response.json()
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint - Get Order Status By Merchant Order Id
@qr_router.post("/getOrderStatusByMerchantOrderId")
async def get_order_status_by_merchant_order_id (payload : GetOrderStatusByMerchantOrderIdPayload):

    token = payload.token
    merchantOrderId = payload.merchantOrderId
    merchantId = payload.merchantId
    
    try:
        async with httpx.AsyncClient() as client:

            response =  await client.get(
                url = f'{URL}/MerchantOrder/getOrderStatusByMerchantOrderId',
                headers={"Authorization": f"Bearer {token}"},
                params= {"merchantOrderId": merchantOrderId,"merchantId":merchantId}
            )
        
        if response.status_code == 200:
            logger.info("Successfully fetched data from external server.")
            return response.json()
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
# Endpoint - Refund On Request By Merchant
@qr_router.post("/refundOnRequestByMerchant")
async def refund_on_request_by_merchant(payload: RefundOnRequestByMerchantPayload):
    
    token = payload.token
    merchantOrderId = payload.merchantOrderId
    merchantId = payload.merchantId
    fromStationId = payload.fromStationId
    toStationId = payload.toStationId
    ticketTypeId = payload.ticketTypeId
    noOfTickets = payload.noOfTickets
    travelDateTime = payload.travelDateTime
    ltmrhlPassId = payload.ltmrhlPassId
    patronPhoneNumber = payload.patronPhoneNumber

    payload={
            "merchantOrderId": merchantOrderId,
            "merchantId": merchantId,
            "fromStationId": fromStationId,
            "toStationId": toStationId,
            "ticketTypeId": ticketTypeId,
            "noOfTickets": noOfTickets,
            "travelDateTime": travelDateTime,
            "ltmrhlPassId" : ltmrhlPassId,
            "patronPhoneNumber" : patronPhoneNumber
            }
    
    try:
        async with httpx.AsyncClient() as client:
            response =  await client.post(
                url = f'{URL}/MerchantOrder/refundOnRequestByMerchant',
                headers={"Authorization": f"Bearer {token}"},
                json = payload)
     
        if response.status_code == 200:
            logger.info("Successfully fetched data from Metro server.")
            return response.json()
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint - Change Password 
@qr_router.put("/ChangePassword")
async def change_password(payload: ChangePasswordPayload):
    
    token = payload.token
    merchantId = payload.merchantId
    currentPassword = payload.currentPassword
    newPassword = payload.newPassword
    

    payload={
            "merchantId": merchantId,
            "currentPassword": currentPassword,
            "newPassword": newPassword
            }
    
    try:
        async with httpx.AsyncClient() as client:
            response =  await client.put(
                url = f'{URL}/Account/ChangePassword',
                headers={"Authorization": f"Bearer {token}"},
                json = payload)
     
        if response.status_code == 200:
            logger.info("Successfully fetched data from Metro server.")
            return response.json()
        else:
            logger.error(f"Failed to fetch data: {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
