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

assert_equal(index(State()), Page(State(), ["Hello World!"]))

start_server(State())
