from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.base import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    icon = Column(String(30), nullable=True)
    route = Column(String(100), nullable=True)
    parent_id = Column(Integer, ForeignKey("menu_items.id"), nullable=True)
    order = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=func.now())

    # 自引用关系
    parent = relationship("MenuItem", remote_side=[id], back_populates="children")
    children = relationship("MenuItem", back_populates="parent")

    # 与用户菜单权限的关系
    user_menu_items = relationship("UserMenuItem", back_populates="menu_item")

    # 与按钮权限的关系
    button_permissions = relationship("ButtonPermission", back_populates="menu_item")


class UserMenuItem(Base):
    __tablename__ = "user_menu_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    has_permission = Column(Boolean, nullable=False, default=True)

    # 关系
    user = relationship("User", back_populates="menu_items")
    menu_item = relationship("MenuItem", back_populates="user_menu_items")


class ButtonPermission(Base):
    __tablename__ = "button_permissions"

    id = Column(Integer, primary_key=True, index=True)
    button_id = Column(String(50), nullable=False, unique=True)
    description = Column(String(100), nullable=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)

    # 关系
    menu_item = relationship("MenuItem", back_populates="button_permissions")
    user_button_permissions = relationship(
        "UserButtonPermission", back_populates="button_permission"
    )


class UserButtonPermission(Base):
    __tablename__ = "user_button_permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    button_id = Column(
        String(50), ForeignKey("button_permissions.button_id"), nullable=False
    )
    has_permission = Column(Boolean, nullable=False, default=False)

    # 关系
    user = relationship("User", back_populates="button_permissions")
    button_permission = relationship(
        "ButtonPermission", back_populates="user_button_permissions"
    )
