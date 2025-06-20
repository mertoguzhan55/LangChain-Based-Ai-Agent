from jose import jwt, JWTError
from dataclasses import dataclass
import uvicorn
from fastapi import FastAPI, Request, Depends, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Form, Request
from app.logger import Logger
from app.utils import verify_password, hash_password, create_access_token
from fastapi.responses import JSONResponse, RedirectResponse

from app.crud import CRUDOperations
from models.models import User

@dataclass
class FastAPIServer:
    database_type: str
    host: str
    port: int
    reload: bool
    log_level: str
    crud: CRUDOperations
    logger: Logger

    def __post_init__(self):
        self.app = FastAPI()
        self.templates = Jinja2Templates(directory="app/templates")
        self.app.mount(f"/static", StaticFiles(directory="app/static"), name="static")
        self.logger.info("Fastapi init")
    def run(self):
        self.server()
        self.logger.info("Server Initialized!")
        uvicorn.run(app=self.app, host=self.host, port=self.port, log_level=self.log_level)

    def server(self):
        @self.app.get("/")
        async def base(request: Request):
            return self.templates.TemplateResponse("register.html", {"request": request})

        @self.app.get("/login")
        async def login_page(request: Request):
            return self.templates.TemplateResponse("login.html", {"request": request})

        @self.app.post("/login")
        async def login_user(request: Request, email: str = Form(...), password: str = Form(...)):

            await self.crud.initialize()
            user = self.crud.read_by_email(User, str(email))

            if not user or not verify_password(password, user.hashed_password):
                return self.templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

            token = create_access_token({"sub": str(user.id)})
            response = RedirectResponse("/", status_code = status.HTTP_302_FOUND)
            response.set_cookie(key="access_token", value=token, httponly=True, max_age=900)
            return response

        @self.app.get("/register")
        async def register_page(request: Request):
            return self.templates.TemplateResponse("register.html", {"request": request})

        @self.app.post("/register")
        async def register_user(request: Request, email: str = Form(...), password: str = Form(...)):
            await self.crud.initialize()
            user_exist = await self.crud.read_by_email(User,str(email))
            if user_exist:
                return self.templates.TemplateResponse("register.html", {"request": request, "error": "Username already exists"})

            user = User(email=email, hashed_password = hash_password(str(password)))
            await self.crud.create(user)

            # Register sonrası otomatik login ve token oluşturma
            print("User ID after create:", user.id)

            token = create_access_token({"sub": str(user.id)})
            print("Generated token:", token)

            response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
            response.set_cookie(key="access_token", value=token, httponly=True, max_age=900)
            return response

        @self.app.get("/jwt")
        async def jwt(request: Request):
            token = request.cookies.get("access_token")
            from app.utils import SECRET_KEY, ALGORITHM
            if not token:
                return {"error": "No token provided"}

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                return {"payload": payload}
            except JWTError as e:
                return {"error": f"Invalid or expired token: {str(e)}"}


if __name__ == "__main__":

    pass