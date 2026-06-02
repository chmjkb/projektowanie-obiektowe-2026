"""10.4.5 - test podatności CSRF.

Endpoint POST /me/email zmienia email zalogowanego użytkownika bazując
wyłącznie na cookie sesyjnym - brak tokenu CSRF. Test:

1. Rejestruje + loguje użytkownika w karcie A.
2. W karcie B otwiera spreparowaną stronę `/csrf-demo`, która automatycznie
   wysyła POST do `/me/email` używając cookies ofiary.
3. Wraca do karty A, odświeża widok konta i potwierdza, że email został
   zmieniony przez "atakującego" bez wiedzy użytkownika.

Strona ataku jest hostowana z tego samego backendu (same-origin), by
ominąć ograniczenia SameSite=Lax w przeglądarce bez konfiguracji HTTPS.
Vulnerability (brak walidacji tokenu CSRF) jest jednak identyczna jak
w przypadku ataku cross-origin.
"""

from __future__ import annotations

from selenium.webdriver.common.by import By

from conftest import wait_until


def _register_and_login(driver, frontend_url: str, user: dict[str, str]) -> None:
    driver.get(f"{frontend_url}/register")
    wait_until(lambda: driver.find_elements(By.CSS_SELECTOR, '[data-testid="register-form"]'))
    driver.find_element(By.CSS_SELECTOR, '[data-testid="username-input"]').send_keys(user["username"])
    driver.find_element(By.CSS_SELECTOR, '[data-testid="email-input"]').send_keys(user["email"])
    driver.find_element(By.CSS_SELECTOR, '[data-testid="password-input"]').send_keys(user["password"])
    driver.find_element(By.CSS_SELECTOR, '[data-testid="submit-button"]').click()
    wait_until(
        lambda: driver.find_elements(By.CSS_SELECTOR, '[data-testid="success-message"]'),
        timeout=8.0,
    )

    driver.get(f"{frontend_url}/login")
    wait_until(lambda: driver.find_elements(By.CSS_SELECTOR, '[data-testid="login-form"]'))
    driver.find_element(By.CSS_SELECTOR, '[data-testid="login-username"]').send_keys(user["username"])
    driver.find_element(By.CSS_SELECTOR, '[data-testid="login-password"]').send_keys(user["password"])
    driver.find_element(By.CSS_SELECTOR, '[data-testid="login-submit"]').click()
    wait_until(
        lambda: driver.find_elements(By.CSS_SELECTOR, '[data-testid="current-username"]'),
        timeout=8.0,
    )


def test_csrf_attack_changes_email(driver, frontend_url, backend_url, unique_user):
    _register_and_login(driver, frontend_url, unique_user)

    initial_email = driver.find_element(By.CSS_SELECTOR, '[data-testid="current-email"]').text
    assert initial_email == unique_user["email"]

    victim_tab = driver.current_window_handle
    driver.switch_to.new_window("tab")
    driver.get(f"{backend_url}/csrf-demo")

    status = wait_until(
        lambda: driver.execute_script(
            "return document.body.dataset.csrfStatus;"
        )
        in ("200", "201"),
        timeout=8.0,
    )
    assert status, (
        "Strona ataku nie zdążyła wysłać żądania CSRF, "
        f"status: {driver.execute_script('return document.body.dataset.csrfStatus;')}"
    )

    driver.switch_to.window(victim_tab)
    driver.refresh()

    new_email = wait_until(
        lambda: (
            els := driver.find_elements(By.CSS_SELECTOR, '[data-testid="current-email"]')
        )
        and els[0].text != initial_email
        and els[0].text,
        timeout=5.0,
    )
    assert new_email and new_email != initial_email, (
        f"Email nie został zmieniony przez atak CSRF "
        f"(initial={initial_email!r}, after={new_email!r})"
    )
    assert "attacker" in new_email.lower(), (
        f"Spodziewałem się emaila atakującego, dostałem {new_email!r}"
    )


def test_change_email_works_with_valid_session_via_ui(driver, frontend_url, unique_user):
    """Kontrola pozytywna - normalna ścieżka UI też zmienia email."""
    _register_and_login(driver, frontend_url, unique_user)

    new_email = "legit-new@example.com"
    driver.find_element(By.CSS_SELECTOR, '[data-testid="new-email-input"]').send_keys(new_email)
    driver.find_element(By.CSS_SELECTOR, '[data-testid="change-email-submit"]').click()

    shown = wait_until(
        lambda: (
            els := driver.find_elements(By.CSS_SELECTOR, '[data-testid="current-email"]')
        )
        and els[0].text == new_email,
        timeout=5.0,
    )
    assert shown, "Email nie został zaktualizowany przez UI"
