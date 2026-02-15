from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.session import get_db
from app.models.user import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
settings = get_settings()


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication")
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exc
    except JWTError as exc:
        raise credentials_exc from exc

    user = (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()
    if not user:
        raise credentials_exc
    return user


def require_role(*roles: UserRole):
    async def role_checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user

    return role_checker
