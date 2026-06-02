"""10.3.0 - testy walidacji formularza rejestracji."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from conftest import wait_until


def _open_register(driver, frontend_url: str) -> None:
    driver.get(f"{frontend_url}/register")
    wait_until(lambda: driver.find_elements(By.CSS_SELECTOR, '[data-testid="register-form"]'))


def test_empty_form_shows_required_field_errors(driver, frontend_url):
    """Pusty formularz pokazuje błędy dla wszystkich wymaganych pól."""
    _open_register(driver, frontend_url)
    driver.find_element(By.CSS_SELECTOR, '[data-testid="submit-button"]').click()

    username_err = wait_until(
        lambda: driver.find_elements(By.CSS_SELECTOR, '[data-testid="username-error"]')
    )
    email_err = driver.find_elements(By.CSS_SELECTOR, '[data-testid="email-error"]')
    password_err = driver.find_elements(By.CSS_SELECTOR, '[data-testid="password-error"]')

    assert username_err and "wymagana" in username_err[0].text.lower()
    assert email_err and "wymagany" in email_err[0].text.lower()
    assert password_err and "wymagane" in password_err[0].text.lower()


def test_invalid_email_format_shows_email_error(driver, frontend_url):
    """Email bez "@" pokazuje błąd 'Niepoprawny format'."""
    _open_register(driver, frontend_url)

    driver.find_element(By.CSS_SELECTOR, '[data-testid="username-input"]').send_keys("janek")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="email-input"]').send_keys("not-an-email")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="password-input"]').send_keys("haslo123")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="submit-button"]').click()

    err = wait_until(
        lambda: driver.find_elements(By.CSS_SELECTOR, '[data-testid="email-error"]')
    )
    assert err, "Brak komunikatu o błędnym emailu"
    assert "niepoprawny" in err[0].text.lower()

    assert not driver.find_elements(By.CSS_SELECTOR, '[data-testid="username-error"]')
    assert not driver.find_elements(By.CSS_SELECTOR, '[data-testid="password-error"]')


def test_invalid_email_missing_tld_shows_error(driver, frontend_url):
    """Email z @ ale bez domeny TLD też powinien być odrzucony."""
    _open_register(driver, frontend_url)

    driver.find_element(By.CSS_SELECTOR, '[data-testid="username-input"]').send_keys("janek")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="email-input"]').send_keys("janek@example")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="password-input"]').send_keys("haslo123")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="submit-button"]').click()

    err = wait_until(
        lambda: driver.find_elements(By.CSS_SELECTOR, '[data-testid="email-error"]')
    )
    assert err and "niepoprawny" in err[0].text.lower()


def test_successful_registration(driver, frontend_url, unique_user):
    """Poprawne dane -> backend zwraca 201, frontend pokazuje sukces."""
    _open_register(driver, frontend_url)

    driver.find_element(By.CSS_SELECTOR, '[data-testid="username-input"]').send_keys(
        unique_user["username"]
    )
    driver.find_element(By.CSS_SELECTOR, '[data-testid="email-input"]').send_keys(
        unique_user["email"]
    )
    driver.find_element(By.CSS_SELECTOR, '[data-testid="password-input"]').send_keys(
        unique_user["password"]
    )
    driver.find_element(By.CSS_SELECTOR, '[data-testid="submit-button"]').click()

    msg = wait_until(
        lambda: driver.find_elements(By.CSS_SELECTOR, '[data-testid="success-message"]'),
        timeout=8.0,
    )
    assert msg, "Brak komunikatu o sukcesie rejestracji"
    assert unique_user["username"] in msg[0].text
