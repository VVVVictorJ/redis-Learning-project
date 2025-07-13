"""
修复后的测试配置文件
解决用户重复创建和认证问题
"""

import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from db.base import Base
from db.session import get_db
from models.user import User
from crud.crud_user import get_password_hash
import uuid

# 设置测试环境变量
os.environ["TESTING"] = "1"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

# 创建测试数据库引擎
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建测试数据库表
Base.metadata.create_all(bind=engine)


def override_get_db():
    """测试数据库依赖覆盖"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    """数据库会话夹具"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        # 清理测试数据
        db.query(User).delete()
        db.commit()
        db.close()


@pytest.fixture(scope="function")
def client():
    """测试客户端夹具"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def unique_email():
    """生成唯一邮箱地址"""
    return f"test_{uuid.uuid4().hex[:8]}@example.com"


@pytest.fixture
def test_user(db_session, unique_email):
    """创建测试用户"""
    user = User(
        username=unique_email,
        email=unique_email,
        full_name="Test User",
        hashed_password=get_password_hash("testpassword"),
        is_active=True,
        is_superuser=False,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_superuser(db_session):
    """创建测试超级用户"""
    email = f"admin_{uuid.uuid4().hex[:8]}@example.com"
    user = User(
        username=email,
        email=email,
        full_name="Super User",
        hashed_password=get_password_hash("testpassword"),
        is_active=True,
        is_superuser=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(client: TestClient, test_user: User) -> dict:
    """获取认证头"""
    login_data = {"username": test_user.email, "password": "testpassword"}
    response = client.post("/api/v1/login/access-token", data=login_data)

    if response.status_code == 200:
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    else:
        # 如果登录失败，返回空头部，让测试自行处理
        return {}


@pytest.fixture
def superuser_auth_headers(client: TestClient, test_superuser: User) -> dict:
    """获取超级用户认证头"""
    login_data = {"username": test_superuser.email, "password": "testpassword"}
    response = client.post("/api/v1/login/access-token", data=login_data)

    if response.status_code == 200:
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    else:
        # 如果登录失败，返回空头部，让测试自行处理
        return {}


# 清理函数
def cleanup_test_db():
    """清理测试数据库"""
    db = TestingSessionLocal()
    try:
        db.query(User).delete()
        db.commit()
    finally:
        db.close()


# 在测试会话结束时清理
@pytest.fixture(scope="session", autouse=True)
def cleanup():
    """自动清理夹具"""
    yield
    cleanup_test_db()
