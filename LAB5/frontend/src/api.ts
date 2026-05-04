import type { Payment, Product } from './types'

const API_BASE = (import.meta.env.VITE_API_BASE as string | undefined) ?? 'http://localhost:8000'

export async function fetchProducts(): Promise<Product[]> {
  const res = await fetch(`${API_BASE}/products`)
  if (!res.ok) throw new Error(`GET /products failed: ${res.status}`)
  return res.json()
}

export async function postPayment(payment: Payment): Promise<Payment> {
  const res = await fetch(`${API_BASE}/payments`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payment),
  })
  if (!res.ok) throw new Error(`POST /payments failed: ${res.status}`)
  return res.json()
}
