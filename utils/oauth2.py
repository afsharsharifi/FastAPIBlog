from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWSError, jwt
from core import config
from datetime import datetime, timedelta
from schemas import auth

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, config.ALGORITHM)
        id: str = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = auth.TokenData(id=id)
    except JWSError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not Validate Credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
