from fastapi import FastAPI
from auth import auth_router
from orders import order_router
from reports import report_router
from database import Base, engine

app = FastAPI()
#hmm
# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(report_router)