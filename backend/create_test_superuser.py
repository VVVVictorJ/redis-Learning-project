#!/usr/bin/env python3
"""
创建测试超级用户脚本
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from db.session import SessionLocal
from crud import crud_user
from schemas.user import UserCreate


def create_test_superuser():
    """创建测试超级用户"""
    db: Session = SessionLocal()

    try:
        print("🔐 创建测试超级用户...")

        # 删除现有的admin用户
        existing_user = crud_user.get_user_by_email(db, email="admin@example.com")
        if existing_user:
            db.delete(existing_user)
            db.commit()
            print("🗑️ 删除现有admin用户")

        # 创建新的超级用户
        user_create = UserCreate(
            username="admin",
            email="admin@example.com",
            full_name="Admin User",
            password="admin123",
        )

        superuser = crud_user.create_user(db, obj_in=user_create, is_superuser=True)
        print(f"✅ 测试超级用户创建成功: {superuser.username}")
        print(f"   邮箱: {superuser.email}")
        print(f"   是否超级用户: {superuser.is_superuser}")

    except Exception as e:
        print(f"❌ 创建测试超级用户失败: {str(e)}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    create_test_superuser()
