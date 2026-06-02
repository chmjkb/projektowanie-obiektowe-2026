
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=chmjkb_projektowanie-obiektowe-2026&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=chmjkb_projektowanie-obiektowe-2026)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=chmjkb_projektowanie-obiektowe-2026&metric=bugs)](https://sonarcloud.io/summary/new_code?id=chmjkb_projektowanie-obiektowe-2026)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=chmjkb_projektowanie-obiektowe-2026&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=chmjkb_projektowanie-obiektowe-2026)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=chmjkb_projektowanie-obiektowe-2026&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=chmjkb_projektowanie-obiektowe-2026)

**Zadanie 1** Pascal

:white_check_mark: 3.0 Procedura do generowania 50 losowych liczb od 0 do 100 [Link do commita 1](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/c14c341562c4f7749b4fe018d804e4d3c1dd2043)

:white_check_mark: 3.5 Procedura do sortowania liczb [Link do commita2 ](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/712d6536db502e6741fd3e81cf3df0fc4f367259)

:white_check_mark: 4.0 Dodanie parametrów do procedury losującej określającymi zakres [Link do commita 3](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/6b720566dc1967fa0506fdb5f6a0c54bad6fece8)

:white_check_mark: 4.5 5 testów jednostkowych testujące procedury [Link do commita 4](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/57ceecef2cad4bef9562989ceac59ca87461df5e)

:white_check_mark: 5.0 Skrypt w bashu do uruchamiania aplikacji w Pascalu via docker [Link do commita 5](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/aa53df0c74ce5d917fb327479bd6ec834ad7d997)

**Zadanie 2** Wzorce architektury 

Należy stworzyć aplikację webową na bazie frameworka Symfony na
obrazie kprzystalski/projobj-php:latest. Baza danych dowolna, sugeruję
SQLite.

:white_check_mark: 3.0 Należy stworzyć jeden model z kontrolerem z produktami, zgodnie z
CRUD (JSON) - [Link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/7ae53ff893c5cbedd2479e688d2ccde3d4fb2d22)

:white_check_mark: 3.5 Należy stworzyć skrypty do testów endpointów via curl (JSON) - [Link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/1b8d77d5e919aa1719e82cf06ae720a0f2ef765d)

:white_check_mark: 4.0 Należy stworzyć dwa dodatkowe kontrolery wraz z modelami  (JSON) - [Link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/83455acfc536b6ff838c84988f66b5b09549cd5a)

**Zadanie 3** Wzorce kreacyjne


Spring Boot (Kotlin)
Proszę stworzyć prosty serwis do autoryzacji, który zasymuluje
autoryzację użytkownika za pomocą przesłanej nazwy użytkownika oraz
hasła. Serwis powinien zostać wstrzyknięty do kontrolera (4.5).
Aplikacja ma oczywiście zawierać jeden kontroler i powinna zostać
napisana w języku Kotlin. Oparta powinna zostać na frameworku Spring
Boot. Serwis do autoryzacji powinien być singletonem.

:white_check_mark: 3.0 Należy stworzyć jeden kontroler wraz z danymi wyświetlanymi z
listy na endpoint’cie w formacie JSON - Kotlin + Spring Boot - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/11fe9390ee16a697045fdef3218f31ad4dfce691)

:white_check_mark: 3.5 Należy stworzyć klasę do autoryzacji (mock) jako Singleton w
formie eager - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/67701c7ac2610e13d0e67a348ebc519ae3351ada)

:white_check_mark: 4.0 Należy obsłużyć dane autoryzacji przekazywane przez użytkownika - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/b7ac3e33dc9009fe9ad252454bcadb9eeb8e81aa)

:white_check_mark: 4.5 Należy wstrzyknąć singleton do głównej klasy via @Autowired lub
kontruktor (constructor injection) - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/9c4a2ae88c44e8a505ed0573c4c70dc39597243f)

:white_check_mark: 5.0 Obok wersji Eager do wyboru powinna być wersja Singletona w wersji
lazy - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/7eda836632f6e44f17548d76d663b53c0642373a)


**Zadanie 4** Wzorce strukturalne

Echo (Go)
Należy stworzyć aplikację w Go na frameworku echo. Aplikacja ma mieć
jeden endpoint, minimum jedną funkcję proxy, która pobiera dane np. o
pogodzie, giełdzie, etc. (do wyboru) z zewnętrznego API. Zapytania do
endpointu można wysyłać w jako GET lub POST. - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/7eda836632f6e44f17548d76d663b53c0642373a)

:white_check_mark: 3.0 Należy stworzyć aplikację we frameworki echo w j. Go, która będzie
miała kontroler Pogody, która pozwala na pobieranie danych o pogodzie
(lub akcjach giełdowych) - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/9487c69df915e1aa02caef683406a8f85e277e5f)

:white_check_mark: 3.5 Należy stworzyć model Pogoda (lub Giełda) wykorzystując gorm, a
dane załadować z listy przy uruchomieniu - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/41b3b327997791af13692be730a1e42dd283bb94)

:white_check_mark: 4.0 Należy stworzyć klasę proxy, która pobierze dane z serwisu
zewnętrznego podczas zapytania do naszego kontrolera - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/9b228c3f5be637e114e959ecb97614f6ef24992c)

:white_check_mark: 4.5 Należy zapisać pobrane dane z zewnątrz do bazy danych - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/ac1286079e2b622e8f8f13b9315b49e752cd7b84)

:white_check_mark: 5.0 Należy rozszerzyć endpoint na więcej niż jedną lokalizację
(Pogoda), lub akcje (Giełda) zwracając JSONa - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/e3c864408cabd31790231e4fb5ad3b403fc03bd1)

**Zadanie 5** Wzorce behawioralne

:white_check_mark: 3.0 W ramach projektu należy stworzyć komponenty Produkty oraz
Płatności; komponent Produkty powinien pobierać listę produktów z
aplikacji serwerowej, natomiast komponent Płatności powinien wysyłać
dane płatności do aplikacji serwerowej. - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/22debf5)

:white_check_mark: 3.5 Należy dodać komponent Koszyk wraz z osobnym widokiem; aplikacja powinna umożliwiać przechodzenie pomiędzy widokami przy użyciu routingu. - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/51bc0fa)

:white_check_mark: 4.0 Dane pomiędzy komponentami, takimi jak Produkty, Koszyk i Płatności, powinny być przekazywane z wykorzystaniem React hooks, np. useState, useEffect lub useContext. - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/c1e129d)

:white_check_mark: 4.5 Należy przygotować konfigurację umożliwiającą uruchomienie
aplikacji klienckiej oraz serwerowej w kontenerach Docker za pomocą
docker-compose. - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/756d429)

:white_check_mark: 5.0 Należy wykorzystać bibliotekę axios do komunikacji z serwerem oraz
skonfigurować obsługę CORS, aby frontend mógł poprawnie komunikować
się z backendem. - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/d535e04)

**Zadanie 8** Zapaszki

Należy sprawdzić kod projektów JS 3.0, 3.5, 4.0, kotlin, go, js - 4.5, 5.0.

:white_check_mark: 3.0 Należy skonfigurować husky + lint-staged uruchamianie lintowania przed commitem - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/375700f)

:white_check_mark: 3.5 Należy wyeliminować wszystkie bugi w kodzie w Sonarze (kod aplikacji klienckiej) - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/87fc2ff)

:white_check_mark: 4.0 Przeskanować oraz naprawić dowolny projekt open source narzędziem CodeQL https://codeql.github.com/ - skan tego repozytorium (Go + JS/TS), naprawione: brak timeoutu HTTP, nieobsłużone błędy `AutoMigrate`/`Create`/`Body.Close` w LAB4 - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/e133224)

:white_check_mark: 4.5 Należy usunąć problemy typu Code Smell w kodzie w Sonarze (kotlin, go, js). Należy dodać badge z Sonara - badge widoczny u góry README; naprawione: `AuthService` jako `object` (Kotlin), `WeatherService` → `WeatherFetcher` zgodnie z konwencją Go, readonly props w `CartProvider` (React/TS) - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/f6e46c6)

:white_check_mark: 5.0 Skonfigurować Github Actions z linterem oraz CodeQL - workflowy `.github/workflows/lint.yml` (ESLint na LAB5/frontend) oraz `.github/workflows/codeql.yml` (Go + JS/TS) - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/7a295cf)

**Zadanie 9** Vapor (Swift) — Fluent + Leaf + Redis

Aplikacja w Vaporze wykorzystująca Leaf jako silnik szablonów oraz
Fluent jako ORM. Trzy modele oraz CRUD dla każdego z nich, model
z minimum jedną relacją, CRUD odzwierciedlony w szablonach.

:white_check_mark: 9.3.0 Kontroler wraz z modelem Produktów zgodny z CRUD w ORM Fluent - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/bd671f7)

:white_check_mark: 9.3.5 Szablony w Leaf dla CRUD produktów - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/2fa76f2)

:white_check_mark: 9.4.0 Drugi model oraz kontroler Kategorii wraz z relacją Parent/Children - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/c54b17a)

:white_check_mark: 9.4.5 Wykorzystanie Redis do przechowywania (cache listy produktów z TTL 60s) - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/624b0ae)

:white_check_mark: 9.5.0 Konfiguracja deploymentu na Heroku (Procfile, app.json, buildpack) - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/71fab09)

**Zadanie 10** Selenium/WebDriver + Playwright (testy aplikacji LAB5)

:white_check_mark: 10.3.0 Testy walidacji pól obowiązkowych i formatu adresu e-mail w formularzu rejestracji - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/3870c3e)

:white_check_mark: 10.3.5 Testy bezpieczeństwa XSS - próby wstrzyknięcia JavaScriptu w aplikacji React - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/ab24e4d)

:white_check_mark: 10.4.0 Testy koszyka zakupowego przy otwarciu aplikacji w kilku kartach przeglądarki - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/41cdb2a)

:white_check_mark: 10.4.5 Formularz logowania + testy podatności CSRF (zmiana ustawień konta spreparowanym linkiem) - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/1a7892c)

:white_check_mark: 10.5.0 Scenariusz End-to-End w Playwright (56 asercji) - [link do commita](https://github.com/chmjkb/projektowanie-obiektowe-2026/commit/0f0248b)
