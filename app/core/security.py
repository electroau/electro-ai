import uuid
from dataclasses import dataclass

from fastapi import Header, HTTPException, status


@dataclass
class AuthUser:
    id: uuid.UUID
    role: str


async def get_current_user(
    x_user_id: str | None = Header(default=None, alias='X-User-Id'),
    x_user_role: str | None = Header(default='employee', alias='X-User-Role'),
) -> AuthUser:
    if not x_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Missing user authentication headers')

    try:
        user_id = uuid.UUID(x_user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid user id') from exc

    role = (x_user_role or 'employee').lower()
    if role not in {'employee', 'admin'}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid role')

    return AuthUser(id=user_id, role=role)
