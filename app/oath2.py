from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# sceret key
# algorithm used
# expiration time
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    print(data)
    to_encode = data.copy()
    print(f"to_encode: {to_encode}")
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    ecodec_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"ecoded_jwt: {to_encode}")

    return ecodec_jwt


def verify_acess_token(token: str, credientials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credientials_exception

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credientials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_acess_token(token, credentials_exception)
