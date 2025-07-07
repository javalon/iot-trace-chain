from fastapi import FastAPI
from app.routes.device import router as device_router
from app.routes.times import router as times_router
import logging
from app.utils.filter_logs import HealthCheckFilter

logging.getLogger("uvicorn.access").addFilter(HealthCheckFilter())

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(device_router, prefix="/device", tags=["Devices"])
app.include_router(times_router, prefix="/times", tags=["Times"])
