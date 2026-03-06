from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.config import settings
from app.core.exceptions import credentials_exception, NotFoundException
from app.db.database import get_db
from app.db import models
from app.schemas.auth import TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User:

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        email: str | None = payload.get("sub")
        tenant_id: int | None = payload.get("tenant_id")

        if email is None:
            raise credentials_exception

        token_data = TokenData(email=email, tenant_id=tenant_id)

    except JWTError:
        raise credentials_exception

    # If tenant_id exists in token, use it for safer multi-tenant resolution
    query = db.query(models.User).filter(models.User.email == token_data.email)

    if token_data.tenant_id is not None:
        query = query.filter(models.User.tenant_id == token_data.tenant_id)

    user = query.first()

    if user is None:
        raise credentials_exception

    return user


def get_current_tenant(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> models.Tenant:

    tenant = db.query(models.Tenant).filter(models.Tenant.id == current_user.tenant_id).first()
    if not tenant:
        raise NotFoundException(detail="Tenant not found for current user")
    return tenant