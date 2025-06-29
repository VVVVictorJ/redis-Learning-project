from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api import deps
from crud import crud_expense
from models.user import User
from schemas.expense import Expense, ExpenseCreate, ExpenseUpdate

router = APIRouter()

@router.get("/", response_model=List[Expense])
def read_expenses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve expenses.
    """
    expenses = crud_expense.get_expenses(db, skip=skip, limit=limit)
    return expenses

@router.get("/me", response_model=List[Expense])
def read_own_expenses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve own expenses.
    """
    expenses = crud_expense.get_expenses_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return expenses

@router.post("/", response_model=Expense)
def create_expense(
    *,
    db: Session = Depends(deps.get_db),
    expense_in: ExpenseCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new expense.
    """
    expense = crud_expense.create_expense(
        db, expense=expense_in, owner_id=current_user.id
    )
    return expense

@router.put("/{expense_id}", response_model=Expense)
def update_expense(
    *,
    db: Session = Depends(deps.get_db),
    expense_id: int,
    expense_in: ExpenseUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an expense.
    """
    expense = crud_expense.get_expense(db, expense_id=expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    if expense.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    expense = crud_expense.update_expense(db, db_expense=expense, expense_in=expense_in)
    return expense

@router.delete("/{expense_id}", response_model=Expense)
def delete_expense(
    *,
    db: Session = Depends(deps.get_db),
    expense_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an expense.
    """
    expense = crud_expense.get_expense(db, expense_id=expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    if expense.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    expense = crud_expense.delete_expense(db, expense_id=expense_id)
    return expense 