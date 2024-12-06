from pydantic import BaseModel, Field
from datetime import date, datetime

class SendOTPRequest(BaseModel):
    phone_number: str = Field(..., description="Phone number with country code e.g. +11234567890")


class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp: str
    
class RetentionConfig(BaseModel):
    days: int 

class PpslTransactionDetails(BaseModel):
    requestType: str = "Payment"
    mid: str
    websiteName: str
    orderId: str
    callbackUrl: str
    txnAmount_value: str
    txnAmount_currency: str = "INR"
    custId: str
    merchant_key: str

class CustomerDetails(BaseModel):
    customer_id: str
    customer_email: str
    customer_phone: str
    customer_name: str

class OrderMeta(BaseModel):
    return_url: str
    notify_url: str

class CashFreeTransactionDetails(BaseModel):
    customer_details: CustomerDetails
    order_meta: OrderMeta
    order_id: str
    order_amount: float
    order_currency: str
    order_note: str

class getOrderdetails(BaseModel):
    order_id: str
    
class GetFarePayload(BaseModel):
    token: str
    fromStationId: str
    toStationId: str
    zoneNumberOrStored_ValueAmount: int
    ticketTypeId: int
    merchant_id: str
    travelDatetime: str

class GetTicketRequestPayload(BaseModel):
    token: str
    merchantOrderId: str
    merchantId: str
    transType: str
    fromStationId: str
    toStationid: str
    ticketTypeId: str
    noOfTickets: str
    travelDateTime: str
    merchantEachTicketFareBeforeGst: int
    merchantEachTicketFareAfterGst: int
    merchantTotalFareBeforeGst: int
    merchantTotalCgst: int
    merchantTotalSgst: int
    merchantTotalFareAfterGst: int
    ltmrhlPassId: str
    patronPhoneNumber: str
    fareQuoteIdforOneTicket: str

class GetStationsByzonePayload(BaseModel):
    token: str
    fromStationId: str
    zoneNumber: str

class TokenPayload(BaseModel):
    token: str

class GetTicketTypesPayload(BaseModel):
    token: str
    merchantId: str

class GetTicketDetailsByIdPayload(BaseModel):
    token: str
    ticketId: str
    ltmrhlPurchaseId: str
    rjtID: str
    ticketTypeid: str
    queringStationID: str

class ChangeDestinationPreviewPayload(BaseModel):
    token: str
    ticketId: str
    newDestination: str

class ChangeDestinationPayload(BaseModel):
    token: str
    ticketId: str
    newDestinationId: str
    newOrderId: str
    codQuoteId: str

class TicketUsedStatusPayload(BaseModel):
    token: str
    ticketId: str
    merchantId: str

class GetTicketDetailsByPhoneMerchantIdPayload(BaseModel):
    token: str
    patornPhoneNumber: str
    merchantId: str
    selectedMonthYear: str

class RefundPayload(BaseModel):
    token: str
    ticketId: str
    rjtId: str
    passId: str
    merchantId: str
    ltmrhlPurchaseId: str
    transactionType: str
    refundQuoteId: str

class GetOrderStatusByMerchantOrderIdPayload(BaseModel):
    token: str
    merchantOrderId: str
    merchantId: str

class RefundOnRequestByMerchantPayload(BaseModel):
  token: str
  merchantOrderId: str
  merchantId: str
  fromStationId: str
  toStationId: str
  ticketTypeId: int
  noOfTickets: int
  travelDateTime: str
  ltmrhlPassId: str
  patronPhoneNumber: str

class ChangePasswordPayload(BaseModel):
  token: str
  merchantId: str
  currentPassword: str
  newPassword: str

class UserRegisterCreate(BaseModel):
  First_Name: str
  Last_Name: str
  Gender: str = None
  Date_of_birth: date 
  Mobile_No: str
  Email_Address: str 
  Password: str
  User_Type: str = None
  IMEI: str = None
  RegistetedBy: str = None
  Source: str = None
  DeviceType: str = None
  ActiveStatus: str = None
  ModifiedDate: datetime = None
  TransactionPin: str = None
  UpdateEmail: str = None
  UpdateMobileNo: str = None
  UpdatePassword: str = None
  Access_Token: str = None
  Acc_Token_Expiry_Date: str = None 
  Last_Login_Time: str = None
  Device_Info: str = None
  Email_Update: str = None
  Mob_Update: str = None
  Password_Update: str = None
  Alt_EmailId: str = None
  Device_Token: str = None
  
class UserFeedbackCreate(BaseModel):
   UID: int
   Subject:str
   Description:str
   Image:dict

class UserFeedbackResponse(BaseModel):
   UID: int
   Subject:str
   Description:str
   Image:str
   Created_at: datetime

class UserFeedbackItemResponse(UserFeedbackResponse):
   pass
