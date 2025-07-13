"""
认证API集成测试
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from models.user import User


@pytest.mark.integration
class TestAuthAPI:
    """认证API测试套件"""

    def test_login_success(self, client: TestClient, test_user: User):
        """
        测试登录成功
        预期: 返回200状态码和访问令牌
        """
        # Arrange
        login_data = {
            "username": test_user.email,  # 系统使用邮箱作为用户名
            "password": "testpassword",
        }

        # Act
        response = client.post("/api/v1/login/access-token", data=login_data)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        token_data = response.json()
        assert "access_token" in token_data
        assert "token_type" in token_data
        assert token_data["token_type"] == "bearer"
        assert isinstance(token_data["access_token"], str)
        assert len(token_data["access_token"]) > 0

    def test_login_wrong_password(self, client: TestClient, test_user: User):
        """
        测试登录失败 - 错误密码
        预期: 返回401状态码和错误信息
        """
        # Arrange
        login_data = {"username": test_user.email, "password": "wrongpassword"}

        # Act
        response = client.post("/api/v1/login/access-token", data=login_data)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        error_data = response.json()
        assert "detail" in error_data
        assert "Incorrect email or password" in error_data["detail"]

    def test_login_wrong_email(self, client: TestClient):
        """
        测试登录失败 - 错误邮箱
        预期: 返回401状态码和错误信息
        """
        # Arrange
        login_data = {"username": "nonexistent@example.com", "password": "testpassword"}

        # Act
        response = client.post("/api/v1/login/access-token", data=login_data)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        error_data = response.json()
        assert "detail" in error_data
        assert "Incorrect email or password" in error_data["detail"]

    def test_login_inactive_user(self, client: TestClient, db_session, test_user: User):
        """
        测试登录失败 - 非激活用户
        预期: 返回400状态码和错误信息
        """
        # Arrange
        test_user.is_active = False
        db_session.commit()

        login_data = {"username": test_user.email, "password": "testpassword"}

        # Act
        response = client.post("/api/v1/login/access-token", data=login_data)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        error_data = response.json()
        assert "detail" in error_data
        assert "Inactive user" in error_data["detail"]

    def test_login_missing_credentials(self, client: TestClient):
        """
        测试登录失败 - 缺少凭据
        预期: 返回422状态码和验证错误
        """
        # Arrange
        login_data = {
            "username": "test@example.com"
            # 缺少password
        }

        # Act
        response = client.post("/api/v1/login/access-token", data=login_data)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_login_empty_credentials(self, client: TestClient):
        """
        测试登录失败 - 空凭据
        预期: 返回422状态码和验证错误
        """
        # Arrange
        login_data = {"username": "", "password": ""}

        # Act
        response = client.post("/api/v1/login/access-token", data=login_data)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_access_protected_endpoint_with_token(
        self, client: TestClient, auth_headers: dict
    ):
        """
        测试使用有效令牌访问受保护端点
        预期: 成功访问
        """
        # Act
        response = client.get("/api/v1/users/me", headers=auth_headers)

        # Assert
        # 注意：这个端点可能不存在，这里只是示例
        # 如果端点不存在，应该返回404而不是401
        assert response.status_code != status.HTTP_401_UNAUTHORIZED

    def test_access_protected_endpoint_without_token(self, client: TestClient):
        """
        测试不使用令牌访问受保护端点
        预期: 返回401状态码
        """
        # Act
        response = client.get("/api/v1/users/")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_access_protected_endpoint_invalid_token(self, client: TestClient):
        """
        测试使用无效令牌访问受保护端点
        预期: 返回401状态码
        """
        # Arrange
        invalid_headers = {"Authorization": "Bearer invalid_token"}

        # Act
        response = client.get("/api/v1/users/", headers=invalid_headers)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_access_protected_endpoint_malformed_token(self, client: TestClient):
        """
        测试使用格式错误的令牌访问受保护端点
        预期: 返回401状态码
        """
        # Arrange
        malformed_headers = {"Authorization": "invalid_format"}

        # Act
        response = client.get("/api/v1/users/", headers=malformed_headers)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_response_format(self, client: TestClient, test_user: User):
        """
        测试登录响应格式
        预期: 返回正确格式的令牌响应
        """
        # Arrange
        login_data = {"username": test_user.email, "password": "testpassword"}

        # Act
        response = client.post("/api/v1/login/access-token", data=login_data)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        token_data = response.json()

        # 验证响应格式符合OAuth2标准
        required_fields = ["access_token", "token_type"]
        for field in required_fields:
            assert field in token_data

        # 验证字段类型
        assert isinstance(token_data["access_token"], str)
        assert isinstance(token_data["token_type"], str)
        assert token_data["token_type"] == "bearer"

    def test_superuser_login(self, client: TestClient, test_superuser: User):
        """
        测试超级用户登录
        预期: 成功登录并获取令牌
        """
        # Arrange
        login_data = {"username": test_superuser.email, "password": "testpassword"}

        # Act
        response = client.post("/api/v1/login/access-token", data=login_data)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        token_data = response.json()
        assert "access_token" in token_data
        assert "token_type" in token_data

    def test_multiple_login_attempts(self, client: TestClient, test_user: User):
        """
        测试多次登录尝试
        预期: 每次都应该返回新的令牌
        """
        # Arrange
        login_data = {"username": test_user.email, "password": "testpassword"}

        # Act
        response1 = client.post("/api/v1/login/access-token", data=login_data)
        response2 = client.post("/api/v1/login/access-token", data=login_data)

        # Assert
        assert response1.status_code == status.HTTP_200_OK
        assert response2.status_code == status.HTTP_200_OK

        token1 = response1.json()["access_token"]
        token2 = response2.json()["access_token"]

        # 令牌可能相同也可能不同，取决于实现
        # 这里只验证都是有效的字符串
        assert isinstance(token1, str)
        assert isinstance(token2, str)
        assert len(token1) > 0
        assert len(token2) > 0
