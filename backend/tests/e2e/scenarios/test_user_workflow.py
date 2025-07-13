"""
用户工作流端到端测试
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.e2e
class TestUserWorkflow:
    """用户工作流测试套件"""

    def test_complete_user_lifecycle(self, client: TestClient):
        """
        测试完整的用户生命周期
        包括: 创建用户 -> 登录 -> 访问资源 -> 更新信息 -> 删除用户
        """
        # Step 1: 创建用户
        user_data = {
            "username": "lifecycleuser",
            "email": "lifecycle@example.com",
            "full_name": "Lifecycle User",
            "password": "testpassword",
        }

        create_response = client.post("/api/v1/users/", json=user_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        user = create_response.json()
        user_id = user["id"]

        # Step 2: 用户登录
        login_data = {"username": user_data["email"], "password": user_data["password"]}

        login_response = client.post("/api/v1/login/access-token", data=login_data)
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Step 3: 创建超级用户以便进行管理操作
        superuser_data = {
            "username": "admin",
            "email": "admin@example.com",
            "password": "adminpassword",
            "is_superuser": True,
        }

        admin_create_response = client.post("/api/v1/users/", json=superuser_data)
        assert admin_create_response.status_code == status.HTTP_201_CREATED

        # 超级用户登录
        admin_login_data = {
            "username": superuser_data["email"],
            "password": superuser_data["password"],
        }

        admin_login_response = client.post(
            "/api/v1/login/access-token", data=admin_login_data
        )
        assert admin_login_response.status_code == status.HTTP_200_OK
        admin_token = admin_login_response.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        # Step 4: 超级用户获取用户信息
        get_response = client.get(f"/api/v1/users/{user_id}", headers=admin_headers)
        assert get_response.status_code == status.HTTP_200_OK
        retrieved_user = get_response.json()
        assert retrieved_user["email"] == user_data["email"]

        # Step 5: 超级用户更新用户信息
        update_data = {"full_name": "Updated Lifecycle User", "is_active": True}

        update_response = client.put(
            f"/api/v1/users/{user_id}", json=update_data, headers=admin_headers
        )
        assert update_response.status_code == status.HTTP_200_OK
        updated_user = update_response.json()
        assert updated_user["full_name"] == update_data["full_name"]

        # Step 6: 验证更新后的信息
        verify_response = client.get(f"/api/v1/users/{user_id}", headers=admin_headers)
        assert verify_response.status_code == status.HTTP_200_OK
        verified_user = verify_response.json()
        assert verified_user["full_name"] == update_data["full_name"]

        # Step 7: 超级用户删除用户
        delete_response = client.delete(
            f"/api/v1/users/{user_id}", headers=admin_headers
        )
        assert delete_response.status_code == status.HTTP_200_OK

        # Step 8: 验证用户已被删除
        check_response = client.get(f"/api/v1/users/{user_id}", headers=admin_headers)
        assert check_response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_authentication_workflow(self, client: TestClient):
        """
        测试用户认证工作流
        包括: 创建用户 -> 登录成功 -> 访问受保护资源 -> 令牌失效测试
        """
        # Step 1: 创建用户
        user_data = {
            "username": "authuser",
            "email": "auth@example.com",
            "full_name": "Auth User",
            "password": "authpassword",
        }

        create_response = client.post("/api/v1/users/", json=user_data)
        assert create_response.status_code == status.HTTP_201_CREATED

        # Step 2: 用户登录
        login_data = {"username": user_data["email"], "password": user_data["password"]}

        login_response = client.post("/api/v1/login/access-token", data=login_data)
        assert login_response.status_code == status.HTTP_200_OK
        token_data = login_response.json()
        assert "access_token" in token_data
        assert "token_type" in token_data

        # Step 3: 使用令牌访问受保护资源
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}

        # 尝试访问需要认证的端点（即使权限不足也应该通过认证）
        protected_response = client.get("/api/v1/users/", headers=headers)
        # 普通用户访问用户列表应该返回403而不是401
        assert protected_response.status_code == status.HTTP_403_FORBIDDEN

        # Step 4: 测试无效令牌
        invalid_headers = {"Authorization": "Bearer invalid_token"}
        invalid_response = client.get("/api/v1/users/", headers=invalid_headers)
        assert invalid_response.status_code == status.HTTP_401_UNAUTHORIZED

        # Step 5: 测试不同密码登录失败
        wrong_login_data = {"username": user_data["email"], "password": "wrongpassword"}

        wrong_login_response = client.post(
            "/api/v1/login/access-token", data=wrong_login_data
        )
        assert wrong_login_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_menu_system_workflow(self, client: TestClient):
        """
        测试菜单系统工作流
        包括: 创建超级用户 -> 创建菜单 -> 设置权限 -> 用户访问菜单
        """
        # Step 1: 创建超级用户
        superuser_data = {
            "username": "menuadmin",
            "email": "menuadmin@example.com",
            "password": "adminpassword",
            "is_superuser": True,
        }

        admin_create_response = client.post("/api/v1/users/", json=superuser_data)
        assert admin_create_response.status_code == status.HTTP_201_CREATED

        # 超级用户登录
        admin_login_data = {
            "username": superuser_data["email"],
            "password": superuser_data["password"],
        }

        admin_login_response = client.post(
            "/api/v1/login/access-token", data=admin_login_data
        )
        assert admin_login_response.status_code == status.HTTP_200_OK
        admin_token = admin_login_response.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        # Step 2: 创建普通用户
        user_data = {
            "username": "menuuser",
            "email": "menuuser@example.com",
            "password": "userpassword",
        }

        user_create_response = client.post("/api/v1/users/", json=user_data)
        assert user_create_response.status_code == status.HTTP_201_CREATED
        user = user_create_response.json()
        user_id = user["id"]

        # Step 3: 创建菜单项
        menu_data = {
            "title": "测试菜单",
            "icon": "test-icon",
            "route": "/test",
            "order": 1,
        }

        menu_response = client.post(
            "/api/v1/menus/", json=menu_data, headers=admin_headers
        )
        assert menu_response.status_code == status.HTTP_201_CREATED
        menu = menu_response.json()
        menu_id = menu["id"]

        # Step 4: 创建按钮权限
        button_data = {
            "button_id": "test_button",
            "description": "测试按钮",
            "menu_item_id": menu_id,
        }

        button_response = client.post(
            "/api/v1/menus/buttons/", json=button_data, headers=admin_headers
        )
        assert button_response.status_code == status.HTTP_201_CREATED

        # Step 5: 设置用户菜单权限
        menu_permission_data = {"menu_item_ids": [menu_id]}

        menu_perm_response = client.post(
            f"/api/v1/menus/users/{user_id}/menus",
            json=menu_permission_data,
            headers=admin_headers,
        )
        assert menu_perm_response.status_code == status.HTTP_200_OK

        # Step 6: 设置用户按钮权限
        button_permission_data = {
            "permissions": [{"button_id": "test_button", "has_permission": True}]
        }

        button_perm_response = client.post(
            f"/api/v1/menus/users/{user_id}/buttons",
            json=button_permission_data,
            headers=admin_headers,
        )
        assert button_perm_response.status_code == status.HTTP_200_OK

        # Step 7: 用户登录并获取菜单
        user_login_data = {
            "username": user_data["email"],
            "password": user_data["password"],
        }

        user_login_response = client.post(
            "/api/v1/login/access-token", data=user_login_data
        )
        assert user_login_response.status_code == status.HTTP_200_OK
        user_token = user_login_response.json()["access_token"]
        user_headers = {"Authorization": f"Bearer {user_token}"}

        # Step 8: 获取用户可访问的菜单
        user_menu_response = client.get(
            "/api/v1/menus/users/me/menus", headers=user_headers
        )
        assert user_menu_response.status_code == status.HTTP_200_OK
        user_menus = user_menu_response.json()
        assert len(user_menus) >= 1

        # 验证菜单包含正确的按钮权限
        test_menu = next((m for m in user_menus if m["title"] == "测试菜单"), None)
        assert test_menu is not None
        assert len(test_menu["buttons"]) >= 1
        test_button = next(
            (b for b in test_menu["buttons"] if b["button_id"] == "test_button"), None
        )
        assert test_button is not None
        assert test_button["has_permission"] is True

    def test_error_handling_workflow(self, client: TestClient):
        """
        测试错误处理工作流
        包括: 各种错误场景的正确处理
        """
        # Step 1: 测试创建重复用户
        user_data = {
            "username": "erroruser",
            "email": "error@example.com",
            "password": "testpassword",
        }

        # 第一次创建成功
        first_response = client.post("/api/v1/users/", json=user_data)
        assert first_response.status_code == status.HTTP_201_CREATED

        # 第二次创建应该失败
        second_response = client.post("/api/v1/users/", json=user_data)
        assert second_response.status_code == status.HTTP_400_BAD_REQUEST

        # Step 2: 测试无效数据格式
        invalid_user_data = {
            "username": "",  # 空用户名
            "email": "invalid-email",  # 无效邮箱
            "password": "",  # 空密码
        }

        invalid_response = client.post("/api/v1/users/", json=invalid_user_data)
        assert invalid_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Step 3: 测试访问不存在的资源
        not_found_response = client.get("/api/v1/users/99999")
        assert (
            not_found_response.status_code == status.HTTP_401_UNAUTHORIZED
        )  # 先检查认证

        # Step 4: 测试未授权访问
        unauthorized_response = client.get("/api/v1/users/")
        assert unauthorized_response.status_code == status.HTTP_401_UNAUTHORIZED

        # Step 5: 测试权限不足
        # 先登录普通用户
        login_data = {"username": user_data["email"], "password": user_data["password"]}

        login_response = client.post("/api/v1/login/access-token", data=login_data)
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 普通用户尝试访问需要超级用户权限的资源
        forbidden_response = client.get("/api/v1/users/", headers=headers)
        assert forbidden_response.status_code == status.HTTP_403_FORBIDDEN
