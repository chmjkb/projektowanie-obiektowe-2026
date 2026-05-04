import { useState } from 'react'
import type { Product } from '../types'

type CartItem = { product: Product; quantity: number }

export function Cart() {
  const [items] = useState<CartItem[]>([])

  const total = items.reduce((s, i) => s + i.product.price * i.quantity, 0)

  return (
    <section>
      <h2>Koszyk</h2>
      {items.length === 0 ? (
        <p>Koszyk jest pusty.</p>
      ) : (
        <ul>
          {items.map((i) => (
            <li key={i.product.id}>
              {i.product.name} × {i.quantity} = {(i.product.price * i.quantity).toFixed(2)} zł
            </li>
          ))}
        </ul>
      )}
      <p>
        <strong>Suma: {total.toFixed(2)} zł</strong>
      </p>
    </section>
  )
}
