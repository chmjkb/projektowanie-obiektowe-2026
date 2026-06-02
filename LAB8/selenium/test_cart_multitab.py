"""10.4.0 - synchronizacja koszyka między kartami przeglądarki.

Cart Provider w aplikacji persystuje stan w localStorage i nasłuchuje
zdarzenia 'storage', dzięki czemu zmiana w jednej karcie propaguje się
do innych otwartych kart tej samej domeny.
"""

from __future__ import annotations

from selenium.webdriver.common.by import By

from conftest import wait_until


def _open_with_clean_storage(driver, frontend_url: str) -> None:
    driver.get(f"{frontend_url}/")
    driver.execute_script("window.localStorage.clear();")
    driver.get(f"{frontend_url}/")
    wait_until(
        lambda: driver.find_elements(By.XPATH, "//button[contains(text(), 'Dodaj do koszyka')]")
    )


def _cart_item_rows(driver):
    return driver.find_elements(By.CSS_SELECTOR, "section ul li")


def test_cart_persists_to_local_storage(driver, frontend_url):
    """Dodanie produktu -> localStorage zawiera koszyk."""
    _open_with_clean_storage(driver, frontend_url)
    driver.find_element(
        By.XPATH, "//button[contains(text(), 'Dodaj do koszyka')]"
    ).click()
    wait_until(
        lambda: driver.execute_script(
            "return JSON.parse(window.localStorage.getItem('lab5:cart') || '[]').length;"
        )
        >= 1
    )
    raw = driver.execute_script("return window.localStorage.getItem('lab5:cart');")
    assert raw is not None
    assert '"quantity":1' in raw


def test_new_tab_loads_cart_from_local_storage(driver, frontend_url):
    """Nowa karta po dodaniu produktu w pierwszej widzi ten sam koszyk (initial load)."""
    _open_with_clean_storage(driver, frontend_url)
    driver.find_element(
        By.XPATH, "//button[contains(text(), 'Dodaj do koszyka')]"
    ).click()
    wait_until(
        lambda: driver.execute_script(
            "return JSON.parse(window.localStorage.getItem('lab5:cart') || '[]').length;"
        )
        >= 1
    )

    driver.switch_to.new_window("tab")
    driver.get(f"{frontend_url}/cart")
    wait_until(lambda: _cart_item_rows(driver))

    rows = _cart_item_rows(driver)
    assert len(rows) == 1, f"Expected 1 cart row in new tab, got {len(rows)}"


def test_storage_event_propagates_changes_to_open_tab(driver, frontend_url):
    """Tab A i Tab B otwarte równolegle - zmiana w A pojawia się w B."""
    _open_with_clean_storage(driver, frontend_url)
    tab_a = driver.current_window_handle

    driver.switch_to.new_window("tab")
    tab_b = driver.current_window_handle
    driver.get(f"{frontend_url}/cart")
    wait_until(lambda: driver.find_elements(By.TAG_NAME, "h2"))

    initial_rows = len(_cart_item_rows(driver))

    driver.switch_to.window(tab_a)
    driver.find_element(
        By.XPATH, "//button[contains(text(), 'Dodaj do koszyka')]"
    ).click()

    driver.switch_to.window(tab_b)
    grew = wait_until(lambda: len(_cart_item_rows(driver)) > initial_rows, timeout=5.0)
    assert grew, "Tab B nie zsynchronizował koszyka po zmianie w tab A"

    rows_b = _cart_item_rows(driver)
    assert len(rows_b) == initial_rows + 1


def test_clearing_cart_in_one_tab_clears_other(driver, frontend_url):
    """Usunięcie pozycji w jednej karcie usuwa ją w drugiej."""
    _open_with_clean_storage(driver, frontend_url)
    driver.find_element(
        By.XPATH, "//button[contains(text(), 'Dodaj do koszyka')]"
    ).click()
    wait_until(
        lambda: driver.execute_script(
            "return JSON.parse(window.localStorage.getItem('lab5:cart') || '[]').length;"
        )
        >= 1
    )

    tab_a = driver.current_window_handle
    driver.switch_to.new_window("tab")
    tab_b = driver.current_window_handle
    driver.get(f"{frontend_url}/cart")
    wait_until(lambda: _cart_item_rows(driver))
    assert _cart_item_rows(driver)

    driver.switch_to.window(tab_a)
    driver.get(f"{frontend_url}/cart")
    wait_until(lambda: driver.find_elements(By.XPATH, "//button[contains(text(), 'Wyczyść koszyk')]"))
    driver.find_element(By.XPATH, "//button[contains(text(), 'Wyczyść koszyk')]").click()

    driver.switch_to.window(tab_b)
    emptied = wait_until(lambda: not _cart_item_rows(driver), timeout=5.0)
    assert emptied, "Tab B nadal pokazuje pozycje po wyczyszczeniu w tab A"
