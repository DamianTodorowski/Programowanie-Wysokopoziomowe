# System Biblioteczny (Wersja Obiektowa)

Projekt przedstawia konsolowy system zarządzania biblioteką zrealizowany w paradygmacie programowania obiektowego (OOP). 

## Struktura projektu

W głównym pliku `biblioteka_obiektowo.py` znajduje się cała logika aplikacji. Poniżej rozpisano za co odpowiadają poszczególne fragmenty kodu:

### 1. Klasa `Book` (Książka)
Odpowiada za reprezentację pojedynczej książki w bibliotece.
- **Atrybuty:** Posiada tytuł, autora oraz zhermetyzowaną (zabezpieczoną) całkowitą i dostępną liczbę sztuk (`_total_count`, `_available_count`).
- **`borrow()`** – obsługuje logikę wypożyczania, pomniejszając dostępną pulę o 1 (jeśli są dostępne sztuki).
- **`return_book()`** – zwiększa dostępną liczbę książek przy zwrocie.

### 2. Klasa `User` (Użytkownik)
Klasa bazowa (rodzic) dla użytkowników logujących się do systemu.
- **Atrybuty:** Przechowuje login, chronione hasło (`_password`) i rolę (np. czytelnik, bibliotekarz).
- **`authenticate()`** – pozwala zweryfikować czy wpisane hasło zgadza się z hasłem przypisanym do użytkownika.
- **`menu()`** – metoda "zaślepka" rzucająca wyjątek `NotImplementedError`. Wymusza na klasach dziedziczących zaimplementowanie własnego menu.

### 3. Klasa `Reader` (Czytelnik)
Dziedziczy po `User`. Odpowiada za akcje zwykłego użytkownika biblioteki.
- **Atrybuty:** Dodatkowo posiada własną listę wypożyczonych książek (`borrowed`) i prośby o przedłużenie (`extension_requests`).
- **`menu()`** – dedykowane menu do przeglądania katalogu, wypożyczania i próśb o przedłużenie.
- **`display_borrowed()`** i **`request_extension()`** – metody pozwalające użytkownikowi zarządzać jego aktywnymi wypożyczeniami.

### 4. Klasa `Librarian` (Bibliotekarz)
Dziedziczy po `User`. Reprezentuje konto administracyjne.
- **`menu()`** – interfejs administratora, który daje możliwość podglądu wszystkich wypożyczeń w systemie. Posiada też osobną opcję do obsługiwania próśb od użytkowników.

### 5. Klasa `Library` (Biblioteka - Baza danych)
Centralny punkt logiki aplikacji integrujący książki i użytkowników.
- **Atrybuty:** `_books` oraz `_users` działają tu jako lokalna baza danych przechowująca utworzone obiekty.
- **`login_system()`** – w pętli pozwala się zalogować po loginie. Sprawdza hasło ograniczając próby wpisania do 3. Zwraca zalogowany obiekt użytkownika.
- **`borrow_book()`** – przeszukuje obiekty książek po nazwie. Jeśli znajdzie pasującą, wywołuje metodę w obiekcie książki i w przypadku sukcesu podpina ją pod konto czytelnika.
- **`display_all_borrowed()`** i **`handle_extension_requests()`** – iterują po wszystkich użytkownikach systemu i pozwalają bibliotekarzowi przeglądać oraz akceptować prośby o przedłużenie książki.

### 6. Funkcje uruchomieniowe
- **`initialize_library()`** – wypełnia początkową listę książek i przypisuje konta testowe (np. konto `admin` / `admin123` oraz czytelników).
- **`application()`** – pętla główna. Obsługuje logowanie użytkowników, a następnie na podstawie tego, kim jest dany użytkownik, odpala dla niego odpowiednie menu (polimorfizm).

---
*README wygenerowano automatycznie przy użyciu AI.*
