import { useEffect, useState } from 'react'
import { fetchProducts } from '../api'
import type { Product } from '../types'

export function Products() {
  const [products, setProducts] = useState<Product[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchProducts()
      .then(setProducts)
      .catch((e: Error) => setError(e.message))
  }, [])

  if (error) return <p>Błąd: {error}</p>

  return (
    <section>
      <h2>Produkty</h2>
      <ul>
        {products.map((p) => (
          <li key={p.id}>
            {p.name} — {p.price.toFixed(2)} zł
          </li>
        ))}
      </ul>
    </section>
  )
}
