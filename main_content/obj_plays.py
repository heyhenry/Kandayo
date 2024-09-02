class Book:
    def __init__(self, title, pages, snackies):
        self.title = title
        self.pages = pages
        self.snackies = snackies

class Snacks:
    def __init__(self, snack_type, snack_colour):
        self.snack_type = snack_type   
        self.snack_colour = snack_colour

s1 = Snacks('Banana', 'Yellow')
b1 = Book('Geronimo', 99, s1)

books = {'Geronimo': b1}
print(books['Geronimo'].snackies.snack_type)