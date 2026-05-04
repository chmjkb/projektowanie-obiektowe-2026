import { createContext, useCallback, useContext, useMemo, useState } from 'react'
import type { ReactNode } from 'react'
import type { Product } from '../types'

export type CartItem = { product: Product; quantity: number }

type CartContextValue = {
  items: CartItem[]
  add: (product: Product) => void
  remove: (productId: number) => void
  clear: () => void
  total: number
}

const CartContext = createContext<CartContextValue | null>(null)

export function CartProvider({ children }: { children: ReactNode }) {
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

export function useCart(): CartContextValue {
  const ctx = useContext(CartContext)
  if (!ctx) throw new Error('useCart must be used inside CartProvider')
  return ctx
}
