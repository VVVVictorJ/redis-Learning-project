#!/usr/bin/env python3
"""
检查用户状态脚本
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.user import User


def check_users():
    """检查用户状态"""
    db: Session = SessionLocal()

    try:
        print("👥 检查用户状态...")

        users = db.query(User).all()

        for user in users:
            print(f"用户: {user.username} ({user.email})")
            print(f"  - 是否激活: {user.is_active}")
            print(f"  - 是否超级用户: {user.is_superuser}")
            print()

    except Exception as e:
        print(f"❌ 检查用户失败: {str(e)}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    check_users()
