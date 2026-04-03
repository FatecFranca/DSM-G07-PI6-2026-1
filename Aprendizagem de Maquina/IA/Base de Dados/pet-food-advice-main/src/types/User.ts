import type { Pet } from './Pet'

export interface User {
  id: string
  first_name: string
  last_name: string
  full_name: string
  email: string
  pets: Pet[]
}
