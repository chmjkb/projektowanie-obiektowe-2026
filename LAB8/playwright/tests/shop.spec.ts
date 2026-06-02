import { expect, test } from '@playwright/test'

const BACKEND_URL = process.env.BACKEND_URL ?? 'http://localhost:8000'

test('pełny scenariusz E2E sklepu (50+ asercji)', async ({ page, context }) => {
  const ts = Date.now()
  const user = {
    username: `e2e_${ts}`,
    email: `e2e_${ts}@example.com`,
    password: 'haslo123',
  }

  // 1-7: Strona główna + nawigacja
  await page.goto('/')
  await expect(page).toHaveURL(/\/$/)
  await expect(page.getByRole('heading', { level: 1, name: 'Sklep' })).toBeVisible()
  await expect(page.getByRole('link', { name: 'Produkty' })).toBeVisible()
  await expect(page.getByRole('link', { name: 'Koszyk' })).toBeVisible()
  await expect(page.getByRole('link', { name: 'Płatności' })).toBeVisible()
  await expect(page.getByRole('link', { name: 'Rejestracja' })).toBeVisible()
  await expect(page.getByRole('link', { name: 'Logowanie' })).toBeVisible()

  // 8-14: Lista produktów
  await expect(page.getByRole('heading', { name: 'Produkty', level: 2 })).toBeVisible()
  const addButtons = page.getByRole('button', { name: 'Dodaj do koszyka' })
  await expect(addButtons).toHaveCount(5)
  await expect(page.getByText('Kawa')).toBeVisible()
  await expect(page.getByText('Herbata')).toBeVisible()
  await expect(page.getByText('Ciastko')).toBeVisible()
  await expect(page.getByText('Kanapka')).toBeVisible()
  await expect(page.getByText('Sok pomarańczowy')).toBeVisible()

  // 15-17: Pusty koszyk
  await page.getByRole('link', { name: 'Koszyk' }).click()
  await expect(page).toHaveURL(/\/cart$/)
  await expect(page.getByText('Koszyk jest pusty.')).toBeVisible()
  await expect(page.getByText('Suma: 0.00 zł')).toBeVisible()

  // 18-21: Walidacja formularza rejestracji - puste pola
  await page.getByRole('link', { name: 'Rejestracja' }).click()
  await expect(page).toHaveURL(/\/register$/)
  await page.getByTestId('submit-button').click()
  await expect(page.getByTestId('username-error')).toBeVisible()
  await expect(page.getByTestId('email-error')).toBeVisible()
  await expect(page.getByTestId('password-error')).toBeVisible()

  // 22-26: Walidacja - niepoprawne wartości
  await page.getByTestId('username-input').fill('xy')
  await page.getByTestId('email-input').fill('badformat')
  await page.getByTestId('password-input').fill('12345')
  await page.getByTestId('submit-button').click()
  await expect(page.getByTestId('username-error')).toContainText(/co najmniej 3/i)
  await expect(page.getByTestId('email-error')).toContainText(/niepoprawny/i)
  await expect(page.getByTestId('password-error')).toContainText(/co najmniej 6/i)
  await expect(page.getByTestId('username-input')).toHaveValue('xy')
  await expect(page.getByTestId('email-input')).toHaveValue('badformat')

  // 27-29: Sukces rejestracji
  await page.getByTestId('username-input').fill(user.username)
  await page.getByTestId('email-input').fill(user.email)
  await page.getByTestId('password-input').fill(user.password)
  await page.getByTestId('submit-button').click()
  await expect(page.getByTestId('success-message')).toBeVisible()
  await expect(page.getByTestId('success-message')).toContainText(user.username)
  await expect(page).toHaveURL(/\/login$/, { timeout: 5_000 })

  // 30-32: Logowanie
  await page.getByTestId('login-username').fill(user.username)
  await page.getByTestId('login-password').fill(user.password)
  await page.getByTestId('login-submit').click()
  await expect(page).toHaveURL(/\/account$/)
  await expect(page.getByTestId('current-username')).toHaveText(user.username)
  await expect(page.getByTestId('current-email')).toHaveText(user.email)

  // 33-34: Zmiana emaila przez UI
  const newEmail = `e2e_${ts}_new@example.com`
  await page.getByTestId('new-email-input').fill(newEmail)
  await page.getByTestId('change-email-submit').click()
  await expect(page.getByTestId('current-email')).toHaveText(newEmail)
  await expect(page.getByTestId('change-email-status')).toContainText(newEmail)

  // 35-38: Dodanie produktów do koszyka
  await page.getByRole('link', { name: 'Produkty' }).click()
  await expect(page).toHaveURL(/\/$/)
  await addButtons.nth(0).click()
  await addButtons.nth(1).click()
  await addButtons.nth(0).click()
  await page.getByRole('link', { name: 'Koszyk' }).click()
  await expect(page).toHaveURL(/\/cart$/)
  const cartRows = page.locator('section ul li')
  await expect(cartRows).toHaveCount(2)
  await expect(cartRows.first()).toContainText('Kawa × 2')

  // 39-41: Sprawdzenie sumy i drugiego elementu
  await expect(cartRows.nth(1)).toContainText('Herbata × 1')
  await expect(page.getByText(/Suma:.*33\.00 zł/)).toBeVisible()
  await expect(page.getByRole('button', { name: 'Wyczyść koszyk' })).toBeVisible()

  // 42-45: Synchronizacja między kartami
  const page2 = await context.newPage()
  await page2.goto('/cart')
  const cart2Rows = page2.locator('section ul li')
  await expect(cart2Rows).toHaveCount(2)
  await expect(page2.getByText(/Suma:.*33\.00 zł/)).toBeVisible()
  await page2.getByRole('button', { name: 'Usuń' }).first().click()
  await expect(cart2Rows).toHaveCount(1)

  // 46-47: Propagacja zmiany do pierwszej karty
  await page.bringToFront()
  await expect(cartRows).toHaveCount(1)
  await page2.close()

  // 48-51: Płatności + weryfikacja braku XSS
  await page.getByRole('link', { name: 'Płatności' }).click()
  await expect(page).toHaveURL(/\/payments$/)
  await expect(page.getByText(/Do zapłaty:/)).toBeVisible()
  const xssPayload = '<script>window.__pwned__=true</script>'
  await page.locator('input[required]').first().fill(xssPayload)
  await page.getByRole('button', { name: 'Zapłać' }).click()
  await expect(page.getByText('Zapłacono:', { exact: false })).toBeVisible({ timeout: 5_000 })
  const pwned = await page.evaluate(() => (window as unknown as { __pwned__?: boolean }).__pwned__)
  expect(pwned).toBeFalsy()

  // 52-53: Koszyk wyczyszczony po płatności
  await page.getByRole('link', { name: 'Koszyk' }).click()
  await expect(page.getByText('Koszyk jest pusty.')).toBeVisible()
  await expect(page.getByText('Suma: 0.00 zł')).toBeVisible()

  // 54-55: Wylogowanie
  await page.getByRole('link', { name: 'Konto' }).click()
  await expect(page.getByTestId('current-username')).toHaveText(user.username)
  await page.getByTestId('logout-button').click()
  await expect(page.getByTestId('not-authenticated')).toBeVisible()

  // 56-58: Backend potwierdza brak sesji + ponowne logowanie
  const meResp = await page.request.get(`${BACKEND_URL}/me`)
  expect(meResp.status()).toBe(401)
  await page.getByRole('link', { name: 'Logowanie' }).click()
  await page.getByTestId('login-username').fill(user.username)
  await page.getByTestId('login-password').fill(user.password)
  await page.getByTestId('login-submit').click()
  await expect(page.getByTestId('current-username')).toHaveText(user.username)
  await expect(page.getByTestId('current-email')).toHaveText(newEmail)
})
