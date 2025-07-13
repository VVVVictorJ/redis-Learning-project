#!/usr/bin/env python3
"""
简单的测试验证脚本
验证我们创建的测试是否能正常运行
"""
import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置环境变量
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("REDIS_HOST", "localhost")
os.environ.setdefault("REDIS_PORT", "6379")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
os.environ.setdefault("FIRST_SUPERUSER", "admin@example.com")
os.environ.setdefault("FIRST_SUPERUSER_PASSWORD", "adminpassword")


def test_password_hashing():
    """测试密码哈希功能"""
    print("Testing password hashing...")

    from core.security import get_password_hash, verify_password

    password = "testpassword"
    hashed = get_password_hash(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

    print("✅ Password hashing test passed")


def test_user_schema():
    """测试用户Schema"""
    print("Testing user schema...")

    from schemas.user import UserCreate, User as UserSchema

    # 测试UserCreate
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword",
    }

    user_create = UserCreate(**user_data)
    assert user_create.username == "testuser"
    assert user_create.email == "test@example.com"
    assert user_create.is_superuser is False

    # 测试User响应Schema
    response_data = {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "is_active": True,
        "is_superuser": False,
    }

    user_response = UserSchema(**response_data)
    assert user_response.id == 1
    assert user_response.username == "testuser"

    print("✅ User schema test passed")


def test_menu_model():
    """测试菜单模型"""
    print("Testing menu model...")

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from db.base import Base
    from models.menu import MenuItem

    # 创建内存数据库
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = SessionLocal()

    # 创建菜单项
    menu_item = MenuItem(title="Test Menu", icon="test-icon", route="/test", order=1)

    session.add(menu_item)
    session.commit()
    session.refresh(menu_item)

    assert menu_item.id is not None
    assert menu_item.title == "Test Menu"
    assert menu_item.is_active is True
    assert menu_item.order == 1

    session.close()
    print("✅ Menu model test passed")


def test_api_creation():
    """测试API创建"""
    print("Testing API creation...")

    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app)

    # 测试根端点
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

    print("✅ API creation test passed")


def test_crud_operations():
    """测试CRUD操作"""
    print("Testing CRUD operations...")

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from db.base import Base
    from crud import crud_user
    from schemas.user import UserCreate

    # 创建内存数据库
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = SessionLocal()

    # 创建用户
    user_data = UserCreate(
        username="cruduser", email="crud@example.com", password="testpassword"
    )

    user = crud_user.user.create(session, obj_in=user_data)
    assert user.id is not None
    assert user.username == "cruduser"

    # 获取用户
    retrieved_user = crud_user.user.get(session, id=user.id)
    assert retrieved_user is not None
    assert retrieved_user.email == "crud@example.com"

    # 通过邮箱获取用户
    user_by_email = crud_user.user.get_by_email(session, email="crud@example.com")
    assert user_by_email is not None
    assert user_by_email.id == user.id

    session.close()
    print("✅ CRUD operations test passed")


def run_all_tests():
    """运行所有测试"""
    print("🚀 Running all simple tests...\n")

    tests = [
        test_password_hashing,
        test_user_schema,
        test_menu_model,
        test_api_creation,
        test_crud_operations,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            import traceback

            traceback.print_exc()
            failed += 1
        print()

    print(f"📊 Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
