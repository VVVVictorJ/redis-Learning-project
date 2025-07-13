#!/usr/bin/env python3
"""
API调试脚本 - 分析测试失败的原因
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app
from fastapi.testclient import TestClient


def debug_user_creation():
    """调试用户创建API"""
    print("=== 调试用户创建API ===")
    client = TestClient(app)

    # 测试1: 基本用户创建
    user_data = {"email": "test@test.com", "password": "test123"}

    print(f"请求数据: {user_data}")
    response = client.post("/api/v1/users/", json=user_data)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    print()

    # 测试2: 带完整信息的用户创建
    user_data_full = {
        "email": "test2@test.com",
        "password": "test123",
        "full_name": "Test User",
    }

    print(f"请求数据(完整): {user_data_full}")
    response2 = client.post("/api/v1/users/", json=user_data_full)
    print(f"状态码: {response2.status_code}")
    print(f"响应内容: {response2.text}")
    print()


def debug_login_api():
    """调试登录API"""
    print("=== 调试登录API ===")
    client = TestClient(app)

    # 先创建用户
    user_data = {
        "email": "login@test.com",
        "password": "test123",
        "full_name": "Login User",
    }

    create_response = client.post("/api/v1/users/", json=user_data)
    print(f"用户创建状态: {create_response.status_code}")

    if create_response.status_code in [200, 201]:
        # 测试登录
        login_data = {"username": "login@test.com", "password": "test123"}

        print(f"登录数据: {login_data}")
        login_response = client.post("/api/v1/login/access-token", data=login_data)
        print(f"登录状态码: {login_response.status_code}")
        print(f"登录响应: {login_response.text}")
    else:
        print("用户创建失败，无法测试登录")
    print()


def debug_schema_validation():
    """调试Schema验证"""
    print("=== 调试Schema验证 ===")

    try:
        from schemas.user import UserCreate, UserUpdate, User

        # 测试UserCreate
        print("测试UserCreate Schema:")
        user_create = UserCreate(email="test@test.com", password="test123")
        print(f"UserCreate成功: {user_create}")
        print(f"字段: {user_create.model_dump()}")

        # 测试UserUpdate
        print("\n测试UserUpdate Schema:")
        try:
            user_update = UserUpdate()
            print(f"空UserUpdate: {user_update}")
        except Exception as e:
            print(f"空UserUpdate失败: {e}")

        try:
            user_update = UserUpdate(email="updated@test.com")
            print(f"UserUpdate成功: {user_update}")
            print(f"字段: {user_update.model_dump()}")
        except Exception as e:
            print(f"UserUpdate失败: {e}")

    except Exception as e:
        print(f"Schema导入或测试失败: {e}")
    print()


def debug_crud_operations():
    """调试CRUD操作"""
    print("=== 调试CRUD操作 ===")

    try:
        from crud import crud_user
        from schemas.user import UserCreate

        # 检查CRUD函数
        print("可用的CRUD函数:")
        print(f"crud_user.user: {hasattr(crud_user, 'user')}")
        if hasattr(crud_user, "user"):
            crud_obj = crud_user.user
            print(f"create方法: {hasattr(crud_obj, 'create')}")
            print(f"is_superuser方法: {hasattr(crud_obj, 'is_superuser')}")

        print(f"create_user函数: {hasattr(crud_user, 'create_user')}")
        print(f"authenticate_user函数: {hasattr(crud_user, 'authenticate_user')}")

    except Exception as e:
        print(f"CRUD测试失败: {e}")
    print()


def main():
    """运行所有调试测试"""
    print("开始API调试...")
    print("=" * 50)

    debug_schema_validation()
    debug_user_creation()
    debug_login_api()
    debug_crud_operations()

    print("=" * 50)
    print("调试完成")


if __name__ == "__main__":
    main()
