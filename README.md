
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
