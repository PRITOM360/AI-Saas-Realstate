from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Tenant(Base):

    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    subdomain = Column(
        String,
        unique=True,
        index=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    users = relationship(
        "User",
        back_populates="tenant"
    )

    leads = relationship(
        "Lead",
        back_populates="tenant"
    )


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password = Column(String)

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id"),
        index=True
    )

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    tenant = relationship(
        "Tenant",
        back_populates="users"
    )


class Lead(Base):

    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id"),
        index=True
    )

    name = Column(String, nullable=False)

    phone = Column(String, nullable=False)

    score = Column(Integer, default=0)

    status = Column(String, default="cold")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    tenant = relationship(
        "Tenant",
        back_populates="leads"
    )

    conversations = relationship(
        "Conversation",
        back_populates="lead"
    )

    appointments = relationship(
        "Appointment",
        back_populates="lead"
    )


class Conversation(Base):

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id"),
        index=True
    )

    lead_id = Column(
        Integer,
        ForeignKey("leads.id"),
        index=True
    )

    message = Column(String)

    sender = Column(String)

    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    lead = relationship(
        "Lead",
        back_populates="conversations"
    )


class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id"),
        index=True
    )

    lead_id = Column(
        Integer,
        ForeignKey("leads.id"),
        index=True
    )

    scheduled_time = Column(DateTime)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    lead = relationship(
        "Lead",
        back_populates="appointments"
    )