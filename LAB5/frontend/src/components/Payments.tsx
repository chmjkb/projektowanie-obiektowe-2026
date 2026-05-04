import { useState } from 'react'
import { postPayment } from '../api'
import { useCart } from '../context/CartContext'

export function Payments() {
  const { items, total, clear } = useCart()
  const [customerName, setCustomerName] = useState('')
  const [status, setStatus] = useState<string | null>(null)

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    if (items.length === 0) {
      setStatus('Koszyk jest pusty.')
      return
    }
    try {
      const payment = await postPayment({
        customer_name: customerName,
        items: items.map((i) => ({ product_id: i.product.id, quantity: i.quantity })),
        total,
      })
      setStatus(`Zapłacono: ${payment.customer_name} — ${payment.total.toFixed(2)} zł`)
      clear()
    } catch (err) {
      setStatus(`Błąd: ${(err as Error).message}`)
    }
  }

  return (
    <section>
      <h2>Płatności</h2>
      <p>Do zapłaty: <strong>{total.toFixed(2)} zł</strong> ({items.length} pozycji)</p>
      <form onSubmit={submit}>
        <label>
          Klient:{' '}
          <input
            value={customerName}
            onChange={(e) => setCustomerName(e.target.value)}
            required
          />
        </label>
        <br />
        <button type="submit">Zapłać</button>
      </form>
      {status && <p>{status}</p>}
    </section>
  )
}
