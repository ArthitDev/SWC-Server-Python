import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.db.database import Base, engine
from app.routers import register_admin_route
from app.routers import login_admin_route
from app.routers import admin_protected_route
from app.routers import profile_admin_route
from app.routers import refresh_token_route
from app.models.password_reset import Base
from app.services.logout_admin_service import router as logout_admin_router
from app.routers.reset_password_route import router as reset_password_router
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
import secure
from main_info import get_main_info

load_dotenv()

app = FastAPI()

# Initialize Limiter
limiter = Limiter(key_func=get_remote_address)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGIN")],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Add GZip middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add SlowAPI middleware
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Add Secure headers
secure_headers = secure.Secure()


@app.middleware("http")
async def set_secure_headers(request: Request, call_next):
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response


# Add HTTPS redirect middleware only in production
if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

# Create the database tables
Base.metadata.create_all(bind=engine)


# Root path
@app.get("/")
@limiter.limit("5/minute")
async def root(request: Request):
    return await get_main_info()


# Include the admin routers
app.include_router(register_admin_route.router, prefix="/api", tags=["register"])
app.include_router(login_admin_route.router, prefix="/api", tags=["login"])
app.include_router(logout_admin_router, prefix="/api", tags=["logout"])
app.include_router(admin_protected_route.router, prefix="/api", tags=["protected"])
app.include_router(profile_admin_route.router, prefix="/api", tags=["profile"])
app.include_router(refresh_token_route.router, prefix="/api", tags=["token"])
app.include_router(reset_password_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 3000)))
