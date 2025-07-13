"""
菜单模型单元测试
"""

import pytest
from sqlalchemy.orm import Session
from models.menu import MenuItem, UserMenuItem, ButtonPermission, UserButtonPermission
from models.user import User
from core.security import get_password_hash


@pytest.mark.unit
class TestMenuItemModel:
    """菜单项模型测试套件"""

    def test_create_menu_item(self, db_session: Session):
        """
        测试创建菜单项
        预期: 成功创建菜单项并设置正确的属性
        """
        # Arrange
        title = "Dashboard"
        icon = "dashboard"
        route = "/dashboard"
        order = 1

        # Act
        menu_item = MenuItem(title=title, icon=icon, route=route, order=order)
        db_session.add(menu_item)
        db_session.commit()
        db_session.refresh(menu_item)

        # Assert
        assert menu_item.id is not None
        assert menu_item.title == title
        assert menu_item.icon == icon
        assert menu_item.route == route
        assert menu_item.order == order
        assert menu_item.parent_id is None
        assert menu_item.is_active is True
        assert menu_item.created_at is not None

    def test_menu_item_default_values(self, db_session: Session):
        """
        测试菜单项默认值
        预期: order默认为0，is_active默认为True
        """
        # Arrange & Act
        menu_item = MenuItem(title="Test Menu")
        db_session.add(menu_item)
        db_session.commit()
        db_session.refresh(menu_item)

        # Assert
        assert menu_item.order == 0
        assert menu_item.is_active is True

    def test_menu_item_hierarchy(self, db_session: Session):
        """
        测试菜单项层级关系
        预期: 父子关系正确建立
        """
        # Arrange
        parent_menu = MenuItem(title="Parent Menu", order=1)
        db_session.add(parent_menu)
        db_session.commit()
        db_session.refresh(parent_menu)

        child_menu = MenuItem(title="Child Menu", parent_id=parent_menu.id, order=1)
        db_session.add(child_menu)
        db_session.commit()
        db_session.refresh(child_menu)

        # Assert
        assert child_menu.parent_id == parent_menu.id
        assert child_menu.parent == parent_menu
        assert parent_menu.children == [child_menu]

    def test_menu_item_relationships(self, db_session: Session):
        """
        测试菜单项关系
        预期: 与用户菜单权限和按钮权限的关系正确建立
        """
        # Arrange
        menu_item = MenuItem(title="Test Menu")
        db_session.add(menu_item)
        db_session.commit()
        db_session.refresh(menu_item)

        # Assert
        assert hasattr(menu_item, "user_menu_items")
        assert hasattr(menu_item, "button_permissions")
        assert menu_item.user_menu_items == []
        assert menu_item.button_permissions == []


@pytest.mark.unit
class TestUserMenuItemModel:
    """用户菜单项模型测试套件"""

    def test_create_user_menu_item(self, db_session: Session):
        """
        测试创建用户菜单项关联
        预期: 成功创建关联并设置正确的属性
        """
        # Arrange
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpassword"),
        )
        menu_item = MenuItem(title="Test Menu")

        db_session.add(user)
        db_session.add(menu_item)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(menu_item)

        # Act
        user_menu_item = UserMenuItem(
            user_id=user.id, menu_item_id=menu_item.id, has_permission=True
        )
        db_session.add(user_menu_item)
        db_session.commit()
        db_session.refresh(user_menu_item)

        # Assert
        assert user_menu_item.id is not None
        assert user_menu_item.user_id == user.id
        assert user_menu_item.menu_item_id == menu_item.id
        assert user_menu_item.has_permission is True
        assert user_menu_item.user == user
        assert user_menu_item.menu_item == menu_item

    def test_user_menu_item_default_permission(self, db_session: Session):
        """
        测试用户菜单项默认权限
        预期: has_permission默认为True
        """
        # Arrange
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpassword"),
        )
        menu_item = MenuItem(title="Test Menu")

        db_session.add(user)
        db_session.add(menu_item)
        db_session.commit()
        db_session.refresh(user)
        db_session.refresh(menu_item)

        # Act
        user_menu_item = UserMenuItem(user_id=user.id, menu_item_id=menu_item.id)
        db_session.add(user_menu_item)
        db_session.commit()
        db_session.refresh(user_menu_item)

        # Assert
        assert user_menu_item.has_permission is True


@pytest.mark.unit
class TestButtonPermissionModel:
    """按钮权限模型测试套件"""

    def test_create_button_permission(self, db_session: Session):
        """
        测试创建按钮权限
        预期: 成功创建按钮权限并设置正确的属性
        """
        # Arrange
        menu_item = MenuItem(title="Test Menu")
        db_session.add(menu_item)
        db_session.commit()
        db_session.refresh(menu_item)

        button_id = "test_button"
        description = "Test Button"

        # Act
        button_permission = ButtonPermission(
            button_id=button_id, description=description, menu_item_id=menu_item.id
        )
        db_session.add(button_permission)
        db_session.commit()
        db_session.refresh(button_permission)

        # Assert
        assert button_permission.id is not None
        assert button_permission.button_id == button_id
        assert button_permission.description == description
        assert button_permission.menu_item_id == menu_item.id
        assert button_permission.menu_item == menu_item

    def test_button_permission_unique_button_id(self, db_session: Session):
        """
        测试按钮权限button_id唯一性
        预期: 相同button_id的按钮权限不能创建
        """
        # Arrange
        menu_item = MenuItem(title="Test Menu")
        db_session.add(menu_item)
        db_session.commit()
        db_session.refresh(menu_item)

        button_permission1 = ButtonPermission(
            button_id="test_button", menu_item_id=menu_item.id
        )
        db_session.add(button_permission1)
        db_session.commit()

        # Act & Assert
        with pytest.raises(Exception):
            button_permission2 = ButtonPermission(
                button_id="test_button", menu_item_id=menu_item.id  # 相同button_id
            )
            db_session.add(button_permission2)
            db_session.commit()


@pytest.mark.unit
class TestUserButtonPermissionModel:
    """用户按钮权限模型测试套件"""

    def test_create_user_button_permission(self, db_session: Session):
        """
        测试创建用户按钮权限
        预期: 成功创建关联并设置正确的属性
        """
        # Arrange
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpassword"),
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        button_id = "test_button"

        # Act
        user_button_permission = UserButtonPermission(
            user_id=user.id, button_id=button_id, has_permission=True
        )
        db_session.add(user_button_permission)
        db_session.commit()
        db_session.refresh(user_button_permission)

        # Assert
        assert user_button_permission.id is not None
        assert user_button_permission.user_id == user.id
        assert user_button_permission.button_id == button_id
        assert user_button_permission.has_permission is True
        assert user_button_permission.user == user

    def test_user_button_permission_default_value(self, db_session: Session):
        """
        测试用户按钮权限默认值
        预期: has_permission默认为False
        """
        # Arrange
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpassword"),
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Act
        user_button_permission = UserButtonPermission(
            user_id=user.id, button_id="test_button"
        )
        db_session.add(user_button_permission)
        db_session.commit()
        db_session.refresh(user_button_permission)

        # Assert
        assert user_button_permission.has_permission is False

    def test_user_button_permission_unique_constraint(self, db_session: Session):
        """
        测试用户按钮权限唯一性约束
        预期: 相同用户和按钮的权限记录不能重复创建
        """
        # Arrange
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpassword"),
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        user_button_permission1 = UserButtonPermission(
            user_id=user.id, button_id="test_button", has_permission=True
        )
        db_session.add(user_button_permission1)
        db_session.commit()

        # Act & Assert
        with pytest.raises(Exception):
            user_button_permission2 = UserButtonPermission(
                user_id=user.id,
                button_id="test_button",  # 相同用户和按钮
                has_permission=False,
            )
            db_session.add(user_button_permission2)
            db_session.commit()
