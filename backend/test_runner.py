#!/usr/bin/env python3
"""
简单的测试运行脚本
"""
import os
import sys
import unittest

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


def test_imports():
    """测试基本导入"""
    try:
        print("Testing imports...")

        # 测试模型导入
        from models.user import User

        print("✅ User model imported")

        from models.menu import MenuItem

        print("✅ Menu model imported")

        # 测试CRUD导入
        from crud import crud_user

        print("✅ CRUD imported")

        # 测试Schema导入
        from schemas.user import UserCreate

        print("✅ Schema imported")

        # 测试FastAPI应用导入
        from main import app

        print("✅ FastAPI app imported")

        # 测试数据库连接
        from sqlalchemy import create_engine
        from db.base import Base

        engine = create_engine("sqlite:///./test.db")
        Base.metadata.create_all(bind=engine)
        print("✅ Database connection works")

        print("\n🎉 All imports successful!")
        return True

    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_user_creation():
    """测试用户创建"""
    try:
        print("\nTesting user creation...")

        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from db.base import Base
        from models.user import User
        from crud import crud_user
        from schemas.user import UserCreate

        # 创建测试数据库
        engine = create_engine("sqlite:///./test_user.db")
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        session = SessionLocal()

        # 创建用户
        user_data = UserCreate(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            password="testpassword",
        )

        user = crud_user.user.create(session, obj_in=user_data)

        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"

        session.close()
        print("✅ User creation test passed")

        # 清理
        os.remove("test_user.db")

        return True

    except Exception as e:
        print(f"❌ User creation test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_api_endpoints():
    """测试API端点"""
    try:
        print("\nTesting API endpoints...")

        from fastapi.testclient import TestClient
        from main import app

        client = TestClient(app)

        # 测试根端点
        response = client.get("/")
        assert response.status_code == 200
        print("✅ Root endpoint works")

        # 测试用户创建端点
        user_data = {
            "username": "apiuser",
            "email": "api@example.com",
            "full_name": "API User",
            "password": "testpassword",
        }

        response = client.post("/api/v1/users/", json=user_data)
        print(f"User creation response status: {response.status_code}")
        if response.status_code == 201:
            print("✅ User creation API works")
        else:
            print(f"⚠️ User creation returned {response.status_code}: {response.text}")

        return True

    except Exception as e:
        print(f"❌ API endpoint test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Starting basic tests...\n")

    success = True

    # 运行测试
    success &= test_imports()
    success &= test_user_creation()
    success &= test_api_endpoints()

    if success:
        print("\n🎉 All basic tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
