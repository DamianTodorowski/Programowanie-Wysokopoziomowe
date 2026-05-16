class Book:
    def __init__(self, title, author, total_count):
        # konstruktor - te z podkreslnikiem to hermetyzacja 
        self.title = title
        self.author = author
        self._total_count = total_count
        self._available_count = total_count

    @property
    def total_count(self):
        return self._total_count

    @property
    def available_count(self):
        return self._available_count

    def borrow(self):
        # sprawdzam czy wgl sa ksiazki
        if self._available_count > 0:
            self._available_count -= 1
            return True
        return False # nie ma

    def return_book(self):
        if self._available_count < self._total_count:
            self._available_count += 1

    def __str__(self):
        return f"'{self.title}' autorstwa {self.author} (dostępne: {self._available_count}/{self._total_count})"


class User:
    def __init__(self, login, password, role):
        self.login = login
        self._password = password
        self.role = role

    def authenticate(self, password):
        return self._password == password

    def menu(self, library):
        # jak ktos zapomni tego nadpisac to program strzeli errorem
        raise NotImplementedError("Klasy pochodne muszą zaimplementować menu()")

    def __str__(self):
        return f"{self.login} ({self.role})"


class Reader(User):
    def __init__(self, login, password):
        # wola konstruktor rodzica zeby przepisac login i haslo
        super().__init__(login, password, "czytelnik")
        self.borrowed = [] # pusta lista na start bo loguje sie bez ksiazek
        self.extension_requests = [] # lista próśb o przedłużenie

    def menu(self, library):
        while True:
            print(f"\n=== MENU CZYTELNIKA ({self.login}) ===")
            print("1. Przeglądaj książki")
            print("2. Wypożycz książkę")
            print("3. Moje wypożyczenia")
            print("4. Poproś o przedłużenie wypożyczenia")
            print("5. Wyloguj")

            choice = input("Wybierz opcję (1-5): ")

            if choice == "1":
                library.display_catalog()
            elif choice == "2":
                library.borrow_book(self)
            elif choice == "3":
                self.display_borrowed()
            elif choice == "4":
                self.request_extension()
            elif choice == "5":
                print("\nWylogowywanie...")
                break
            else:
                print("\nNieprawidłowy wybór. Spróbuj ponownie.")

    def display_borrowed(self):
        print("\n--- Moje wypożyczenia ---")
        if not self.borrowed:
            print("Nie masz obecnie wypożyczonych żadnych książek.")
        else:
            for idx, book in enumerate(self.borrowed, 1):
                status = " (oczekuje na przedłużenie)" if book in self.extension_requests else ""
                print(f"{idx}. {book.title}{status}")
        print("-------------------------")

    def request_extension(self):
        self.display_borrowed()
        if not self.borrowed:
            return # po co liczyc dalej 
        
        try:
            # try-except bo uzytkownicy moga znowu wpisac litery zamiast cyfr...
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
            print("1. Przeglądaj książki")
            print("2. Lista wszystkich wypożyczeń")
            print("3. Zarządzaj prośbami o przedłużenie")
            print("4. Wyloguj")

            choice = input("Wybierz opcję (1-4): ")

            if choice == "1":
                library.display_catalog()
            elif choice == "2":
                library.display_all_borrowed()
            elif choice == "3":
                library.handle_extension_requests()
            elif choice == "4":
                print("\nWylogowywanie...")
                break
            else:
                print("\nNieprawidłowy wybór. Spróbuj ponownie.")


class Library:
    def __init__(self):
        # cala baza danych w listach
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
                # limit do 3 razyzeby nie bylo bruteforce'a
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
        for book in self._books:
            print(book)
        print("--------------------------")

    def borrow_book(self, reader):
        title_input = input("Podaj tytuł książki, którą chcesz wypożyczyć: ")
        
        # iterujemy po wszystkich
        # dajemy lower() zeby nie bylo problemow z wielkimi literami
        for book in self._books:
            if book.title.lower() == title_input.lower():
                if book.borrow():
                    reader.borrowed.append(book)
                    print(f"\nKsiążka wypożyczona: '{book.title}'.")
                else:
                    print(f"\nNiestety, książka '{book.title}' nie jest obecnie dostępna.")
                return
                
        print("\nNie znaleziono książki o podanym tytule.")

    def display_all_borrowed(self):
        print("\n--- Lista wszystkich wypożyczeń ---")
        found_any = False
        for user in self._users:
            if isinstance(user, Reader) and user.borrowed:
                for book in user.borrowed:
                    print(f"Użytkownik: {user.login} | Książka: '{book.title}'")
                    found_any = True
                    
        if not found_any:
            print("Brak wypożyczonych książek.")
        print("-----------------------------------")

    def handle_extension_requests(self):
        print("\n--- Prośby o przedłużenie ---")
        requests_found = False
        for user in self._users:
            if isinstance(user, Reader) and user.extension_requests:
                # Iterujemy po kopii listy, ponieważ będziemy ją modyfikować podczas iteracji
                for book in list(user.extension_requests):
                    requests_found = True
                    print(f"\nUżytkownik: {user.login} | Książka: '{book.title}'")
                    decision = input("Zaakceptować prośbę? (t/n/pomiń - cokolwiek innego): ").lower()
                    
                    if decision == 't':
                        print(f"Zaakceptowano przedłużenie dla '{book.title}'.")
                        user.extension_requests.remove(book)
                    elif decision == 'n':
                        print(f"Odrzucono przedłużenie dla '{book.title}'.")
                        user.extension_requests.remove(book)
                        
        if not requests_found:
            print("Brak oczekujących próśb.")
        print("\n-----------------------------")


def initialize_library():
    lib = Library()
    
    # Dodawanie książek z poprzedniej wersji programu
    lib.add_book(Book("Wiedźmin", "Andrzej Sapkowski", 3))
    lib.add_book(Book("Władca Pierścieni", "J.R.R. Tolkien", 2))
    lib.add_book(Book("Harry Potter", "J.K. Rowling", 4))
    lib.add_book(Book("Diuna", "Frank Herbert", 5))
    lib.add_book(Book("Rok 1984", "George Orwell", 1))
    
    # Dodawanie użytkowników (czytelnicy i nowa rola: bibliotekarz)
    lib.add_user(Reader("adam", "p1"))
    lib.add_user(Reader("kuba", "p2"))
    lib.add_user(Reader("damian", "p3"))
    lib.add_user(Librarian("admin", "admin123"))
    
    return lib


def application():
    print("Witaj w obiektowym systemie bibliotecznym!")
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
