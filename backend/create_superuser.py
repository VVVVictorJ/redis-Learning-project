#!/usr/bin/env python3
"""
创建超级用户脚本
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from db.session import SessionLocal
from crud import crud_user
from schemas.user import UserCreate


def create_superuser():
    """创建超级用户"""
    db: Session = SessionLocal()

    try:
        print("🔐 创建超级用户...")

        # 检查是否已存在
        existing_user = crud_user.get_user_by_email(db, email="admin@example.com")
        if existing_user:
            print("✅ 超级用户已存在")
            return

        # 创建超级用户
        user_create = UserCreate(
            username="admin",
            email="admin@example.com",
            full_name="Admin User",
            password="admin123",
        )

        superuser = crud_user.create_user(db, obj_in=user_create, is_superuser=True)
        print(f"✅ 超级用户创建成功: {superuser.username}")

    except Exception as e:
        print(f"❌ 创建超级用户失败: {str(e)}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    create_superuser()
