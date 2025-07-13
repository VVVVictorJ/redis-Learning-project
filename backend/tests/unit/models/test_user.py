"""
用户模型单元测试
"""

import pytest
from sqlalchemy.orm import Session
from models.user import User
from core.security import verify_password, get_password_hash


@pytest.mark.unit
class TestUserModel:
    """用户模型测试套件"""

    def test_create_user(self, db_session: Session):
        """
        测试创建用户
        预期: 成功创建用户并设置正确的属性
        """
        # Arrange
        username = "testuser"
        email = "test@example.com"
        full_name = "Test User"
        hashed_password = get_password_hash("testpassword")

        # Act
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Assert
        assert user.id is not None
        assert user.username == username
        assert user.email == email
        assert user.full_name == full_name
        assert user.hashed_password == hashed_password
        assert user.is_active is True
        assert user.is_superuser is False

    def test_user_password_hashing(self):
        """
        测试密码哈希
        预期: 密码正确哈希并能够验证
        """
        # Arrange
        password = "testpassword"

        # Act
        hashed_password = get_password_hash(password)

        # Assert
        assert hashed_password != password
        assert verify_password(password, hashed_password) is True
        assert verify_password("wrongpassword", hashed_password) is False

    def test_user_default_values(self, db_session: Session):
        """
        测试用户默认值
        预期: is_active默认为True，is_superuser默认为False
        """
        # Arrange & Act
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpassword"),
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Assert
        assert user.is_active is True
        assert user.is_superuser is False

    def test_user_unique_constraints(self, db_session: Session):
        """
        测试用户唯一性约束
        预期: 相同用户名或邮箱的用户不能创建
        """
        # Arrange
        user1 = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpassword"),
        )
        db_session.add(user1)
        db_session.commit()

        # Act & Assert - 相同用户名
        with pytest.raises(Exception):
            user2 = User(
                username="testuser",  # 相同用户名
                email="different@example.com",
                hashed_password=get_password_hash("testpassword"),
            )
            db_session.add(user2)
            db_session.commit()

        db_session.rollback()

        # Act & Assert - 相同邮箱
        with pytest.raises(Exception):
            user3 = User(
                username="differentuser",
                email="test@example.com",  # 相同邮箱
                hashed_password=get_password_hash("testpassword"),
            )
            db_session.add(user3)
            db_session.commit()

    def test_user_relationships(self, db_session: Session):
        """
        测试用户关系
        预期: 用户与支出、菜单项、按钮权限的关系正确建立
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

        # Assert
        assert hasattr(user, "expenses")
        assert hasattr(user, "menu_items")
        assert hasattr(user, "button_permissions")
        assert user.expenses == []
        assert user.menu_items == []
        assert user.button_permissions == []
