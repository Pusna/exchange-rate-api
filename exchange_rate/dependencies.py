from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
import httpx

from exchange_rate.schemas import AuthUserResponse


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'
AUTH_SERVICE_URL = "http://auth_service:8000"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> AuthUserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Невалідний токен або не вдалося авторизувати користувача",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email: str = payload.get("sub")
        user_id: int | None = payload.get("id")
        username: str | None = payload.get("username")

        if email is None or user_id is None or username is None:
            raise credentials_exception

        user = AuthUserResponse(id=user_id, username=username, email=email)
        return user

    except JWTError:
        raise credentials_exception
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Невідома помилка при обробці токена: {e}"
        )