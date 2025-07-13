"""
用户API集成测试
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.user import User


@pytest.mark.integration
class TestUserAPI:
    """用户API测试套件"""

    def test_create_user(self, client: TestClient):
        """
        测试创建用户API
        预期: 返回201状态码和用户信息
        """
        # Arrange
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "full_name": "New User",
            "password": "testpassword",
        }

        # Act
        response = client.post("/api/v1/users/", json=user_data)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["username"] == user_data["username"]
        assert response_data["email"] == user_data["email"]
        assert response_data["full_name"] == user_data["full_name"]
        assert "password" not in response_data
        assert "hashed_password" not in response_data
        assert response_data["is_active"] is True
        assert response_data["is_superuser"] is False

    def test_create_user_duplicate_email(self, client: TestClient, test_user: User):
        """
        测试创建重复邮箱用户
        预期: 返回400状态码和错误信息
        """
        # Arrange
        user_data = {
            "username": "newuser",
            "email": test_user.email,  # 使用已存在的邮箱
            "password": "testpassword",
        }

        # Act
        response = client.post("/api/v1/users/", json=user_data)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"]

    def test_create_user_invalid_email(self, client: TestClient):
        """
        测试创建用户时使用无效邮箱
        预期: 返回422状态码和验证错误
        """
        # Arrange
        user_data = {
            "username": "newuser",
            "email": "invalid-email",
            "password": "testpassword",
        }

        # Act
        response = client.post("/api/v1/users/", json=user_data)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        error_detail = response.json()["detail"][0]
        assert error_detail["loc"] == ["body", "email"]

    def test_create_user_missing_fields(self, client: TestClient):
        """
        测试创建用户时缺少必需字段
        预期: 返回422状态码和验证错误
        """
        # Arrange
        user_data = {
            "email": "test@example.com"
            # 缺少username和password
        }

        # Act
        response = client.post("/api/v1/users/", json=user_data)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        error_details = response.json()["detail"]
        missing_fields = [error["loc"][-1] for error in error_details]
        assert "username" in missing_fields
        assert "password" in missing_fields

    def test_get_users_unauthorized(self, client: TestClient):
        """
        测试未授权获取用户列表
        预期: 返回401状态码
        """
        # Act
        response = client.get("/api/v1/users/")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_users_normal_user(self, client: TestClient, auth_headers: dict):
        """
        测试普通用户获取用户列表
        预期: 返回403状态码（权限不足）
        """
        # Act
        response = client.get("/api/v1/users/", headers=auth_headers)

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_users_superuser(
        self, client: TestClient, superuser_auth_headers: dict
    ):
        """
        测试超级用户获取用户列表
        预期: 返回200状态码和用户列表
        """
        # Act
        response = client.get("/api/v1/users/", headers=superuser_auth_headers)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        users = response.json()
        assert isinstance(users, list)
        assert len(users) >= 1  # 至少有测试超级用户

    def test_get_user_by_id_superuser(
        self, client: TestClient, superuser_auth_headers: dict, test_user: User
    ):
        """
        测试超级用户通过ID获取用户
        预期: 返回200状态码和用户信息
        """
        # Act
        response = client.get(
            f"/api/v1/users/{test_user.id}", headers=superuser_auth_headers
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        user_data = response.json()
        assert user_data["id"] == test_user.id
        assert user_data["email"] == test_user.email
        assert "password" not in user_data
        assert "hashed_password" not in user_data

    def test_get_user_by_id_not_found(
        self, client: TestClient, superuser_auth_headers: dict
    ):
        """
        测试获取不存在的用户
        预期: 返回404状态码
        """
        # Act
        response = client.get("/api/v1/users/999", headers=superuser_auth_headers)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_user_superuser(
        self, client: TestClient, superuser_auth_headers: dict, test_user: User
    ):
        """
        测试超级用户更新用户信息
        预期: 返回200状态码和更新后的用户信息
        """
        # Arrange
        update_data = {"full_name": "Updated Name", "is_active": False}

        # Act
        response = client.put(
            f"/api/v1/users/{test_user.id}",
            json=update_data,
            headers=superuser_auth_headers,
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        user_data = response.json()
        assert user_data["full_name"] == "Updated Name"
        assert user_data["is_active"] is False

    def test_update_user_unauthorized(self, client: TestClient, test_user: User):
        """
        测试未授权更新用户
        预期: 返回401状态码
        """
        # Arrange
        update_data = {"full_name": "Updated Name"}

        # Act
        response = client.put(f"/api/v1/users/{test_user.id}", json=update_data)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_user_normal_user(
        self, client: TestClient, auth_headers: dict, test_user: User
    ):
        """
        测试普通用户更新用户信息
        预期: 返回403状态码（权限不足）
        """
        # Arrange
        update_data = {"full_name": "Updated Name"}

        # Act
        response = client.put(
            f"/api/v1/users/{test_user.id}", json=update_data, headers=auth_headers
        )

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_user_superuser(
        self, client: TestClient, superuser_auth_headers: dict, test_user: User
    ):
        """
        测试超级用户删除用户
        预期: 返回200状态码
        """
        # Act
        response = client.delete(
            f"/api/v1/users/{test_user.id}", headers=superuser_auth_headers
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK

        # 验证用户已被删除
        get_response = client.get(
            f"/api/v1/users/{test_user.id}", headers=superuser_auth_headers
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user_unauthorized(self, client: TestClient, test_user: User):
        """
        测试未授权删除用户
        预期: 返回401状态码
        """
        # Act
        response = client.delete(f"/api/v1/users/{test_user.id}")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_response_schema(self, client: TestClient):
        """
        测试用户响应Schema
        预期: 返回的用户数据符合Schema定义
        """
        # Arrange
        user_data = {
            "username": "schemauser",
            "email": "schema@example.com",
            "full_name": "Schema User",
            "password": "testpassword",
        }

        # Act
        response = client.post("/api/v1/users/", json=user_data)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        user_response = response.json()

        # 验证必需字段存在
        required_fields = ["id", "username", "email", "is_active", "is_superuser"]
        for field in required_fields:
            assert field in user_response

        # 验证敏感字段不存在
        sensitive_fields = ["password", "hashed_password"]
        for field in sensitive_fields:
            assert field not in user_response

        # 验证字段类型
        assert isinstance(user_response["id"], int)
        assert isinstance(user_response["username"], str)
        assert isinstance(user_response["email"], str)
        assert isinstance(user_response["is_active"], bool)
        assert isinstance(user_response["is_superuser"], bool)
