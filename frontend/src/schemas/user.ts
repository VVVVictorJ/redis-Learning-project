export interface User {
  id: number
  email: string
  full_name: string | null
  is_active: boolean
  is_superuser: boolean
}

export interface UserCreate {
  email: string
  password: string
  full_name?: string
} 