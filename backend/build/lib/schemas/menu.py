from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# MenuItem Schemas
class MenuItemBase(BaseModel):
    title: str
    icon: Optional[str] = None
    route: Optional[str] = None
    parent_id: Optional[int] = None
    order: int = 0
    is_active: bool = True


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    title: Optional[str] = None
    icon: Optional[str] = None
    route: Optional[str] = None
    parent_id: Optional[int] = None
    order: Optional[int] = None
    is_active: Optional[bool] = None


class MenuItem(MenuItemBase):
    id: int
    created_at: datetime
    children: List["MenuItem"] = []

    class Config:
        from_attributes = True


# ButtonPermission Schemas
class ButtonPermissionBase(BaseModel):
    button_id: str
    description: Optional[str] = None
    menu_item_id: int


class ButtonPermissionCreate(ButtonPermissionBase):
    pass


class ButtonPermissionUpdate(BaseModel):
    description: Optional[str] = None
    menu_item_id: Optional[int] = None


class ButtonPermission(ButtonPermissionBase):
    id: int

    class Config:
        from_attributes = True


# User Permission Schemas
class UserMenuPermission(BaseModel):
    menu_item_id: int
    has_permission: bool = True


class UserButtonPermission(BaseModel):
    button_id: str
    has_permission: bool = False


class UserMenuResponse(BaseModel):
    id: int
    title: str
    icon: Optional[str] = None
    route: Optional[str] = None
    order: int
    children: List["UserMenuResponse"] = []
    buttons: List[UserButtonPermission] = []

    class Config:
        from_attributes = True


class SetUserMenuPermissions(BaseModel):
    menu_permissions: List[UserMenuPermission]


class SetUserButtonPermissions(BaseModel):
    button_permissions: List[UserButtonPermission]


# 解决前向引用
MenuItem.model_rebuild()
UserMenuResponse.model_rebuild()
