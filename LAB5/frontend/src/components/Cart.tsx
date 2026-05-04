import { useCart } from '../context/CartContext'

export function Cart() {
  const { items, remove, clear, total } = useCart()

  return (
    <section>
      <h2>Koszyk</h2>
      {items.length === 0 ? (
        <p>Koszyk jest pusty.</p>
      ) : (
        <>
          <ul>
            {items.map((i) => (
              <li key={i.product.id}>
                {i.product.name} × {i.quantity} ={' '}
                {(i.product.price * i.quantity).toFixed(2)} zł{' '}
                <button type="button" onClick={() => remove(i.product.id)}>
                  Usuń
                </button>
              </li>
            ))}
          </ul>
          <button type="button" onClick={clear}>
            Wyczyść koszyk
          </button>
        </>
      )}
      <p>
        <strong>Suma: {total.toFixed(2)} zł</strong>
      </p>
    </section>
  )
}
