from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api import deps
from crud import crud_menu
from models.user import User
from schemas.menu import (
    MenuItem,
    MenuItemCreate,
    MenuItemUpdate,
    ButtonPermission,
    ButtonPermissionCreate,
    UserMenuResponse,
    SetUserMenuPermissions,
    SetUserButtonPermissions,
    UserButtonPermission as UserButtonPermissionSchema,
)

router = APIRouter()


# 菜单项管理端点
@router.get("/", response_model=List[MenuItem])
def read_menu_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    include_inactive: bool = False,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    获取所有菜单项（仅超级用户）
    """
    menu_items = crud_menu.get_menu_items(
        db, skip=skip, limit=limit, include_inactive=include_inactive
    )
    return menu_items


@router.post("/", response_model=MenuItem)
def create_menu_item(
    *,
    db: Session = Depends(deps.get_db),
    menu_item_in: MenuItemCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    创建新菜单项（仅超级用户）
    """
    menu_item = crud_menu.create_menu_item(db, menu_item=menu_item_in)
    return menu_item


@router.get("/{menu_id}", response_model=MenuItem)
def read_menu_item(
    menu_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    获取单个菜单项详情（仅超级用户）
    """
    menu_item = crud_menu.get_menu_item(db, menu_item_id=menu_id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return menu_item


@router.put("/{menu_id}", response_model=MenuItem)
def update_menu_item(
    *,
    db: Session = Depends(deps.get_db),
    menu_id: int,
    menu_item_in: MenuItemUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    更新菜单项（仅超级用户）
    """
    menu_item = crud_menu.update_menu_item(
        db, menu_item_id=menu_id, menu_item_update=menu_item_in
    )
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return menu_item


@router.delete("/{menu_id}")
def delete_menu_item(
    menu_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    删除菜单项（仅超级用户）
    """
    success = crud_menu.delete_menu_item(db, menu_item_id=menu_id)
    if not success:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return {"message": "Menu item deleted successfully"}


# 按钮权限管理端点
@router.get("/buttons/", response_model=List[ButtonPermission])
def read_button_permissions(
    db: Session = Depends(deps.get_db),
    menu_item_id: int = None,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    获取按钮权限（仅超级用户）
    """
    button_permissions = crud_menu.get_button_permissions(db, menu_item_id=menu_item_id)
    return button_permissions


@router.post("/buttons/", response_model=ButtonPermission)
def create_button_permission(
    *,
    db: Session = Depends(deps.get_db),
    button_permission_in: ButtonPermissionCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    创建按钮权限（仅超级用户）
    """
    button_permission = crud_menu.create_button_permission(
        db, button_permission=button_permission_in
    )
    return button_permission


# 用户菜单权限端点
@router.get("/users/me/menus", response_model=List[UserMenuResponse])
def read_current_user_menus(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取当前用户的菜单
    """
    accessible_menus = crud_menu.get_user_accessible_menus(db, user_id=current_user.id)

    # 构建层次结构并添加按钮权限
    def build_menu_tree(menus: List[Any]) -> List[UserMenuResponse]:
        result = []
        for menu in menus:
            # 获取用户按钮权限
            user_button_perms = crud_menu.get_user_button_permissions(
                db, user_id=current_user.id
            )
            button_perms_dict = {
                perm.button_id: perm.has_permission for perm in user_button_perms
            }

            # 获取菜单相关的按钮
            menu_buttons = crud_menu.get_button_permissions(db, menu_item_id=menu.id)
            buttons = [
                UserButtonPermissionSchema(
                    button_id=btn.button_id,
                    has_permission=button_perms_dict.get(btn.button_id, False),
                )
                for btn in menu_buttons
            ]

            menu_response = UserMenuResponse(
                id=menu.id,
                title=menu.title,
                icon=menu.icon,
                route=menu.route,
                order=menu.order,
                children=build_menu_tree(menu.children),
                buttons=buttons,
            )
            result.append(menu_response)

        return result

    return build_menu_tree(accessible_menus)


@router.get("/users/{user_id}/menus", response_model=List[UserMenuResponse])
def read_user_menu_permissions(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    获取用户菜单权限（仅超级用户）
    """
    accessible_menus = crud_menu.get_user_accessible_menus(db, user_id=user_id)

    # 构建层次结构并添加按钮权限
    def build_menu_tree(menus: List[Any]) -> List[UserMenuResponse]:
        result = []
        for menu in menus:
            # 获取用户按钮权限
            user_button_perms = crud_menu.get_user_button_permissions(
                db, user_id=user_id
            )
            button_perms_dict = {
                perm.button_id: perm.has_permission for perm in user_button_perms
            }

            # 获取菜单相关的按钮
            menu_buttons = crud_menu.get_button_permissions(db, menu_item_id=menu.id)
            buttons = [
                UserButtonPermissionSchema(
                    button_id=btn.button_id,
                    has_permission=button_perms_dict.get(btn.button_id, False),
                )
                for btn in menu_buttons
            ]

            menu_response = UserMenuResponse(
                id=menu.id,
                title=menu.title,
                icon=menu.icon,
                route=menu.route,
                order=menu.order,
                children=build_menu_tree(menu.children),
                buttons=buttons,
            )
            result.append(menu_response)

        return result

    return build_menu_tree(accessible_menus)


@router.post("/users/{user_id}/menus")
def set_user_menu_permissions(
    user_id: int,
    permissions: SetUserMenuPermissions,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    设置用户菜单权限（仅超级用户）
    """
    success = crud_menu.set_user_menu_permissions(
        db, user_id=user_id, menu_permissions=permissions.menu_permissions
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to set menu permissions")
    return {"message": "Menu permissions updated successfully"}


# 用户按钮权限端点
@router.get("/users/{user_id}/buttons", response_model=List[UserButtonPermissionSchema])
def read_user_button_permissions(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    获取用户按钮权限（仅超级用户）
    """
    user_button_perms = crud_menu.get_user_button_permissions(db, user_id=user_id)
    return [
        UserButtonPermissionSchema(
            button_id=perm.button_id,
            has_permission=perm.has_permission,
        )
        for perm in user_button_perms
    ]


@router.post("/users/{user_id}/buttons")
def set_user_button_permissions(
    user_id: int,
    permissions: SetUserButtonPermissions,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    设置用户按钮权限（仅超级用户）
    """
    success = crud_menu.set_user_button_permissions(
        db, user_id=user_id, button_permissions=permissions.button_permissions
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to set button permissions")
    return {"message": "Button permissions updated successfully"}


@router.get("/users/me/buttons/{button_id}/check")
def check_current_user_button_permission(
    button_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    检查当前用户是否有特定按钮权限
    """
    has_permission = crud_menu.check_user_button_permission(
        db, user_id=current_user.id, button_id=button_id
    )
    return {"has_permission": has_permission}
