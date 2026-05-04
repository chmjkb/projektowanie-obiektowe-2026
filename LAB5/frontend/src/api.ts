import axios from 'axios'
import type { Payment, Product } from './types'

const baseURL = (import.meta.env.VITE_API_BASE as string | undefined) ?? 'http://localhost:8000'

export const api = axios.create({
  baseURL,
  headers: { 'Content-Type': 'application/json' },
})

export async function fetchProducts(): Promise<Product[]> {
  const res = await api.get<Product[]>('/products')
  return res.data
}

export async function postPayment(payment: Payment): Promise<Payment> {
  const res = await api.post<Payment>('/payments', payment)
  return res.data
}
