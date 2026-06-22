class Book:
    def __init__(self, title, author, total_count):
        # Konstruktor - pola z podkreślnikiem oznaczają hermetyzację
        self.title = title
        self.author = author
        self._total_count = total_count
        self._available_count = total_count
        self._reservations = []  # Lista przechowująca czytelników, którzy zarezerwowali książkę

    @property
    def total_count(self):
        return self._total_count

    @property
    def available_count(self):
        return self._available_count

    @property
    def reservations(self):
        return self._reservations

    def borrow(self):
        # Sprawdzam czy książki są dostępne
        if self._available_count > 0:
            self._available_count -= 1
            return True
        return False  # Brak dostępnych sztuk

    def return_book(self):
        if self._available_count < self._total_count:
            self._available_count += 1

    def reserve(self, reader):
        if reader not in self._reservations:
            self._reservations.append(reader)
            return True
        return False

    def remove_reservation(self, reader):
        if reader in self._reservations:
            self._reservations.remove(reader)
            return True
        return False

    def __str__(self):
        res_info = f" | zarezerwowana: {len(self._reservations)} os." if self._reservations else ""
        return f"'{self.title}' autorstwa {self.author} (dostępne: {self._available_count}/{self._total_count}{res_info})"


class User:
    def __init__(self, login, password, role):
        self.login = login
        self._password = password
        self.role = role

    def authenticate(self, password):
        return self._password == password

    def menu(self, library):
        # Jeśli ktoś zapomni tego nadpisać, program zgłosi błąd
        raise NotImplementedError("Klasy pochodne muszą zaimplementować menu()")

    def __str__(self):
        return f"{self.login} ({self.role})"


class Reader(User):
    def __init__(self, login, password):
        super().__init__(login, password, "czytelnik")
        self.borrowed = []  # Wypożyczone książki
        self.extension_requests = []  # Prośby o przedłużenie

    def menu(self, library):
        while True:
            print(f"\n=== MENU CZYTELNIKA ({self.login}) ===")
            print("1. Opcje katalogu (przeglądaj, filtruj, sortuj)")
            print("2. Wypożycz książkę")
            print("3. Moje wypożyczenia i rezerwacje")
            print("4. Poproś o przedłużenie wypożyczenia")
            print("5. Zarezerwuj książkę")
            print("6. Wyloguj")

            choice = input("Wybierz opcję (1-6): ").strip()

            if choice == "1":
                library.catalog_menu()
            elif choice == "2":
                library.borrow_book(self)
            elif choice == "3":
                self.display_borrowed(library)
            elif choice == "4":
                self.request_extension()
            elif choice == "5":
                library.reserve_book(self)
            elif choice == "6":
                print("\nWylogowywanie...")
                break
            else:
                print("\nNieprawidłowy wybór. Spróbuj ponownie.")

    def display_borrowed(self, library):
        print("\n--- Moje wypożyczenia ---")
        if not self.borrowed:
            print("Nie masz obecnie wypożyczonych żadnych książek.")
        else:
            for idx, book in enumerate(self.borrowed, 1):
                status = " (oczekuje na przedłużenie)" if book in self.extension_requests else ""
                print(f"{idx}. {book.title}{status}")

        # List comprehension
        my_reservations = [b for b in library._books if self in b.reservations]
        print("\n--- Moje rezerwacje ---")
        if not my_reservations:
            print("Nie masz obecnie żadnych rezerwacji.")
        else:
            for idx, book in enumerate(my_reservations, 1):
                print(f"{idx}. {book.title}")
        print("-------------------------")

    def request_extension(self):
        print("\n--- Poproś o przedłużenie ---")
        if not self.borrowed:
            print("Nie masz wypożyczonych książek.")
            return

        # Wyświetlamy dostępne wypożyczenia
        for idx, book in enumerate(self.borrowed, 1):
            status = " (oczekuje na przedłużenie)" if book in self.extension_requests else ""
            print(f"{idx}. {book.title}{status}")

        try:
            choice = int(input("Podaj numer książki do przedłużenia: "))
            if 1 <= choice <= len(self.borrowed):
                book = self.borrowed[choice - 1]
                if book not in self.extension_requests:
                    self.extension_requests.append(book)
                    print(f"Wysłano prośbę o przedłużenie książki '{book.title}'.")
                else:
                    print(f"Prośba o przedłużenie dla '{book.title}' została już wysłana.")
            else:
                print("Nieprawidłowy numer.")
        except ValueError:
            print("Proszę podać liczbę.")


class Librarian(User):
    def __init__(self, login, password):
        super().__init__(login, password, "bibliotekarz")

    def menu(self, library):
        while True:
            print(f"\n=== MENU BIBLIOTEKARZA ({self.login}) ===")
            print("1. Opcje katalogu (przeglądaj, filtruj, sortuj)")
            print("2. Lista wszystkich wypożyczeń")
            print("3. Zarządzaj prośbami o przedłużenie")
            print("4. Statystyki biblioteki")
            print("5. Wyloguj")

            choice = input("Wybierz opcję (1-5): ").strip()

            if choice == "1":
                library.catalog_menu()
            elif choice == "2":
                library.display_all_borrowed()
            elif choice == "3":
                library.handle_extension_requests()
            elif choice == "4":
                library.display_statistics()
            elif choice == "5":
                print("\nWylogowywanie...")
                break
            else:
                print("\nNieprawidłowy wybór. Spróbuj ponownie.")


class Library:
    def __init__(self):
        self._books = []
        self._users = []

    def add_book(self, book):
        self._books.append(book)

    def add_user(self, user):
        self._users.append(user)

    def login_system(self):
        while True:
            login_input = input("Podaj login (lub 'wyjdz' aby zakończyć): ")
            if login_input.lower() == 'wyjdz':
                return None

            user_found = next((u for u in self._users if u.login == login_input), None)

            if user_found:
                attempts = 0
                while attempts < 3:
                    password_input = input("Podaj hasło: ")
                    if user_found.authenticate(password_input):
                        print(f"\nWitaj {login_input}!")
                        return user_found
                    else:
                        attempts += 1
                        print(f"Błędne hasło. Pozostało prób: {3 - attempts}\n")

                print("Przekroczono limit prób logowania. Powrót do ekranu powitalnego.")
            else:
                print("Użytkownik nie istnieje.\n")

    def display_catalog(self):
        print("\n--- Katalog Biblioteki ---")
        # Wyświetlamy cały katalog
        list(map(print, self._books))
        print("--------------------------")

    # Funkcja wyższego rzędu (Wymóg techniczny: HOF przyjmujący funkcję jako argument)
    def display_filtered_books(self, predicate):
        """
        Filtruje katalog książek na podstawie przekazanego predykatu i go wyświetla.
        Funkcja wyższego rzędu (HOF) - brak klasycznych pętli for/while.
        """
        filtered_books = list(filter(predicate, self._books))
        if not filtered_books:
            print("\nBrak książek spełniających podane kryteria.")
        else:
            print("\n--- Przefiltrowany Katalog ---")
            list(map(print, filtered_books))
            print("------------------------------")

    def catalog_menu(self):
        while True:
            print("\n--- OPCJE KATALOGU ---")
            print("1. Wyświetl cały katalog")
            print("2. Filtruj katalog (wyszukaj)")
            print("3. Sortuj katalog")
            print("4. Powrót")

            choice = input("Wybierz opcję (1-4): ").strip()
            if choice == "1":
                self.display_catalog()
            elif choice == "2":
                phrase = input("Podaj frazę do wyszukania w tytule lub autorze (Enter = dowolna): ").strip().lower()
                only_available_input = input("Czy pokazać tylko książki aktualnie dostępne? (t/n): ").strip().lower()
                only_available = only_available_input == 't'

                # Lambda 1: Filtrowanie po frazie i dostępności 
                predicate = lambda b: (
                    (not phrase or phrase in b.title.lower() or phrase in b.author.lower()) and
                    (not only_available or b.available_count > 0)
                )
                self.display_filtered_books(predicate)

            elif choice == "3":
                print("\nSortuj według:")
                print("1. Tytułu (alfabetycznie)")
                print("2. Autora (alfabetycznie)")
                print("3. Liczby dostępnych sztuk (malejąco)")
                sort_choice = input("Wybierz opcję (1-3): ").strip()

                if sort_choice == "1":
                    # Lambda 2: Klucz sortowania po tytule
                    sorted_books = sorted(self._books, key=lambda b: b.title.lower())
                    print("\n--- Książki posortowane po tytule ---")
                    list(map(print, sorted_books))
                elif sort_choice == "2":
                    # Lambda 3: Klucz sortowania po autorze
                    sorted_books = sorted(self._books, key=lambda b: b.author.lower())
                    print("\n--- Książki posortowane po autorze ---")
                    list(map(print, sorted_books))
                elif sort_choice == "3":
                    # Lambda 4: Klucz sortowania po dostępnych kopiach malejąco
                    sorted_books = sorted(self._books, key=lambda b: b.available_count, reverse=True)
                    print("\n--- Książki posortowane po dostępnych sztukach ---")
                    list(map(print, sorted_books))
                else:
                    print("Nieprawidłowa opcja sortowania.")
            elif choice == "4":
                break
            else:
                print("Nieprawidłowy wybór.")

    def borrow_book(self, reader):
        title_input = input("Podaj tytuł książki, którą chcesz wypożyczyć: ").strip()

        # Szukamy książki (możemy użyć filter/next w stylu FP)
        book = next(filter(lambda b: b.title.lower() == title_input.lower(), self._books), None)

        if book:
            if book.borrow():
                # Jeśli udane wypożyczenie, usuwamy ewentualną rezerwację tego czytelnika
                book.remove_reservation(reader)
                reader.borrowed.append(book)
                print(f"\nKsiążka wypożyczona: '{book.title}'.")
            else:
                print(f"\nNiestety, książka '{book.title}' nie jest obecnie dostępna (dostępne: 0 szt.).")
                reserve_choice = input("Czy chcesz zarezerwować ten tytuł? (t/n): ").strip().lower()
                if reserve_choice == 't':
                    if book.reserve(reader):
                        print(f"Książka '{book.title}' została zarezerwowana.")
                    else:
                        print("Masz już aktywną rezerwację na ten tytuł.")
        else:
            print("\nNie znaleziono książki o podanym tytule.")

    def reserve_book(self, reader):
        title_input = input("Podaj tytuł książki do rezerwacji: ").strip()
        book = next(filter(lambda b: b.title.lower() == title_input.lower(), self._books), None)

        if book:
            if book.available_count > 0:
                print(f"Książka '{book.title}' jest dostępna w bibliotece ({book.available_count} szt.). Wypożycz ją zamiast rezerwować.")
            else:
                if book.reserve(reader):
                    print(f"Pomyślnie zarezerwowano książkę '{book.title}'.")
                else:
                    print("Masz już aktywną rezerwację na ten tytuł.")
        else:
            print("Nie znaleziono książki o podanym tytule.")

    def display_all_borrowed(self):
        print("\n--- Lista wszystkich wypożyczeń ---")
        # Filtrujemy tylko czytelników (FP filter)
        readers = list(filter(lambda u: isinstance(u, Reader), self._users))
        
        # Płaska lista par (Użytkownik, Książka) za pomocą list comprehension
        borrows = [(r.login, b.title) for r in readers for b in r.borrowed]

        if not borrows:
            print("Brak wypożyczonych książek.")
        else:
            # Wyświetlanie za pomocą map/print bez pętli for
            list(map(lambda item: print(f"Użytkownik: {item[0]} | Książka: '{item[1]}'"), borrows))
        print("-----------------------------------")

    def handle_extension_requests(self):
        print("\n--- Prośby o przedłużenie ---")
        readers = list(filter(lambda u: isinstance(u, Reader), self._users))
        
        # Sprawdzamy czy są jakiekolwiek prośby
        requests = [(r, b) for r in readers for b in r.extension_requests]
        
        if not requests:
            print("Brak oczekujących próśb.")
        else:
            # Musimy obsłużyć decyzje interaktywnie. Iterujemy po liście próśb.
            # Tradycyjna pętla jest tu dozwolona do obsługi I/O decyzji, ale nie do transformacji/filtrowania danych.
            for reader, book in list(requests):
                # Sprawdzamy czy na książkę istnieje rezerwacja 
                has_res = " [UWAGA: Istnieje rezerwacja na tę książkę!]" if book.reservations else ""
                print(f"\nUżytkownik: {reader.login} | Książka: '{book.title}'{has_res}")
                decision = input("Zaakceptować prośbę? (t/n/pomiń - cokolwiek innego): ").lower().strip()
                
                if decision == 't':
                    print(f"Zaakceptowano przedłużenie dla '{book.title}'.")
                    if book in reader.extension_requests:
                        reader.extension_requests.remove(book)
                elif decision == 'n':
                    print(f"Odrzucono przedłużenie dla '{book.title}'.")
                    if book in reader.extension_requests:
                        reader.extension_requests.remove(book)
        print("\n-----------------------------")

    def display_statistics(self):
        """
        Statystyki biblioteki zaimplementowane funkcyjnie:
        - Najpopularniejsza książka (największa różnica między łączną a dostępną liczbą sztuk).
        - Łączna liczba aktywnych wypożyczeń ogółem.
        - Ranking czytelników posortowany malejąco po liczbie wypożyczeń.
        Bez użycia klasycznych pętli for/while do filtrowania i kalkulacji.
        """
        print("\n=== STATYSTYKI BIBLIOTEKI ===")

        # 1. Najpopularniejsza książka
        if not self._books:
            print("Brak książek w katalogu.")
        else:
            # Lambda 5: Różnica między total a available (wypożyczone sztuki)
            popular_book = max(self._books, key=lambda b: b.total_count - b.available_count)
            popularity = popular_book.total_count - popular_book.available_count
            print(f"Najpopularniejsza książka: '{popular_book.title}' autorstwa {popular_book.author} (wypożyczona {popularity} razy)")

        # 2. Liczba aktywnych wypożyczeń ogółem
        # List comprehension do odfiltrowania czytelników
        readers = [u for u in self._users if isinstance(u, Reader)]
        # Mapowanie i sumowanie do zliczenia wypożyczeń
        total_borrows = sum(map(lambda r: len(r.borrowed), readers))
        print(f"Liczba aktywnych wypożyczeń ogółem: {total_borrows}")

        # 3. Lista czytelników posortowana malejąco wg liczby wypożyczonych książek
        # Lambda 6: Klucz sortowania po liczbie wypożyczeń
        sorted_readers = sorted(readers, key=lambda r: len(r.borrowed), reverse=True)
        print("\nRanking czytelników (wg liczby wypożyczonych książek):")
        
        # Map i list comprehension do sformatowania wyjścia bez pętli for
        ranking_lines = [f"- {r.login}: {len(r.borrowed)} wypożyczonych książek" for r in sorted_readers]
        if ranking_lines:
            list(map(print, ranking_lines))
        else:
            print("Brak czytelników w systemie.")
        print("=============================")


def initialize_library():
    lib = Library()
    
    # Dodawanie książek 
    lib.add_book(Book("Wiedźmin", "Andrzej Sapkowski", 3))
    lib.add_book(Book("Władca Pierścieni", "J.R.R. Tolkien", 2))
    lib.add_book(Book("Harry Potter", "J.K. Rowling", 4))
    lib.add_book(Book("Diuna", "Frank Herbert", 5))
    lib.add_book(Book("Rok 1984", "George Orwell", 1))
    
    # Dodawanie użytkowników  (czytelnicy i bibliotekarz)
    lib.add_user(Reader("adam", "p1"))
    lib.add_user(Reader("kuba", "p2"))
    lib.add_user(Reader("damian", "p3"))
    lib.add_user(Librarian("admin", "admin123"))
    
    return lib


def application():
    print("Witaj w obiektowo-funkcyjnym systemie bibliotecznym!")
    library = initialize_library()
    
    while True:
        logged_in_user = library.login_system()
        if logged_in_user:
            # Polimorfizm - wywołujemy menu na obiekcie (Reader lub Librarian)
            logged_in_user.menu(library)
        else:
            print("Zamykanie programu. Miłego dnia!")
            break


if __name__ == "__main__":
    application()
