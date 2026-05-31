import { useCallback, useMemo, useState } from 'react'
import type { ReactNode } from 'react'
import type { Product } from '../types'
import { CartContext, type CartItem } from './useCart'

export function CartProvider({ children }: Readonly<{ children: ReactNode }>) {
  const [items, setItems] = useState<CartItem[]>([])

  const add = useCallback((product: Product) => {
    setItems((prev) => {
      const existing = prev.find((i) => i.product.id === product.id)
      if (existing) {
        return prev.map((i) =>
          i.product.id === product.id ? { ...i, quantity: i.quantity + 1 } : i,
        )
      }
      return [...prev, { product, quantity: 1 }]
    })
  }, [])

  const remove = useCallback((productId: number) => {
    setItems((prev) => prev.filter((i) => i.product.id !== productId))
  }, [])

  const clear = useCallback(() => setItems([]), [])

  const total = useMemo(
    () => items.reduce((s, i) => s + i.product.price * i.quantity, 0),
    [items],
  )

  const value = useMemo(
    () => ({ items, add, remove, clear, total }),
    [items, add, remove, clear, total],
  )

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>
}
