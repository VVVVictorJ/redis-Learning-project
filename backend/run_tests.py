#!/usr/bin/env python3
"""
测试运行脚本
"""
import sys
import os
import pytest

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_tests():
    """运行所有测试"""

    # 设置环境变量
    os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
    os.environ.setdefault("REDIS_HOST", "localhost")
    os.environ.setdefault("REDIS_PORT", "6379")
    os.environ.setdefault("SECRET_KEY", "test-secret-key")
    os.environ.setdefault("ALGORITHM", "HS256")
    os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    os.environ.setdefault("FIRST_SUPERUSER", "admin@example.com")
    os.environ.setdefault("FIRST_SUPERUSER_PASSWORD", "adminpassword")

    # 运行测试
    pytest_args = ["tests/", "-v", "--tb=short", "--strict-markers", "--strict-config"]

    return pytest.main(pytest_args)


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
