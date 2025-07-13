#!/usr/bin/env python3

from db.session import SessionLocal
from models.user import User
from models.expense import Expense
import datetime


def create_test_expenses():
    db = SessionLocal()
    try:
        # 获取第一个用户
        user = db.query(User).first()
        if user:
            print(f"找到用户: {user.email}")

            # 创建一些测试expense数据
            test_expenses = [
                {"description": "午餐", "amount": 35.50},
                {"description": "地铁票", "amount": 6.00},
                {"description": "咖啡", "amount": 15.80},
                {"description": "超市购物", "amount": 128.90},
                {"description": "电影票", "amount": 45.00},
            ]

            for expense_data in test_expenses:
                expense = Expense(
                    description=expense_data["description"],
                    amount=expense_data["amount"],
                    owner_id=user.id,
                    date=datetime.datetime.utcnow(),
                )
                db.add(expense)

            db.commit()
            print("测试expense数据创建成功!")

            # 查询验证
            expenses = db.query(Expense).filter(Expense.owner_id == user.id).all()
            print(f"用户总共有 {len(expenses)} 笔支出")
            for exp in expenses:
                print(f"- {exp.description}: ¥{exp.amount}")
        else:
            print("没有找到用户")
    finally:
        db.close()


if __name__ == "__main__":
    create_test_expenses()
