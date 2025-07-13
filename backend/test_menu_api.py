#!/usr/bin/env python3
"""
菜单系统API测试脚本
"""
import requests
import json
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


def test_login() -> str:
    """测试登录并获取token"""
    print("🔐 测试登录...")

    # 首先创建一个超级用户（如果不存在）
    register_data = {
        "username": "admin",
        "email": "admin@example.com",
        "full_name": "Admin User",
        "password": "admin123",
    }

    try:
        response = requests.post(f"{BASE_URL}/api/v1/users/", json=register_data)
        if response.status_code == 200:
            print("✅ 超级用户创建成功")
        else:
            print(f"ℹ️  超级用户可能已存在: {response.status_code}")
    except Exception as e:
        print(f"⚠️  创建超级用户失败: {e}")

    # 登录获取token
    login_data = {"username": "admin@example.com", "password": "admin123"}

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/login/access-token", data=login_data
        )
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ 登录成功")
            return token
        else:
            print(f"❌ 登录失败: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
        return None


def test_menu_crud(token: str):
    """测试菜单CRUD操作"""
    print("\n📋 测试菜单CRUD操作...")

    headers = {"Authorization": f"Bearer {token}"}

    # 1. 创建菜单项
    print("1. 创建菜单项...")
    menu_data = {"title": "API测试菜单", "icon": "test", "route": "/test", "order": 1}

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/menus/", json=menu_data, headers=headers
        )
        if response.status_code == 200:
            menu_item = response.json()
            print(f"✅ 菜单项创建成功: {menu_item['title']}")
            menu_id = menu_item["id"]
        else:
            print(f"❌ 菜单项创建失败: {response.status_code}")
            print(response.text)
            return
    except Exception as e:
        print(f"❌ 菜单项创建请求失败: {e}")
        return

    # 2. 获取所有菜单项
    print("2. 获取所有菜单项...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/menus/", headers=headers)
        if response.status_code == 200:
            menus = response.json()
            print(f"✅ 获取菜单项成功，共 {len(menus)} 项")
        else:
            print(f"❌ 获取菜单项失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取菜单项请求失败: {e}")

    # 3. 获取单个菜单项
    print("3. 获取单个菜单项...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/menus/{menu_id}", headers=headers)
        if response.status_code == 200:
            menu_item = response.json()
            print(f"✅ 获取单个菜单项成功: {menu_item['title']}")
        else:
            print(f"❌ 获取单个菜单项失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取单个菜单项请求失败: {e}")

    # 4. 更新菜单项
    print("4. 更新菜单项...")
    update_data = {"title": "更新后的测试菜单", "description": "这是更新后的描述"}

    try:
        response = requests.put(
            f"{BASE_URL}/api/v1/menus/{menu_id}", json=update_data, headers=headers
        )
        if response.status_code == 200:
            updated_menu = response.json()
            print(f"✅ 菜单项更新成功: {updated_menu['title']}")
        else:
            print(f"❌ 菜单项更新失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 菜单项更新请求失败: {e}")

    return menu_id


def test_button_permissions(token: str, menu_id: int):
    """测试按钮权限操作"""
    print("\n🔘 测试按钮权限操作...")

    headers = {"Authorization": f"Bearer {token}"}

    # 1. 创建按钮权限
    print("1. 创建按钮权限...")
    import time

    button_data = {
        "button_id": f"test_button_{int(time.time())}",
        "description": "测试按钮",
        "menu_item_id": menu_id,
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/menus/buttons/", json=button_data, headers=headers
        )
        if response.status_code == 200:
            button_perm = response.json()
            print(f"✅ 按钮权限创建成功: {button_perm['description']}")
        else:
            print(f"❌ 按钮权限创建失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 按钮权限创建请求失败: {e}")

    # 2. 获取所有按钮权限
    print("2. 获取所有按钮权限...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/menus/buttons/", headers=headers)
        if response.status_code == 200:
            buttons = response.json()
            print(f"✅ 获取按钮权限成功，共 {len(buttons)} 项")
        else:
            print(f"❌ 获取按钮权限失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取按钮权限请求失败: {e}")


def test_user_menus(token: str):
    """测试用户菜单权限"""
    print("\n👤 测试用户菜单权限...")

    headers = {"Authorization": f"Bearer {token}"}

    # 获取当前用户菜单
    print("1. 获取当前用户菜单...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/menus/users/me/menus", headers=headers
        )
        if response.status_code == 200:
            user_menus = response.json()
            print(f"✅ 获取当前用户菜单成功，共 {len(user_menus)} 项")
            for menu in user_menus:
                print(f"  - {menu['title']} ({menu['route']})")
        else:
            print(f"❌ 获取当前用户菜单失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 获取当前用户菜单请求失败: {e}")


def main():
    """主测试函数"""
    print("🚀 开始测试菜单系统API...")

    # 1. 测试登录
    token = test_login()
    if not token:
        print("❌ 无法获取访问令牌，测试终止")
        sys.exit(1)

    # 2. 测试菜单CRUD
    menu_id = test_menu_crud(token)
    if not menu_id:
        print("❌ 菜单CRUD测试失败，跳过后续测试")
        return

    # 3. 测试按钮权限
    test_button_permissions(token, menu_id)

    # 4. 测试用户菜单
    test_user_menus(token)

    print("\n🎉 菜单系统API测试完成！")


if __name__ == "__main__":
    main()
