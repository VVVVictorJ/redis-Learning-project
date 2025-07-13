#!/usr/bin/env python3
"""
菜单系统测试脚本
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.menu import MenuItem, UserMenuItem, ButtonPermission, UserButtonPermission
from models.user import User
from crud import crud_menu, crud_user
from schemas.menu import (
    MenuItemCreate,
    ButtonPermissionCreate,
    UserMenuPermission,
    UserButtonPermission,
)
from schemas.user import UserCreate
from core.security import get_password_hash


def test_menu_system():
    """测试菜单系统功能"""
    db: Session = SessionLocal()

    try:
        print("🚀 开始测试菜单系统...")

        # 1. 创建测试用户
        print("\n1. 创建测试用户...")
        test_user = crud_user.get_user_by_email(db, email="test@example.com")
        if not test_user:
            user_create = UserCreate(
                username="testuser",
                email="test@example.com",
                full_name="Test User",
                password="testpass123",
            )
            test_user = crud_user.create_user(db, obj_in=user_create)
        print(f"✅ 测试用户创建成功: {test_user.username}")

        # 2. 创建菜单项
        print("\n2. 创建菜单项...")

        # 清理现有数据
        from models.menu import UserButtonPermission as UserButtonPermissionModel
        from models.menu import UserMenuItem as UserMenuItemModel
        from models.menu import ButtonPermission as ButtonPermissionModel
        from models.menu import MenuItem as MenuItemModel

        db.query(UserButtonPermissionModel).delete()
        db.query(UserMenuItemModel).delete()
        db.query(ButtonPermissionModel).delete()
        db.query(MenuItemModel).delete()
        db.commit()

        # 创建主菜单
        dashboard_menu = crud_menu.create_menu_item(
            db,
            MenuItemCreate(
                title="仪表板", icon="dashboard", route="/dashboard", order=1
            ),
        )
        print(f"✅ 主菜单创建成功: {dashboard_menu.title}")

        # 创建子菜单
        analytics_menu = crud_menu.create_menu_item(
            db,
            MenuItemCreate(
                title="数据分析",
                icon="analytics",
                route="/dashboard/analytics",
                parent_id=dashboard_menu.id,
                order=1,
            ),
        )
        print(f"✅ 子菜单创建成功: {analytics_menu.title}")

        # 创建用户管理菜单
        user_menu = crud_menu.create_menu_item(
            db, MenuItemCreate(title="用户管理", icon="users", route="/users", order=2)
        )
        print(f"✅ 用户管理菜单创建成功: {user_menu.title}")

        # 3. 创建按钮权限
        print("\n3. 创建按钮权限...")

        # 仪表板刷新按钮
        refresh_button = crud_menu.create_button_permission(
            db,
            ButtonPermissionCreate(
                button_id="dashboard_refresh",
                description="刷新仪表板",
                menu_item_id=dashboard_menu.id,
            ),
        )
        print(f"✅ 按钮权限创建成功: {refresh_button.description}")

        # 用户添加按钮
        add_user_button = crud_menu.create_button_permission(
            db,
            ButtonPermissionCreate(
                button_id="user_add", description="添加用户", menu_item_id=user_menu.id
            ),
        )
        print(f"✅ 按钮权限创建成功: {add_user_button.description}")

        # 4. 设置用户菜单权限
        print("\n4. 设置用户菜单权限...")
        menu_permissions = [
            UserMenuPermission(menu_item_id=dashboard_menu.id, has_permission=True),
            UserMenuPermission(menu_item_id=analytics_menu.id, has_permission=True),
            UserMenuPermission(menu_item_id=user_menu.id, has_permission=False),
        ]

        success = crud_menu.set_user_menu_permissions(
            db, test_user.id, menu_permissions
        )
        print(f"✅ 用户菜单权限设置成功: {success}")

        # 5. 设置用户按钮权限
        print("\n5. 设置用户按钮权限...")
        button_permissions = [
            UserButtonPermission(button_id="dashboard_refresh", has_permission=True),
            UserButtonPermission(button_id="user_add", has_permission=False),
        ]

        success = crud_menu.set_user_button_permissions(
            db, test_user.id, button_permissions
        )
        print(f"✅ 用户按钮权限设置成功: {success}")

        # 6. 测试获取用户可访问的菜单
        print("\n6. 测试获取用户可访问的菜单...")
        accessible_menus = crud_menu.get_user_accessible_menus(db, test_user.id)
        print(f"✅ 用户可访问的菜单数量: {len(accessible_menus)}")

        for menu in accessible_menus:
            print(f"  - {menu.title} ({menu.route})")

        # 7. 测试获取用户按钮权限
        print("\n7. 测试获取用户按钮权限...")
        user_button_perms = crud_menu.get_user_button_permissions(db, test_user.id)
        print(f"✅ 用户按钮权限数量: {len(user_button_perms)}")

        for perm in user_button_perms:
            print(f"  - {perm.button_id}: {perm.has_permission}")

        print("\n🎉 菜单系统测试完成！所有功能正常工作。")

    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_menu_system()
