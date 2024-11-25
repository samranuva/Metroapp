from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from Endpoints.auth import send_otp, verify_otp, SendOTPRequest, VerifyOTPRequest
from Endpoints.log_handling import log_router
from Endpoints.ppsl_pg import ppslpg_router
from Endpoints.qr_endpoints import qr_router
from Endpoints.cashfree_pg import cfpg_router


app = FastAPI(
    title="Mapp API",
    description="API for tapp",
    version="1.2.0",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include router
app.include_router(log_router, prefix="/logging", tags=["Logging"])
app.include_router(ppslpg_router,prefix="/psplpg",tags=["PSPL Payment Gateway"])
app.include_router(cfpg_router,prefix="/cfpg",tags=["Cashfree Payment Gateway"])
app.include_router(qr_router,prefix="/qr",tags=[" APIs"])





# @app.post("/auth/send-otp", tags=["Authentication"])
# async def api_send_otp(request: SendOTPRequest):
#     """
#     Send an OTP to the provided phone number.
#     """
#     return await send_otp(request)

# @app.post("/auth/verify-otp", tags=["Authentication"])
# async def api_verify_otp(request: VerifyOTPRequest):
#     """
#     Verify the OTP provided by the user.
#     """
#     return await verify_otp(request)

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify if the API is running.
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    import os

    load_dotenv()
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
