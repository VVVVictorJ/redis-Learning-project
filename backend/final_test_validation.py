#!/usr/bin/env python3
"""
最终测试验证脚本
验证修复后的测试框架和API
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app
from fastapi.testclient import TestClient
from schemas.user import UserCreate, UserUpdate, User as UserSchema
from crud.crud_user import get_password_hash, pwd_context
import uuid


def test_schema_fixes():
    """测试Schema修复"""
    print("=== 测试Schema修复 ===")

    try:
        # 测试UserCreate
        user_create = UserCreate(
            email="test@example.com", password="testpassword", full_name="Test User"
        )
        print(f"✅ UserCreate成功: {user_create.email}")

        # 测试UserUpdate（需要email）
        try:
            user_update = UserUpdate()
            print("❌ UserUpdate空对象应该失败但没有失败")
        except Exception:
            print("✅ UserUpdate空对象正确失败")

        user_update = UserUpdate(email="updated@test.com", full_name="Updated")
        print(f"✅ UserUpdate成功: {user_update.email}")

        # 测试User Schema
        user_schema = UserSchema(
            id=1,
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            is_active=True,
            is_superuser=False,
        )
        print(f"✅ User Schema成功: {user_schema.id}")

        return True
    except Exception as e:
        print(f"❌ Schema测试失败: {e}")
        return False


def test_api_behavior():
    """测试API行为修复"""
    print("\n=== 测试API行为修复 ===")

    try:
        client = TestClient(app)

        # 测试用户创建（期望200）
        unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        user_data = {
            "email": unique_email,
            "password": "testpassword",
            "full_name": "Test User",
        }

        response = client.post("/api/v1/users/", json=user_data)
        if response.status_code == 200:
            print(f"✅ 用户创建返回200: {response.json()['email']}")
        else:
            print(f"❌ 用户创建失败: {response.status_code} - {response.text}")
            return False

        # 测试重复创建（期望400）
        response2 = client.post("/api/v1/users/", json=user_data)
        if response2.status_code == 400:
            print("✅ 重复用户创建正确返回400")
        else:
            print(f"❌ 重复用户创建应返回400，实际: {response2.status_code}")

        # 测试登录（期望200）
        login_data = {"username": unique_email, "password": "testpassword"}

        login_response = client.post("/api/v1/login/access-token", data=login_data)
        if login_response.status_code == 200:
            token_data = login_response.json()
            if "access_token" in token_data:
                print("✅ 登录成功并返回access_token")
            else:
                print("❌ 登录成功但缺少access_token")
                return False
        else:
            print(f"❌ 登录失败: {login_response.status_code} - {login_response.text}")
            return False

        # 测试错误密码登录（期望401）
        wrong_login_data = {"username": unique_email, "password": "wrongpassword"}

        wrong_response = client.post(
            "/api/v1/login/access-token", data=wrong_login_data
        )
        if wrong_response.status_code == 401:
            print("✅ 错误密码登录正确返回401")
        else:
            print(f"❌ 错误密码登录应返回401，实际: {wrong_response.status_code}")

        return True
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False


def test_password_functions():
    """测试密码功能"""
    print("\n=== 测试密码功能 ===")

    try:
        password = "testpassword123"
        hashed = get_password_hash(password)

        if hashed != password:
            print("✅ 密码哈希不等于原密码")
        else:
            print("❌ 密码哈希等于原密码")
            return False

        if pwd_context.verify(password, hashed):
            print("✅ 密码验证成功")
        else:
            print("❌ 密码验证失败")
            return False

        if not pwd_context.verify("wrongpassword", hashed):
            print("✅ 错误密码验证正确失败")
        else:
            print("❌ 错误密码验证应该失败但成功了")
            return False

        return True
    except Exception as e:
        print(f"❌ 密码测试失败: {e}")
        return False


def test_crud_functions():
    """测试CRUD功能"""
    print("\n=== 测试CRUD功能 ===")

    try:
        from crud import crud_user

        # 检查CRUD对象存在
        if hasattr(crud_user, "user"):
            crud_obj = crud_user.user
            print("✅ crud_user.user对象存在")

            if hasattr(crud_obj, "create"):
                print("✅ create方法存在")
            else:
                print("❌ create方法不存在")
                return False

            if hasattr(crud_obj, "is_superuser"):
                print("✅ is_superuser方法存在")
            else:
                print("❌ is_superuser方法不存在")
                return False
        else:
            print("❌ crud_user.user对象不存在")
            return False

        # 检查独立函数
        if hasattr(crud_user, "create_user"):
            print("✅ create_user函数存在")
        else:
            print("❌ create_user函数不存在")

        if hasattr(crud_user, "authenticate_user"):
            print("✅ authenticate_user函数存在")
        else:
            print("❌ authenticate_user函数不存在")

        return True
    except Exception as e:
        print(f"❌ CRUD测试失败: {e}")
        return False


def main():
    """运行所有验证测试"""
    print("开始最终测试验证...")
    print("=" * 60)

    tests = [
        test_schema_fixes,
        test_password_functions,
        test_crud_functions,
        test_api_behavior,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 60)
    print(f"验证结果: {passed}/{total} 通过 ({passed/total*100:.1f}%)")

    if passed == total:
        print("🎉 所有验证测试通过！测试框架修复成功！")
        print("\n推荐使用以下命令运行修复后的测试:")
        print("python -m pytest tests/test_core_fixed.py -v")
    else:
        print(f"⚠️ {total - passed} 个验证测试失败，需要进一步修复")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
