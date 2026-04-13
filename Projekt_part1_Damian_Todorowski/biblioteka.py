# Listy symulujące proste rekordy bazy danych
users = [
    {"login": "adam", "password": "p1", "role": "czytelnik", "borrowed": []},
    {"login": "kuba", "password": "p2", "role": "czytelnik", "borrowed": []},
    {"login": "damian", "password": "p3", "role": "czytelnik", "borrowed": []},
]

books = [
    {"title": "Wiedźmin", "author": "Andrzej Sapkowski", "count": 3},
    {"title": "Władca Pierścieni", "author": "J.R.R. Tolkien", "count": 2},
    {"title": "Harry Potter", "author": "J.K. Rowling", "count": 4},
    {"title": "Diuna", "author": "Frank Herbert", "count": 5},
    {"title": "Rok 1984", "author": "George Orwell", "count": 1},
]


def login():
    """
    Obsługuje logowanie użytkownika.
    Najpierw pyta o login (aż do skutku, jeśli nie istnieje).
    Potem prosi o hasło, dając max 3 szanse na wpisanie poprawnego hasła, po czym blokuje program.
    """
    while True:
        login_input = input("Podaj login: ")

        user_found = None
        # Szukanie użytkownika na liście
        for user in users:
            if user["login"] == login_input:
                user_found = user
                break

        if user_found:
            attempts = 0
            # Walidacja wprowadzenia hasła
            while attempts < 3:
                password_input = input("Podaj hasło: ")
                if user_found["password"] == password_input:
                    print(f"\nWitaj {login_input}!")
                    return user_found
                else:
                    attempts += 1
                    print(f"Błędne hasło. Pozostało prób: {3 - attempts}\n")

            print("Przekroczono limit prób logowania. System został zablokowany.")
            return None
        else:
            print("Użytkownik nie istnieje.\n")


def display_catalog():
    #wyświetlanie katalogu książek
    print("\n--- Katalog Biblioteki ---")
    for book in books:
        print(
            f"Tytuł: '{book['title']}', Autor: {book['author']}, Dostępne sztuki: {book['count']}"
        )
    print("--------------------------")


def borrow_book(current_user):
    """
    Mechanizm wypożyczania: przeszukuje listę żeby znaleźć tytuł, jeśli dany 
    tytuł znajduje się w bibliotece i jest dostępny (sztuki > 0) to przypisuje książkę do konta zalogowanego użytkownika.
    """
    title_input = input("Podaj tytuł książki, którą chcesz wypożyczyć: ")

    for book in books:
        # Porównywanie tytułów bez uwzględniania wielkości liter (.lower())
        if book["title"].lower() == title_input.lower():
            if book["count"] > 0:
                book["count"] -= 1
                # Przypisanie referencji z wykorzystaniem modyfikacji samej listy
                current_user["borrowed"].append(book["title"])
                print(f"\nKsiążka wypożyczona: '{book['title']}'.")
            else:
                print(
                    f"\nNiestety, książka '{book['title']}' nie jest obecnie dostępna."
                )
            return

    print("\nNie znaleziono książki o podanym tytule.")


def display_borrowed(current_user):
    """Odczytuje pole 'borrowed' ze słownika obecnie zalogowanego użytkownika."""
    print("\n--- Moje wypożyczenia ---")
    if len(current_user["borrowed"]) == 0:
        print("Nie masz obecnie wypożyczonych żadnych książek.")
    else:
        # 'enumerate' przydaje się do ładnego numerowania listy i wyciągnięcia indeksu
        for idx, title in enumerate(current_user["borrowed"], 1):
            print(f"{idx}. {title}")
    print("-------------------------")


def main_menu(current_user):
    """
    Główna pętla programu. Pyta użytkownika opcje
    dopóki nie wybierze warunku wyjścia - opcji nr 4 (wyloguj).
    """
    while True:
        print("\n=== MENU GŁÓWNE ===")
        print("1. Przeglądaj książki")
        print("2. Wypożycz książkę")
        print("3. Moje wypożyczenia")
        print("4. Wyloguj")

        choice = input("Wybierz opcję (1-4): ")

        if choice == "1":
            display_catalog()
        elif choice == "2":
            borrow_book(current_user)
        elif choice == "3":
            display_borrowed(current_user)
        elif choice == "4":
            print("\nWylogowywanie...")
            break
        else:
            print("\nNieprawidłowy wybór. Spróbuj ponownie.")


def application():
    #Funkcja inicjująca całą architekturę skryptu 
    print("Witaj w systemie bibliotecznym!")
    logged_in_user = login()

    # Przejście do menu tylko jezeli użytkownik został poprawnie zalogowany
    if logged_in_user is not None:
        main_menu(logged_in_user)

    print("Wylogowano z systemu. Miłego czytania!")


if __name__ == "__main__":
    application()
