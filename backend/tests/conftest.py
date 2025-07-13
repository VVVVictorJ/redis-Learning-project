"""
全局测试配置文件
提供测试所需的基础夹具和配置
"""

import os
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# 设置测试环境变量
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("REDIS_HOST", "localhost")
os.environ.setdefault("REDIS_PORT", "6379")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
os.environ.setdefault("FIRST_SUPERUSER", "admin@example.com")
os.environ.setdefault("FIRST_SUPERUSER_PASSWORD", "adminpassword")

from main import app
from db.base import Base
from db.session import get_db
from models.user import User
from models.expense import Expense
from models.menu import MenuItem, UserMenuItem, ButtonPermission, UserButtonPermission
from crud import crud_user
from schemas.user import UserCreate
from core.security import get_password_hash


# 测试数据库URL - 使用SQLite内存数据库
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# 同步数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    同步数据库会话夹具
    每个测试函数都会获得一个独立的数据库会话
    """
    # 创建表
    Base.metadata.create_all(bind=engine)

    # 创建会话
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # 清理表
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    FastAPI测试客户端夹具
    自动注入测试数据库会话
    """

    def get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = get_test_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# 用户相关夹具
@pytest.fixture
def test_user(db_session: Session) -> User:
    """创建测试用户"""
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        password="testpassword",
    )
    user = crud_user.user.create(db_session, obj_in=user_data)
    return user


@pytest.fixture
def test_superuser(db_session: Session) -> User:
    """创建测试超级用户"""
    user_data = UserCreate(
        username="testsuperuser",
        email="superuser@example.com",
        full_name="Test Super User",
        password="testpassword",
        is_superuser=True,
    )
    user = crud_user.user.create(db_session, obj_in=user_data)
    return user


# 菜单相关夹具
@pytest.fixture
def test_menu_item(db_session: Session) -> MenuItem:
    """创建测试菜单项"""
    menu_item = MenuItem(title="Test Menu", icon="test-icon", route="/test", order=1)
    db_session.add(menu_item)
    db_session.commit()
    db_session.refresh(menu_item)
    return menu_item


@pytest.fixture
def test_button_permission(
    db_session: Session, test_menu_item: MenuItem
) -> ButtonPermission:
    """创建测试按钮权限"""
    button_permission = ButtonPermission(
        button_id="test_button",
        description="Test Button",
        menu_item_id=test_menu_item.id,
    )
    db_session.add(button_permission)
    db_session.commit()
    db_session.refresh(button_permission)
    return button_permission


# 支出相关夹具
@pytest.fixture
def test_expense(db_session: Session, test_user: User) -> Expense:
    """创建测试支出"""
    expense = Expense(
        title="Test Expense",
        amount=100.50,
        description="Test expense description",
        owner_id=test_user.id,
    )
    db_session.add(expense)
    db_session.commit()
    db_session.refresh(expense)
    return expense


# 认证相关夹具
@pytest.fixture
def auth_headers(client: TestClient, test_user: User) -> dict:
    """获取认证头"""
    login_data = {"username": test_user.email, "password": "testpassword"}
    response = client.post("/api/v1/login/access-token", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def superuser_auth_headers(client: TestClient, test_superuser: User) -> dict:
    """获取超级用户认证头"""
    login_data = {"username": test_superuser.email, "password": "testpassword"}
    response = client.post("/api/v1/login/access-token", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
