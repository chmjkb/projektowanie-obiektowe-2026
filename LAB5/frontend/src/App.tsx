import { Link, Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import { Account } from './components/Account'
import { Cart } from './components/Cart'
import { Login } from './components/Login'
import { Payments } from './components/Payments'
import { Products } from './components/Products'
import { Register } from './components/Register'
import { CartProvider } from './context/CartContext'
import './App.css'

function App() {
  return (
    <CartProvider>
      <Router>
        <main style={{ padding: '2rem', maxWidth: 720, margin: '0 auto' }}>
          <h1>Sklep</h1>
          <nav style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem' }}>
            <Link to="/">Produkty</Link>
            <Link to="/cart">Koszyk</Link>
            <Link to="/payments">Płatności</Link>
            <Link to="/register">Rejestracja</Link>
            <Link to="/login">Logowanie</Link>
            <Link to="/account">Konto</Link>
          </nav>
          <Routes>
            <Route path="/" element={<Products />} />
            <Route path="/cart" element={<Cart />} />
            <Route path="/payments" element={<Payments />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/account" element={<Account />} />
          </Routes>
        </main>
      </Router>
    </CartProvider>
  )
}

export default App
