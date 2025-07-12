from sqlalchemy import create_engine, text


def verify_admin():
    engine = create_engine(
        "postgresql+psycopg2://catuser:catDevPass@localhost:5432/catdb"
    )
    with engine.connect() as conn:
        # Check if admin user exists
        result = conn.execute(
            text(
                "SELECT id, username, email, full_name, is_active, is_superuser FROM users WHERE is_superuser = true"
            )
        )
        admin_users = list(result)

        if admin_users:
            print("管理员账号创建成功！")
            for user in admin_users:
                print(f"ID: {user[0]}")
                print(f"用户名: {user[1]}")
                print(f"邮箱: {user[2]}")
                print(f"全名: {user[3]}")
                print(f"激活状态: {user[4]}")
                print(f"超级用户: {user[5]}")
                print("-" * 30)
        else:
            print("未找到管理员账号")


if __name__ == "__main__":
    verify_admin()
