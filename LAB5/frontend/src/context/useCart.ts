import { createContext, useContext } from 'react'
import type { Product } from '../types'

export type CartItem = { readonly product: Product; readonly quantity: number }

export type CartContextValue = {
  readonly items: readonly CartItem[]
  readonly add: (product: Product) => void
  readonly remove: (productId: number) => void
  readonly clear: () => void
  readonly total: number
}

export const CartContext = createContext<CartContextValue | null>(null)

export function useCart(): CartContextValue {
  const ctx = useContext(CartContext)
  if (!ctx) throw new Error('useCart must be used inside CartProvider')
  return ctx
}
