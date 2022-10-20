import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, Table
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint
from sqlalchemy.types import DateTime, String, Text

from helpers.db import db

user_role_table = Table(
    'user_role',
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("role_id", ForeignKey("role.id"), primary_key=True),
)


def create_partition(target, connection, **kw) -> None:
    """ creating partition by user_sign_in """
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS "user_login_record_smart" 
        PARTITION OF "user_login_record" 
        FOR VALUES IN ('smart')
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS "user_login_record_mobile" 
        PARTITION OF "user_login_record" 
        FOR VALUES IN ('mobile')
        """
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_login_record_web"   
        PARTITION OF "user_login_record" 
        FOR VALUES IN ('web')
        """
    )


class User(db.Model):
    __tablename__ = 'user'

    id = Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    login_records = relationship('UserLoginRecord', backref='user')
    roles = relationship('Role', secondary=user_role_table, back_populates="users")


class UserLoginRecord(db.Model):
    __tablename__ = 'user_login_record'
    # __table_args__ = (
    #     UniqueConstraint('id', 'user_device_type'),
    #     {
    #         'postgresql_partition_by': 'LIST (user_device_type)',
    #         'listeners': [('after_create', create_partition)],
    #     }
    # )

    id = Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column('user_id', UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    user_agent = Column('user_agent', Text(), nullable=True)
    access_token = Column('access_token', Text(), nullable=False)
    refresh_token = Column('refresh_token', Text(), nullable=False)
    login_at = Column('login_at', DateTime(), nullable=False, default=func.now())
    # user_device_type = db.Column(db.Text, primary_key=True)


class Role(db.Model):
    __tablename__ = 'role'

    id = Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(128), nullable=False)
    users = relationship('User', secondary=user_role_table, back_populates="roles")
