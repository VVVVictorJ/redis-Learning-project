from pydantic import BaseModel
import datetime

# Shared properties
class ExpenseBase(BaseModel):
    description: str | None = None
    amount: float

# Properties to receive on expense creation
class ExpenseCreate(ExpenseBase):
    pass

# Properties to receive on expense update
class ExpenseUpdate(ExpenseBase):
    pass

# Properties shared by models stored in DB
class ExpenseInDBBase(ExpenseBase):
    id: int
    date: datetime.datetime
    owner_id: int

    class Config:
        from_attributes = True

# Properties to return to client
class Expense(ExpenseInDBBase):
    pass

# Properties stored in DB
class ExpenseInDB(ExpenseInDBBase):
    pass 