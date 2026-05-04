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
