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
    genre:str
    rating:float
    filepath:str
    
@dataclass
class State:
    safe_key:[int]
    safe_attempt:[int]
    darkmode:bool
    shelf_books:[book]
    safe_books:[book]
    message:str


#pages
@route
def index(state: State) -> Page:
    return Page(state, ["Hello World!"])
@route
def shelf(state: State) -> Page:
    return Page(state, [])
@route 
def add_book_page(state: State) -> Page:
    return Page(state, [])
@route 
def safe(state: State) -> Page:
    return Page(state, [])
@route
def inside_safe(state: State) -> Page:
    return Page(state, [])
@route
def open_book(state: State) -> Page:
    return Page(state, [])

#Routes w/o pages
@route 
def toggle_darkmode(state: State) ->Page:
    return index(state)
@route
def add_book(state: State) -> Page:
    return shelf(state)
@route 
def remove_book(state: State) -> Page:
    return shelf(state)
@route
def sort_books(state: State) -> Page:
    return shelf(state)
@route 
def input_attempt(state: State) -> Page:
    if state.safe_attempt.len() >= 3:
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
def remove_from_state(state: State) -> Page:
    return inside_safe(state)


assert_equal(index(State()), Page(State(), ["Hello World!"]))

start_server(State())
