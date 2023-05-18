# Reputation-Settlement-Discord-Bot
Aplikacja wspomagająca prowadzenie systemu Fallout 2d20. Założenia i obsługa są proste.

W pierwszej kolejności należy uruchomić `database.py` by utworzyć bazę danych.

Wybieramy kanał na discrodzie tworzymy na nim webhook, następnie uruchamiamy `main.py` uruchomi się nam poniższe okno:
![image](https://github.com/D1025/Reputation-Settlement-Discord-Bot/assets/69533622/5031e557-116b-4137-ac17-7d9760dbc556)

Z drobną różnicą, pole pod main window które jest combo-boxem będzie puste, ponieważ tu wybieramy nasze połączone webhooki.

W pole `name` wpisujemy nazwę naszego webhooka, a w `url` link wygenerowany przez discord do webhooka i klikamy `Add`.

Po dodaniu możemy wybrać naszego webhooka kliknąć `Connect` i przejść do głównego menu:
![image](https://github.com/D1025/Reputation-Settlement-Discord-Bot/assets/69533622/9ac3ea25-b14d-44bd-9af8-51f636b0efba)

nad `add module` możemy wybrać nazwę modułu i klikając w guzik doda się do naszej listy. Możemy mieć tyle takich modułów - settlementów ile potrzebujemy.

Zmiany po prawej stronie które wprowadzimy nie zapisują się od razu. Po kliknięciu `push` zostają zapisane a wiadomość na kanale discord o następojuącym wyglądzie z naszymi wprowadzonymi danymi będzie wyglądać tak:
![image](https://github.com/D1025/Reputation-Settlement-Discord-Bot/assets/69533622/beaa32dd-1a8f-4ad3-873f-6a58fcc7e6cf)

Po zmianie wartości i kliknięciu `push` zmiany zostaną wprowadzone także w oryginalnej wiadomości
