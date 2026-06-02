export type Product = {
  id: number
  name: string
  price: number
}

export type PaymentItem = {
  product_id: number
  quantity: number
}

export type Payment = {
  customer_name: string
  items: PaymentItem[]
  total: number
}

export type RegisterRequest = {
  username: string
  email: string
  password: string
}

export type User = {
  id: number
  username: string
  email: string
}
