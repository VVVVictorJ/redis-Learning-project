from sqlalchemy.orm import Session
from models.expense import Expense
from schemas.expense import ExpenseCreate, ExpenseUpdate

def create_expense(db: Session, expense: ExpenseCreate, owner_id: int):
    db_expense = Expense(**expense.dict(), owner_id=owner_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expenses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Expense).offset(skip).limit(limit).all()

def get_expense(db: Session, expense_id: int):
    return db.query(Expense).filter(Expense.id == expense_id).first()

def get_expenses_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(Expense).filter(Expense.owner_id == owner_id).offset(skip).limit(limit).all()

def update_expense(db: Session, db_expense: Expense, expense_in: ExpenseUpdate):
    update_data = expense_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_expense, key, value)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: int):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if db_expense:
        db.delete(db_expense)
        db.commit()
    return db_expense 