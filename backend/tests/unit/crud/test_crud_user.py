"""
用户CRUD操作单元测试
"""

import pytest
from sqlalchemy.orm import Session
from crud import crud_user
from schemas.user import UserCreate, UserUpdate
from models.user import User
from core.security import verify_password


@pytest.mark.unit
class TestCRUDUser:
    """用户CRUD操作测试套件"""

    def test_create_user(self, db_session: Session):
        """
        测试创建用户
        预期: 成功创建用户并正确设置属性
        """
        # Arrange
        user_in = UserCreate(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            password="testpassword",
        )

        # Act
        user = crud_user.user.create(db_session, obj_in=user_in)

        # Assert
        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.hashed_password is not None
        assert user.hashed_password != "testpassword"  # 密码应该被哈希
        assert verify_password("testpassword", user.hashed_password)
        assert user.is_active is True
        assert user.is_superuser is False

    def test_create_superuser(self, db_session: Session):
        """
        测试创建超级用户
        预期: 正确设置超级用户标志
        """
        # Arrange
        user_in = UserCreate(
            username="superuser",
            email="super@example.com",
            password="testpassword",
            is_superuser=True,
        )

        # Act
        user = crud_user.create_user(db_session, obj_in=user_in, is_superuser=True)

        # Assert
        assert user.is_superuser is True

    def test_get_user_by_id(self, db_session: Session, test_user: User):
        """
        测试通过ID获取用户
        预期: 返回正确的用户
        """
        # Act
        user = crud_user.user.get(db_session, id=test_user.id)

        # Assert
        assert user is not None
        assert user.id == test_user.id
        assert user.email == test_user.email

    def test_get_user_by_id_not_found(self, db_session: Session):
        """
        测试获取不存在的用户
        预期: 返回None
        """
        # Act
        user = crud_user.user.get(db_session, id=999)

        # Assert
        assert user is None

    def test_get_user_by_email(self, db_session: Session, test_user: User):
        """
        测试通过邮箱获取用户
        预期: 返回正确的用户
        """
        # Act
        user = crud_user.user.get_by_email(db_session, email=test_user.email)

        # Assert
        assert user is not None
        assert user.id == test_user.id
        assert user.email == test_user.email

    def test_get_user_by_email_not_found(self, db_session: Session):
        """
        测试获取不存在邮箱的用户
        预期: 返回None
        """
        # Act
        user = crud_user.user.get_by_email(db_session, email="nonexistent@example.com")

        # Assert
        assert user is None

    def test_get_user_by_username(self, db_session: Session, test_user: User):
        """
        测试通过用户名获取用户
        预期: 返回正确的用户
        """
        # Act
        user = crud_user.get_user_by_username(db_session, username=test_user.username)

        # Assert
        assert user is not None
        assert user.id == test_user.id
        assert user.username == test_user.username

    def test_get_users(self, db_session: Session):
        """
        测试获取用户列表
        预期: 返回用户列表
        """
        # Arrange - 创建多个用户
        users_data = [
            UserCreate(
                username=f"user{i}",
                email=f"user{i}@example.com",
                password="testpassword",
            )
            for i in range(3)
        ]
        created_users = [
            crud_user.user.create(db_session, obj_in=user_data)
            for user_data in users_data
        ]

        # Act
        users = crud_user.user.get_multi(db_session, skip=0, limit=10)

        # Assert
        assert len(users) == 3
        assert all(user.id is not None for user in users)

    def test_get_users_with_pagination(self, db_session: Session):
        """
        测试分页获取用户列表
        预期: 正确应用分页参数
        """
        # Arrange - 创建5个用户
        users_data = [
            UserCreate(
                username=f"user{i}",
                email=f"user{i}@example.com",
                password="testpassword",
            )
            for i in range(5)
        ]
        for user_data in users_data:
            crud_user.user.create(db_session, obj_in=user_data)

        # Act
        users_page1 = crud_user.user.get_multi(db_session, skip=0, limit=2)
        users_page2 = crud_user.user.get_multi(db_session, skip=2, limit=2)

        # Assert
        assert len(users_page1) == 2
        assert len(users_page2) == 2
        assert users_page1[0].id != users_page2[0].id

    def test_authenticate_user_success(self, db_session: Session, test_user: User):
        """
        测试用户认证成功
        预期: 返回用户对象
        """
        # Act
        authenticated_user = crud_user.authenticate_user(
            db_session, email=test_user.email, password="testpassword"
        )

        # Assert
        assert authenticated_user is not None
        assert authenticated_user.id == test_user.id
        assert authenticated_user.email == test_user.email

    def test_authenticate_user_wrong_password(
        self, db_session: Session, test_user: User
    ):
        """
        测试用户认证失败 - 错误密码
        预期: 返回None
        """
        # Act
        authenticated_user = crud_user.authenticate_user(
            db_session, email=test_user.email, password="wrongpassword"
        )

        # Assert
        assert authenticated_user is None

    def test_authenticate_user_wrong_email(self, db_session: Session):
        """
        测试用户认证失败 - 错误邮箱
        预期: 返回None
        """
        # Act
        authenticated_user = crud_user.authenticate_user(
            db_session, email="nonexistent@example.com", password="testpassword"
        )

        # Assert
        assert authenticated_user is None

    def test_is_active_user(self, test_user: User):
        """
        测试检查用户是否激活
        预期: 返回True
        """
        # Act
        result = crud_user.is_active(test_user)

        # Assert
        assert result is True

    def test_is_active_inactive_user(self, db_session: Session):
        """
        测试检查非激活用户
        预期: 返回False
        """
        # Arrange
        user_in = UserCreate(
            username="inactiveuser",
            email="inactive@example.com",
            password="testpassword",
        )
        user = crud_user.user.create(db_session, obj_in=user_in)
        user.is_active = False
        db_session.commit()

        # Act
        result = crud_user.is_active(user)

        # Assert
        assert result is False

    def test_is_superuser(self, test_superuser: User):
        """
        测试检查超级用户
        预期: 返回True
        """
        # Act
        result = crud_user.user.is_superuser(test_superuser)

        # Assert
        assert result is True

    def test_is_not_superuser(self, test_user: User):
        """
        测试检查普通用户
        预期: 返回False
        """
        # Act
        result = crud_user.user.is_superuser(test_user)

        # Assert
        assert result is False

    def test_create_user_duplicate_email(self, db_session: Session, test_user: User):
        """
        测试创建重复邮箱用户
        预期: 应该处理重复邮箱的情况
        """
        # Arrange
        user_in = UserCreate(
            username="newuser",
            email=test_user.email,  # 使用已存在的邮箱
            password="testpassword",
        )

        # Act & Assert
        # 这里的行为取决于具体的实现
        # 如果CRUD层有重复检查，应该抛出异常或返回None
        # 如果没有，数据库层会抛出完整性错误
        with pytest.raises(Exception):
            crud_user.user.create(db_session, obj_in=user_in)

    def test_password_hashing(self, db_session: Session):
        """
        测试密码哈希功能
        预期: 密码正确哈希并能验证
        """
        # Arrange
        password = "testpassword"

        # Act
        hashed_password = crud_user.get_password_hash(password)

        # Assert
        assert hashed_password != password
        assert verify_password(password, hashed_password) is True
        assert verify_password("wrongpassword", hashed_password) is False
