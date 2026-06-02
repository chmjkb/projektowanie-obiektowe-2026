import { useEffect, useState } from 'react'
import { changeEmail, fetchMe, logoutUser } from '../api'
import type { User } from '../types'

export function Account() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [newEmail, setNewEmail] = useState('')
  const [status, setStatus] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    fetchMe().then((me) => {
      if (cancelled) return
      setUser(me)
      setLoading(false)
    })
    return () => {
      cancelled = true
    }
  }, [])

  async function reloadMe() {
    const me = await fetchMe()
    setUser(me)
  }

  async function submit(ev: React.FormEvent) {
    ev.preventDefault()
    setStatus(null)
    try {
      const updated = await changeEmail(newEmail)
      setUser(updated)
      setNewEmail('')
      setStatus(`Email zmieniony na ${updated.email}`)
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : String(err)
      setStatus(`Błąd: ${message}`)
    }
  }

  async function logout() {
    await logoutUser()
    await reloadMe()
  }

  if (loading) return <p>Wczytywanie...</p>

  if (!user) {
    return (
      <section>
        <h2>Moje konto</h2>
        <p data-testid="not-authenticated">Nie jesteś zalogowany.</p>
      </section>
    )
  }

  return (
    <section>
      <h2>Moje konto</h2>
      <p>
        Zalogowany jako <strong data-testid="current-username">{user.username}</strong>
      </p>
      <p>
        Email: <span data-testid="current-email">{user.email}</span>
      </p>

      <h3>Zmień email</h3>
      <form onSubmit={submit} data-testid="change-email-form">
        <input
          data-testid="new-email-input"
          value={newEmail}
          onChange={(e) => setNewEmail(e.target.value)}
          required
        />
        <button type="submit" data-testid="change-email-submit">
          Zmień
        </button>
      </form>
      {status && <p data-testid="change-email-status">{status}</p>}

      <p style={{ marginTop: '1.5rem' }}>
        <button type="button" onClick={logout} data-testid="logout-button">
          Wyloguj
        </button>
      </p>
    </section>
  )
}
