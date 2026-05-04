import { Payments } from './components/Payments'
import { Products } from './components/Products'
import './App.css'

function App() {
  return (
    <main style={{ padding: '2rem', maxWidth: 720, margin: '0 auto' }}>
      <h1>Sklep</h1>
      <Products />
      <Payments />
    </main>
  )
}

export default App
