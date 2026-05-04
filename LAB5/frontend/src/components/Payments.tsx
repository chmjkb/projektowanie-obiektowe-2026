import { useState } from 'react'
import { postPayment } from '../api'

export function Payments() {
  const [customerName, setCustomerName] = useState('')
  const [productId, setProductId] = useState(1)
  const [quantity, setQuantity] = useState(1)
  const [total, setTotal] = useState(0)
  const [status, setStatus] = useState<string | null>(null)

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    try {
      const payment = await postPayment({
        customer_name: customerName,
        items: [{ product_id: productId, quantity }],
        total,
      })
      setStatus(`Zapłacono: ${payment.customer_name} — ${payment.total.toFixed(2)} zł`)
    } catch (err) {
      setStatus(`Błąd: ${(err as Error).message}`)
    }
  }

  return (
    <section>
      <h2>Płatności</h2>
      <form onSubmit={submit}>
        <label>
          Klient:{' '}
          <input value={customerName} onChange={(e) => setCustomerName(e.target.value)} required />
        </label>
        <br />
        <label>
          ID produktu:{' '}
          <input
            type="number"
            value={productId}
            onChange={(e) => setProductId(Number(e.target.value))}
          />
        </label>
        <br />
        <label>
          Ilość:{' '}
          <input
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(Number(e.target.value))}
          />
        </label>
        <br />
        <label>
          Suma:{' '}
          <input
            type="number"
            step="0.01"
            value={total}
            onChange={(e) => setTotal(Number(e.target.value))}
          />
        </label>
        <br />
        <button type="submit">Zapłać</button>
      </form>
      {status && <p>{status}</p>}
    </section>
  )
}
