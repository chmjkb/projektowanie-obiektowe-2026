import axios from 'axios'
import type { Payment, Product, RegisterRequest, User } from './types'

const baseURL = (import.meta.env.VITE_API_BASE as string | undefined) ?? 'http://localhost:8000'

export const api = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
})

export async function fetchProducts(): Promise<Product[]> {
  const res = await api.get<Product[]>('/products')
  return res.data
}

export async function postPayment(payment: Payment): Promise<Payment> {
  const res = await api.post<Payment>('/payments', payment)
  return res.data
}

export async function registerUser(payload: RegisterRequest): Promise<User> {
  const res = await api.post<User>('/register', payload)
  return res.data
}
