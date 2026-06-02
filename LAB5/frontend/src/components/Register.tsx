import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { registerUser } from '../api'

const EMAIL_REGEX = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/

type Errors = {
  username?: string
  email?: string
  password?: string
  form?: string
}

export function Register() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [errors, setErrors] = useState<Errors>({})
  const [success, setSuccess] = useState<string | null>(null)

  function validate(): Errors {
    const e: Errors = {}
    if (!username.trim()) e.username = 'Nazwa użytkownika jest wymagana'
    else if (username.trim().length < 3) e.username = 'Nazwa musi mieć co najmniej 3 znaki'

    if (!email.trim()) e.email = 'Email jest wymagany'
    else if (!EMAIL_REGEX.test(email.trim())) e.email = 'Niepoprawny format adresu e-mail'

    if (!password) e.password = 'Hasło jest wymagane'
    else if (password.length < 6) e.password = 'Hasło musi mieć co najmniej 6 znaków'

    return e
  }

  async function submit(ev: React.FormEvent) {
    ev.preventDefault()
    setSuccess(null)
    const validation = validate()
    setErrors(validation)
    if (Object.keys(validation).length > 0) return

    try {
      const user = await registerUser({ username: username.trim(), email: email.trim(), password })
      setSuccess(`Konto utworzone dla ${user.username}`)
      setTimeout(() => navigate('/login'), 800)
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : String(err)
      setErrors({ form: `Błąd rejestracji: ${message}` })
    }
  }

  return (
    <section>
      <h2>Rejestracja</h2>
      <form onSubmit={submit} noValidate data-testid="register-form">
        <div>
          <label>
            Nazwa użytkownika{' '}
            <input
              data-testid="username-input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </label>
          {errors.username && (
            <p data-testid="username-error" style={{ color: 'red' }}>
              {errors.username}
            </p>
          )}
        </div>
        <div>
          <label>
            Email{' '}
            <input
              data-testid="email-input"
              type="text"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </label>
          {errors.email && (
            <p data-testid="email-error" style={{ color: 'red' }}>
              {errors.email}
            </p>
          )}
        </div>
        <div>
          <label>
            Hasło{' '}
            <input
              data-testid="password-input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>
          {errors.password && (
            <p data-testid="password-error" style={{ color: 'red' }}>
              {errors.password}
            </p>
          )}
        </div>
        <button type="submit" data-testid="submit-button">
          Zarejestruj
        </button>
        {errors.form && (
          <p data-testid="form-error" style={{ color: 'red' }}>
            {errors.form}
          </p>
        )}
        {success && (
          <p data-testid="success-message" style={{ color: 'green' }}>
            {success}
          </p>
        )}
      </form>
    </section>
  )
}
