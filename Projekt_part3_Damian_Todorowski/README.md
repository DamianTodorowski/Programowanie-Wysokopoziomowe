# System Biblioteczny (Wersja Obiektowo-Funkcyjna)

Projekt stanowi rozwinięcie systemu zarządzania biblioteką z Części 2 (`Projekt_part2_Damian_Todorowski`). Do logiki obiektowej dodano elementy programowania funkcyjnego (FP), takie jak wyrażenia lambda, funkcje wyższego rzędu (HOF), mapowanie, filtrowanie, sortowanie przy użyciu dedykowanych kluczy oraz list comprehensions.

## Nowe Funkcjonalności

1. **Opcje Katalogu (Wyszukiwanie, Filtrowanie, Sortowanie):**
   - Dodano podmenu do zarządzania widokiem katalogu.
   - **Filtrowanie:** Możliwość wyszukiwania po frazie w tytule lub autorze oraz opcjonalne wyświetlanie tylko książek aktualnie dostępnych (sztuki > 0). Zaimplementowane przy użyciu funkcji `filter` z predykatem przekazanym jako wyrażenie `lambda`.
   - **Sortowanie:** Możliwość posortowania książek po tytule, autorze lub dostępnych sztukach. Zaimplementowane za pomocą funkcji `sorted()` z kluczem w postaci wyrażenia `lambda`.

2. **System Rezerwacji:**
   - Jeśli książka ma 0 dostępnych sztuk, czytelnik może ją zarezerwować (z poziomu menu głównego lub bezpośrednio po nieudanej próbie wypożyczenia).
   - Wypożyczenie książki automatycznie usuwa rezerwację danego użytkownika na ten tytuł.
   - Przy rozpatrywaniu próśb o przedłużenie wypożyczenia przez bibliotekarza, system wyświetla ostrzeżenie: `[UWAGA: Istnieje rezerwacja na tę książkę!]` jeśli na dany tytuł czekają inni czytelnicy.

3. **Statystyki Biblioteki (dla Bibliotekarza):**
   - Wyświetlanie **najpopularniejszej książki** (największa różnica między łączną pulą a dostępnymi egzemplarzami) przy użyciu funkcji `max()` z odpowiednim kluczem `lambda`.
   - Obliczanie **łącznej liczby aktywnych wypożyczeń** przy użyciu generator expression oraz funkcji `sum()`.
   - Wyświetlanie **rankingu czytelników** posortowanego malejąco wg liczby wypożyczonych książek za pomocą `sorted()` z kluczem `lambda`.
   - Cała logika statystyk została zrealizowana bez użycia pętli `for` czy `while` z ręczną akumulacją.

4. **Funkcja Wyższego Rzędu (Higher-Order Function):**
   - Metoda `display_filtered_books(predicate)` w klasie `Library` to uniwersalna funkcja wyświetlająca katalog, która przyjmuje inną funkcję (`predicate`) jako argument.

---

## Spełnienie Wymagań Technicznych

- **Co najmniej 3 użycia lambda (w kodzie jest ich 6+):**
  - Lambda filtrująca frazę i dostępność książek.
  - Lambdy określające klucze sortowania dla tytułów, autorów i dostępnych sztuk.
  - Lambda do wyznaczania najpopularniejszej książki (kryterium różnicy sztuk).
  - Lambda do sortowania rankingu użytkowników po długości listy wypożyczeń.
- **Co najmniej 2 użycia comprehension (list/dict comprehensions):**
  - Pobieranie rezerwacji zalogowanego czytelnika: `[b for b in library._books if self in b.reservations]`.
  - Wyciąganie listy czytelników do statystyk: `[u for u in self._users if isinstance(u, Reader)]`.
  - Formatowanie rankingu czytelników: `[f"- {r.login}: {len(r.borrowed)} wypożyczonych..." for r in sorted_readers]`.
- **Brak pętli w nowej logice danych:**
  - Wszelkie operacje wyszukiwania, sortowania, filtrowania i obliczania statystyk są robione za pomocą narzędzi funkcyjnych (`filter`, `map`, `sum`, `sorted`, `max`).
  - Do wyświetlania list bez pętli użyto funkcyjnego mapowania: `list(map(print, ...))`.

## Uruchomienie Programu

Program można uruchomić poleceniem:
```bash
python biblioteka_funkcyjnie.py
```

### Dane Testowe:
- Czytelnicy:
  - `adam` / `p1`
  - `kuba` / `p2`
  - `damian` / `p3`
- Bibliotekarz:
  - `admin` / `admin123`

  *README wygenerowano automatycznie przy użyciu AI.*
