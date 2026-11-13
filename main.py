from bakery import assert_equal
from drafter import *
from dataclasses import dataclass



hide_debug_information()
set_website_title("Your Drafter Website")
set_website_framed(False)

@dataclass
class Book:
    title:str
    author:str
    length:int
    rating:float
    filepath:str
    
@dataclass
class State:
    safe_key:list[int]
    safe_attempt:list[int]
    darkmode:bool
    shelf_books:list[Book]
    safe_books:list[Book]
    message:str
    
#helper functions
def show(state: State, content:list) -> Page:
    """puts the message at the top and does the darkmode check."""
    msg = state.message
    state.message = ""
    if state.darkmode:
        return Page(state, [Div(msg, *content, style_background_color="black", style_color="white")])
    return Page(state, [Div(msg, *content])
def find_book(books:list[Book], title: str) -> Book | None:
    """finds the title of the requested book and returns it if it exists, otherewise None"""
    for book in books:
        if book.title == title:
            return book
    return None

#pages
@route
def index(state: State) -> Page:
    return Page(state, [Header("The Room"),
                       Button("Toggle dark mode", toggle_darkmode),
                       Button("Go to shelf", shelf),
                       Button("Go to safe", safe),
                       ])
@route
def shelf(state: State) -> Page:
    content = [Header("Shelf")]
    for book in state.shelf_books:
        content.append(book.title + " by " + book.author + " (" + str(book.length) + " pages, " + str(book.rating) + " stars)")
        content.append(Button("Open", open_book, [Argument("title", book.title)]))
        content.append(Button("Remove", remove_book, [Argument("title", book.title)]))
        if len(state.shelf_books) > 1:
            content.append(Selectbox("sort_by", ["title","author","length","rating"]))
            content.append(Checkbox("Reverse sort"))
            content.append(Button("Sort", sort_books))
        content.append(Button("Add a book", add_book_page))
        content.append(Button("Back", index))
    return Page(state, content)
@route 
def add_book_page(state: State) -> Page:
    return Page(state, [
        Header("Add a book"),
        "Title", TextBox("title"),
        "Author", TextBox("author"),
        "Length", TextBox("length"),
        "Rating (0-5 float)", TextBox("rating"),
        "Text file path", TextBox("filepath"),
        Button("Add", add_book),
        Button("Back", shelf),
    ])
@route 
def safe(state: State) -> Page:
    dots = "●" * len(state.safe_attempt) + "○" * (3 - len(state.safe_attempt))
    return Page(state, [
        Header("Safe"),
        dots,
        Textbox("digit"),
        Button("Enter number", input_attempt),
        Button("Back", index),
    ])
@route
def inside_safe(state: State) -> Page:
    content = [Header("Inside the Safe")]
    for book in state.safe_books:
        content.append(book.title)
        content.append(Button("Open", open_book, [Argument("title", book.title)]))
        content.append(Button("Take out", remove_from_safe, [Argument("title", book.title)]))
    if len(state.shelf_books) > 0:
        content.append(SelectBox("title", [b.title for b in state.shelf_books]))
        content.append(Button("Put in safe", add_to_safe))
    conntent.append(Button("Back", index))
    return Page(state, content)
@route
def open_book(state: State, title:str) -> Page:
    book = find_book(state.shelf_books, title)
    if book is None:
        book = find_book(state.safe_books, title)
    text = "(no text!)"
    try:
        with open(book.filepath) as f:
            text = f.read()
    except OSError:
        text = "Could not read file!"
    return Page(state, [
        Header(book.title),
        text,
        Button("Back", shelf),
    ])

#Routes w/o pages
@route 
def toggle_darkmode(state: State) ->Page:
    state.darkmode = not state.darkmode
    return index(state)
@route
def add_book(state: State, title:str, author:str, length:int, rating:float, filepath:str ) -> Page:
    if title == "" or author == "":
        state.message = "Title and author are required!"
        return add_book_page(state)
    if not length.isdigit():
        state.message = "Length must be a whole number!"
        return add_book_page(state)
    if find_book(state.shelf_books + state.safe_books, title) is not None:
        state.message = "Title aready exists!"
        return add_book_page(state)
    state.shelf_books.append(Book(title, author, int(length), float(rating), filepath))
    return shelf(state)
@route 
def remove_book(state: State, title:str) -> Page:
    state.shelf_books.remove(find_book(state.shelf_books, title))
    return shelf(state)
@route
def sort_books(state: State) -> Page:
    return shelf(state)
@route 
def input_attempt(state: State, digit:int) -> Page:
    # characters to display safe progress ● ○
    if len(state.safe_attempt) >= 3:
        return open_safe(state)
    else:
        return safe(state)
@route
def open_safe(state: State) -> Page:
    if True:
        return inside_safe(state)
    else:
        return safe(state)
@route 
def add_to_safe(state: State) -> Page:
    return inside_safe(state)
@route
def remove_from_safe(state: State) -> Page:
    return inside_safe(state)

start_server(State([4, 2, 7], [], False, [], [], ""))
