import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { loginUser } from '../api'

export function Login() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)

  async function submit(ev: React.FormEvent) {
    ev.preventDefault()
    setError(null)
    try {
      const user = await loginUser({ username, password })
      navigate(`/account`, { state: { justLoggedIn: user.username } })
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : String(err)
      setError(`Logowanie nie powiodło się: ${message}`)
    }
  }

  return (
    <section>
      <h2>Logowanie</h2>
      <form onSubmit={submit} data-testid="login-form">
        <div>
          <label>
            Nazwa użytkownika{' '}
            <input
              data-testid="login-username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </label>
        </div>
        <div>
          <label>
            Hasło{' '}
            <input
              data-testid="login-password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>
        </div>
        <button type="submit" data-testid="login-submit">
          Zaloguj
        </button>
        {error && (
          <p data-testid="login-error" style={{ color: 'red' }}>
            {error}
          </p>
        )}
      </form>
    </section>
  )
}
