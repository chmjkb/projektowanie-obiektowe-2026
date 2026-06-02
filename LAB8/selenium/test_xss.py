"""10.3.5 - testy XSS na aplikacji React.

React domyślnie escape'uje wartości wstawiane w JSX (`{value}`), więc
spreparowane payloady powinny być wyrenderowane jako zwykły tekst, a nie
wykonane jako kod. Testy potwierdzają to zachowanie na trzech polach:

* customer_name w widoku Płatności (wartość jest echo'wana w komunikacie)
* username + email w formularzu rejestracji (echo w komunikacie sukcesu /
  komunikacie błędu walidacji)
"""

from __future__ import annotations

from selenium.webdriver.common.by import By

from conftest import wait_until

XSS_PAYLOADS = [
    "<script>window.__xssed__ = true</script>",
    "<img src=x onerror=\"window.__xssed__=true\">",
    '"><svg onload="window.__xssed__=true">',
]


def _add_first_product_to_cart(driver, frontend_url):
    driver.get(f"{frontend_url}/")
    btn = wait_until(
        lambda: driver.find_elements(By.XPATH, "//button[contains(text(), 'Dodaj do koszyka')]")
    )
    assert btn, "Brak produktów na stronie - czy backend działa?"
    btn[0].click()


def _go_to_payments(driver, frontend_url):
    driver.get(f"{frontend_url}/cart")
    wait_until(lambda: driver.find_elements(By.TAG_NAME, "h2"))
    driver.get(f"{frontend_url}/payments")
    wait_until(lambda: driver.find_elements(By.CSS_SELECTOR, "form"))


def test_xss_in_customer_name_is_rendered_as_text(driver, frontend_url):
    """Skrypt wstrzyknięty w pole customer_name nie powinien się wykonać."""
    for payload in XSS_PAYLOADS:
        driver.execute_script("window.__xssed__ = undefined;")

        _add_first_product_to_cart(driver, frontend_url)
        _go_to_payments(driver, frontend_url)

        input_el = driver.find_element(By.CSS_SELECTOR, 'input[required]')
        input_el.clear()
        input_el.send_keys(payload)

        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        wait_until(lambda: driver.find_elements(By.TAG_NAME, "p"))

        executed = driver.execute_script("return window.__xssed__ === true;")
        assert not executed, f"XSS executed for payload: {payload!r}"

        body_html = driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML") or ""
        assert "<script>window.__xssed__" not in body_html, (
            f"Payload trafił do DOM jako żywy skrypt: {payload!r}"
        )

        assert driver.execute_script(
            "return document.querySelectorAll('script[data-injected]').length"
        ) == 0


def test_xss_in_register_form_username_is_escaped(driver, frontend_url):
    """Spreparowany username nie powinien się wykonać po stronie klienta."""
    driver.execute_script("window.__xssed__ = undefined;")

    driver.get(f"{frontend_url}/register")
    wait_until(lambda: driver.find_elements(By.CSS_SELECTOR, '[data-testid="register-form"]'))

    payload = "<img src=x onerror=window.__xssed__=true>"
    driver.find_element(By.CSS_SELECTOR, '[data-testid="username-input"]').send_keys(payload)
    driver.find_element(By.CSS_SELECTOR, '[data-testid="email-input"]').send_keys("ok@example.com")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="password-input"]').send_keys("haslo123")
    driver.find_element(By.CSS_SELECTOR, '[data-testid="submit-button"]').click()

    wait_until(
        lambda: driver.find_elements(By.CSS_SELECTOR, '[data-testid="success-message"]'),
        timeout=8.0,
    )

    executed = driver.execute_script("return window.__xssed__ === true;")
    assert not executed, "XSS executed via username field"


def test_xss_payload_present_as_literal_text_in_payment_status(driver, frontend_url):
    """Po wysłaniu formy payload powinien być widoczny w DOM jako tekst, nie jako element."""
    driver.execute_script("window.__xssed__ = undefined;")

    _add_first_product_to_cart(driver, frontend_url)
    _go_to_payments(driver, frontend_url)

    payload = "<b>XSS-LITERAL</b>"
    input_el = driver.find_element(By.CSS_SELECTOR, 'input[required]')
    input_el.clear()
    input_el.send_keys(payload)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    wait_until(
        lambda: any(
            "XSS-LITERAL" in p.text
            for p in driver.find_elements(By.TAG_NAME, "p")
        )
    )

    bold_with_payload = [
        b for b in driver.find_elements(By.TAG_NAME, "b") if b.text == "XSS-LITERAL"
    ]
    assert not bold_with_payload, "Payload wyrenderowany jako element <b>, nie jako tekst"
