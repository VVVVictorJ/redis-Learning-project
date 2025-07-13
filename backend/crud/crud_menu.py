from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from models.menu import MenuItem, UserMenuItem, ButtonPermission, UserButtonPermission
from schemas.menu import (
    MenuItemCreate,
    MenuItemUpdate,
    ButtonPermissionCreate,
    UserMenuPermission,
    UserButtonPermission as UserButtonPermissionSchema,
)


# MenuItem CRUD
def create_menu_item(db: Session, menu_item: MenuItemCreate) -> MenuItem:
    db_menu_item = MenuItem(**menu_item.model_dump())
    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item


def get_menu_item(db: Session, menu_item_id: int) -> Optional[MenuItem]:
    return db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()


def get_menu_items(
    db: Session, skip: int = 0, limit: int = 100, include_inactive: bool = False
) -> List[MenuItem]:
    query = db.query(MenuItem)
    if not include_inactive:
        query = query.filter(MenuItem.is_active == True)
    return query.offset(skip).limit(limit).all()


def get_root_menu_items(db: Session, include_inactive: bool = False) -> List[MenuItem]:
    """获取根菜单项（没有父级的菜单项）"""
    query = db.query(MenuItem).filter(MenuItem.parent_id.is_(None))
    if not include_inactive:
        query = query.filter(MenuItem.is_active == True)
    return query.order_by(MenuItem.order).all()


def update_menu_item(
    db: Session, menu_item_id: int, menu_item_update: MenuItemUpdate
) -> Optional[MenuItem]:
    db_menu_item = get_menu_item(db, menu_item_id)
    if not db_menu_item:
        return None

    update_data = menu_item_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_menu_item, key, value)

    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item


def delete_menu_item(db: Session, menu_item_id: int) -> bool:
    db_menu_item = get_menu_item(db, menu_item_id)
    if not db_menu_item:
        return False

    db.delete(db_menu_item)
    db.commit()
    return True


# ButtonPermission CRUD
def create_button_permission(
    db: Session, button_permission: ButtonPermissionCreate
) -> ButtonPermission:
    db_button_permission = ButtonPermission(**button_permission.model_dump())
    db.add(db_button_permission)
    db.commit()
    db.refresh(db_button_permission)
    return db_button_permission


def get_button_permissions(
    db: Session, menu_item_id: Optional[int] = None
) -> List[ButtonPermission]:
    query = db.query(ButtonPermission)
    if menu_item_id:
        query = query.filter(ButtonPermission.menu_item_id == menu_item_id)
    return query.all()


def get_button_permission(db: Session, button_id: str) -> Optional[ButtonPermission]:
    return (
        db.query(ButtonPermission)
        .filter(ButtonPermission.button_id == button_id)
        .first()
    )


# User Menu Permissions
def set_user_menu_permissions(
    db: Session, user_id: int, menu_permissions: List[UserMenuPermission]
) -> bool:
    """设置用户菜单权限"""
    # 删除现有权限
    db.query(UserMenuItem).filter(UserMenuItem.user_id == user_id).delete()

    # 添加新权限
    for perm in menu_permissions:
        db_user_menu = UserMenuItem(
            user_id=user_id,
            menu_item_id=perm.menu_item_id,
            has_permission=perm.has_permission,
        )
        db.add(db_user_menu)

    db.commit()
    return True


def get_user_menu_permissions(db: Session, user_id: int) -> List[UserMenuItem]:
    """获取用户菜单权限"""
    return db.query(UserMenuItem).filter(UserMenuItem.user_id == user_id).all()


def get_user_accessible_menus(db: Session, user_id: int) -> List[MenuItem]:
    """获取用户可访问的菜单项"""
    # 如果是超级用户，返回所有活跃菜单
    from models.user import User

    user = db.query(User).filter(User.id == user_id).first()
    if user and user.is_superuser:
        return get_root_menu_items(db, include_inactive=False)

    # 普通用户只返回有权限的菜单
    accessible_menu_ids = (
        db.query(UserMenuItem.menu_item_id)
        .filter(
            and_(UserMenuItem.user_id == user_id, UserMenuItem.has_permission == True)
        )
        .subquery()
    )

    return (
        db.query(MenuItem)
        .filter(
            and_(
                MenuItem.id.in_(accessible_menu_ids),
                MenuItem.is_active == True,
                MenuItem.parent_id.is_(None),
            )
        )
        .order_by(MenuItem.order)
        .all()
    )


# User Button Permissions
def set_user_button_permissions(
    db: Session, user_id: int, button_permissions: List[UserButtonPermissionSchema]
) -> bool:
    """设置用户按钮权限"""
    # 删除现有权限
    db.query(UserButtonPermission).filter(
        UserButtonPermission.user_id == user_id
    ).delete()

    # 添加新权限
    for perm in button_permissions:
        db_user_button = UserButtonPermission(
            user_id=user_id,
            button_id=perm.button_id,
            has_permission=perm.has_permission,
        )
        db.add(db_user_button)

    db.commit()
    return True


def get_user_button_permissions(
    db: Session, user_id: int
) -> List[UserButtonPermission]:
    """获取用户按钮权限"""
    return (
        db.query(UserButtonPermission)
        .filter(UserButtonPermission.user_id == user_id)
        .all()
    )


def check_user_button_permission(db: Session, user_id: int, button_id: str) -> bool:
    """检查用户是否有特定按钮权限"""
    # 如果是超级用户，拥有所有权限
    from models.user import User

    user = db.query(User).filter(User.id == user_id).first()
    if user and user.is_superuser:
        return True

    # 检查具体权限
    permission = (
        db.query(UserButtonPermission)
        .filter(
            and_(
                UserButtonPermission.user_id == user_id,
                UserButtonPermission.button_id == button_id,
                UserButtonPermission.has_permission == True,
            )
        )
        .first()
    )

    return permission is not None
