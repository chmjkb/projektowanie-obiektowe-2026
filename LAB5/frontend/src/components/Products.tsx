import { useEffect, useState } from 'react'
import { fetchProducts } from '../api'
import { useCart } from '../context/CartContext'
import type { Product } from '../types'

export function Products() {
  const [products, setProducts] = useState<Product[]>([])
  const [error, setError] = useState<string | null>(null)
  const { add } = useCart()

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
          <li key={p.id} style={{ marginBottom: '0.5rem' }}>
            {p.name} — {p.price.toFixed(2)} zł{' '}
            <button type="button" onClick={() => add(p)}>
              Dodaj do koszyka
            </button>
          </li>
        ))}
      </ul>
    </section>
  )
}
