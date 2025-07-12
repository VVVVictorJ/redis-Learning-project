export interface Expense {
  id: number
  description: string
  amount: number
  category: string
  date: string // or Date, if you parse it
  owner_id: number
}

export interface ExpenseCreate {
  description: string
  amount: number
  category: string
  date: string
}

export interface ExpenseUpdate {
  description?: string
  amount?: number
  category?: string
  date?: string
} 