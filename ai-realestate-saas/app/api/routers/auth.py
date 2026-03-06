from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db import models
from app.db.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from app.schemas.auth import Token, UserCreate, UserResponse
from app.schemas.tenant import TenantCreate, TenantResponse
from app.core.exceptions import credentials_exception, BadRequestException

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register-tenant", response_model=TenantResponse)
def register_tenant(tenant: TenantCreate, db: Session = Depends(get_db)):
    db_tenant = (
        db.query(models.Tenant)
        .filter(models.Tenant.subdomain == tenant.subdomain)
        .first()
    )
    if db_tenant:
        raise BadRequestException(detail="Subdomain already registered")

    new_tenant = models.Tenant(name=tenant.name, subdomain=tenant.subdomain)
    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)
    return new_tenant


@router.post("/register-user", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # NOTE: Your DB model currently has email unique=True
    # So same email cannot exist across multiple tenants.
    # For now we keep that behavior.
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise BadRequestException(detail="Email already registered")

    tenant = db.query(models.Tenant).filter(models.Tenant.id == user.tenant_id).first()
    if not tenant:
        raise BadRequestException(detail="Tenant not found")

    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        tenant_id=user.tenant_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise credentials_exception

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # ✅ embed tenant_id into token for safer multi-tenant access
    access_token = create_access_token(
        data={"sub": user.email, "tenant_id": user.tenant_id},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}