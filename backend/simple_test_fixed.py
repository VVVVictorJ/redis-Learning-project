#!/usr/bin/env python3
"""
简化测试脚本 - 修复版本
测试核心功能是否正常工作
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_password_hashing():
    """测试密码哈希功能"""
    try:
        from crud.crud_user import get_password_hash, pwd_context

        password = "testpassword"
        hashed = get_password_hash(password)

        # 验证哈希不等于原密码
        assert hashed != password
        # 验证可以验证密码
        assert pwd_context.verify(password, hashed)

        print("✅ 密码哈希功能正常")
        return True
    except Exception as e:
        print(f"❌ 密码哈希测试失败: {e}")
        return False


def test_user_schemas():
    """测试用户Schema"""
    try:
        from schemas.user import UserCreate, User

        # 测试UserCreate
        user_create_data = {
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User",
        }
        user_create = UserCreate(**user_create_data)
        assert user_create.email == "test@example.com"
        assert user_create.password == "testpassword"

        # 测试User响应Schema
        user_data = {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "is_active": True,
            "is_superuser": False,
        }
        user = User(**user_data)
        assert user.id == 1
        assert user.email == "test@example.com"

        print("✅ 用户Schema验证正常")
        return True
    except Exception as e:
        print(f"❌ 用户Schema测试失败: {e}")
        return False


def test_database_models():
    """测试数据库模型"""
    try:
        from models.user import User
        from crud.crud_user import get_password_hash

        # 创建用户实例
        user = User(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            hashed_password=get_password_hash("testpassword"),
            is_active=True,
            is_superuser=False,
        )

        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.is_active == True

        print("✅ 数据库模型创建正常")
        return True
    except Exception as e:
        print(f"❌ 数据库模型测试失败: {e}")
        return False


def test_api_structure():
    """测试API结构"""
    try:
        from main import app
        from fastapi.testclient import TestClient

        client = TestClient(app)

        # 测试根端点
        response = client.get("/")
        assert response.status_code == 200
        assert "Welcome" in response.json()["message"]

        # 测试API文档端点
        response = client.get("/docs")
        assert response.status_code == 200

        print("✅ API结构正常")
        return True
    except Exception as e:
        print(f"❌ API结构测试失败: {e}")
        return False


def test_user_creation_api():
    """测试用户创建API"""
    try:
        from main import app
        from fastapi.testclient import TestClient

        client = TestClient(app)

        # 测试创建用户
        user_data = {
            "email": "apitest@example.com",
            "password": "testpassword",
            "full_name": "API Test User",
        }

        response = client.post("/api/v1/users/", json=user_data)

        # 应该返回200或201
        assert response.status_code in [200, 201]
        response_data = response.json()
        assert response_data["email"] == "apitest@example.com"
        assert "password" not in response_data  # 密码不应该返回

        print("✅ 用户创建API正常")
        return True
    except Exception as e:
        print(f"❌ 用户创建API测试失败: {e}")
        return False


def test_login_api():
    """测试登录API"""
    try:
        from main import app
        from fastapi.testclient import TestClient

        client = TestClient(app)

        # 先创建用户
        user_data = {
            "email": "logintest@example.com",
            "password": "testpassword",
            "full_name": "Login Test User",
        }
        create_response = client.post("/api/v1/users/", json=user_data)
        assert create_response.status_code in [200, 201]

        # 测试登录
        login_data = {"username": "logintest@example.com", "password": "testpassword"}

        response = client.post("/api/v1/login/access-token", data=login_data)

        if response.status_code == 200:
            response_data = response.json()
            assert "access_token" in response_data
            assert response_data["token_type"] == "bearer"
            print("✅ 登录API正常")
            return True
        else:
            print(f"⚠️ 登录API返回状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False

    except Exception as e:
        print(f"❌ 登录API测试失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("开始运行简化测试...")
    print("=" * 50)

    tests = [
        test_password_hashing,
        test_user_schemas,
        test_database_models,
        test_api_structure,
        test_user_creation_api,
        test_login_api,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    print(f"测试结果: {passed}/{total} 通过 ({passed/total*100:.1f}%)")

    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print(f"⚠️ {total - passed} 个测试失败")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
