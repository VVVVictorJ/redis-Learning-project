"""
用户Schema单元测试
"""

import pytest
from pydantic import ValidationError
from schemas.user import UserCreate, UserUpdate, User as UserSchema


@pytest.mark.unit
class TestUserCreateSchema:
    """用户创建Schema测试套件"""

    def test_valid_user_create(self):
        """
        测试有效的用户创建数据
        预期: 成功创建UserCreate实例
        """
        # Arrange
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpassword",
        }

        # Act
        user_create = UserCreate(**user_data)

        # Assert
        assert user_create.username == "testuser"
        assert user_create.email == "test@example.com"
        assert user_create.full_name == "Test User"
        assert user_create.password == "testpassword"
        assert user_create.is_superuser is False  # 默认值

    def test_user_create_with_superuser(self):
        """
        测试创建超级用户
        预期: 正确设置is_superuser字段
        """
        # Arrange
        user_data = {
            "username": "superuser",
            "email": "super@example.com",
            "password": "testpassword",
            "is_superuser": True,
        }

        # Act
        user_create = UserCreate(**user_data)

        # Assert
        assert user_create.is_superuser is True

    def test_user_create_invalid_email(self):
        """
        测试无效邮箱格式
        预期: 抛出验证错误
        """
        # Arrange
        user_data = {
            "username": "testuser",
            "email": "invalid-email",
            "password": "testpassword",
        }

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**user_data)

        assert "email" in str(exc_info.value)

    def test_user_create_missing_required_fields(self):
        """
        测试缺少必需字段
        预期: 抛出验证错误
        """
        # Act & Assert - 缺少用户名
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(email="test@example.com", password="testpassword")
        assert "username" in str(exc_info.value)

        # Act & Assert - 缺少邮箱
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(username="testuser", password="testpassword")
        assert "email" in str(exc_info.value)

        # Act & Assert - 缺少密码
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(username="testuser", email="test@example.com")
        assert "password" in str(exc_info.value)

    def test_user_create_empty_strings(self):
        """
        测试空字符串字段
        预期: 抛出验证错误
        """
        # Act & Assert - 空用户名
        with pytest.raises(ValidationError):
            UserCreate(username="", email="test@example.com", password="testpassword")

        # Act & Assert - 空邮箱
        with pytest.raises(ValidationError):
            UserCreate(username="testuser", email="", password="testpassword")

        # Act & Assert - 空密码
        with pytest.raises(ValidationError):
            UserCreate(username="testuser", email="test@example.com", password="")


@pytest.mark.unit
class TestUserUpdateSchema:
    """用户更新Schema测试套件"""

    def test_valid_user_update(self):
        """
        测试有效的用户更新数据
        预期: 成功创建UserUpdate实例
        """
        # Arrange
        update_data = {"full_name": "Updated Name", "email": "updated@example.com"}

        # Act
        user_update = UserUpdate(**update_data)

        # Assert
        assert user_update.full_name == "Updated Name"
        assert user_update.email == "updated@example.com"
        assert user_update.username is None  # 可选字段
        assert user_update.password is None  # 可选字段

    def test_user_update_all_fields(self):
        """
        测试更新所有字段
        预期: 所有字段正确设置
        """
        # Arrange
        update_data = {
            "username": "newusername",
            "email": "new@example.com",
            "full_name": "New Name",
            "password": "newpassword",
            "is_active": False,
            "is_superuser": True,
        }

        # Act
        user_update = UserUpdate(**update_data)

        # Assert
        assert user_update.username == "newusername"
        assert user_update.email == "new@example.com"
        assert user_update.full_name == "New Name"
        assert user_update.password == "newpassword"
        assert user_update.is_active is False
        assert user_update.is_superuser is True

    def test_user_update_empty_object(self):
        """
        测试空更新对象
        预期: 成功创建，所有字段为None或默认值
        """
        # Act
        user_update = UserUpdate()

        # Assert
        assert user_update.username is None
        assert user_update.email is None
        assert user_update.full_name is None
        assert user_update.password is None
        assert user_update.is_active is None
        assert user_update.is_superuser is None

    def test_user_update_invalid_email(self):
        """
        测试更新时无效邮箱格式
        预期: 抛出验证错误
        """
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            UserUpdate(email="invalid-email")

        assert "email" in str(exc_info.value)


@pytest.mark.unit
class TestUserSchema:
    """用户响应Schema测试套件"""

    def test_valid_user_schema(self):
        """
        测试有效的用户Schema
        预期: 成功创建User实例
        """
        # Arrange
        user_data = {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "is_active": True,
            "is_superuser": False,
        }

        # Act
        user = UserSchema(**user_data)

        # Assert
        assert user.id == 1
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.is_active is True
        assert user.is_superuser is False

    def test_user_schema_missing_required_fields(self):
        """
        测试缺少必需字段
        预期: 抛出验证错误
        """
        # Act & Assert - 缺少ID
        with pytest.raises(ValidationError) as exc_info:
            UserSchema(
                username="testuser",
                email="test@example.com",
                is_active=True,
                is_superuser=False,
            )
        assert "id" in str(exc_info.value)

    def test_user_schema_invalid_types(self):
        """
        测试无效的字段类型
        预期: 抛出验证错误
        """
        # Act & Assert - ID不是整数
        with pytest.raises(ValidationError):
            UserSchema(
                id="not_an_integer",
                username="testuser",
                email="test@example.com",
                is_active=True,
                is_superuser=False,
            )

        # Act & Assert - is_active不是布尔值
        with pytest.raises(ValidationError):
            UserSchema(
                id=1,
                username="testuser",
                email="test@example.com",
                is_active="not_a_boolean",
                is_superuser=False,
            )

    def test_user_schema_config(self):
        """
        测试用户Schema配置
        预期: 正确配置from_attributes
        """
        # Arrange
        user_data = {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "is_active": True,
            "is_superuser": False,
        }

        # Act
        user = UserSchema(**user_data)

        # Assert
        assert hasattr(UserSchema.model_config, "from_attributes")
        assert user.model_dump() == user_data
