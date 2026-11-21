from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import re
from datetime import datetime

app = FastAPI ()

# This dictionary will store book information using the ISBN as the key
book_cache = {}

# Defines response model
class Book (BaseModel):
    title: str 
    author: str
    publish_date: str
    isbn: str

class CachedBookResponse (BaseModel):
    cached: bool
    data: Book

# RegEx for ISBN-10 or ISBN-13 validation
ISBN_REGEX = r"^(?:\d{10}|\d{13})$"

def validate_isbn (isbn: str) -> bool:
    return bool (re.match (ISBN_REGEX, isbn))

def parse_date (date_str: str) -> str:
    try:
        # Try common date formats
        for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
            try:
                parsed_date = datetime.strptime (date_str, fmt)

                # Validate publication year
                year = parsed_date.year

                if not 1800 <= year <= datetime.now ().year:
                    raise HTTPException (
                        status_code = 400,
                        detail = "Publication year must be between 1800 and the current year."
                    )

                return parsed_date.strftime ("%Y-%m-%d")

            except ValueError:
                continue
                
        # Fallback to original if parsing fails
        return date_str 
    except Exception:
        return date_str

@app.get ("/book/{isbn}", response_model = CachedBookResponse)
async def get_book_by_isbn (isbn):
    # Validate ISBN
    if not validate_isbn (isbn):
        raise HTTPException (status_code = 400, detail = "Invalid ISBN format. Format must be 10 or 13 digits. ")

    if isbn in book_cache:
        return CachedBookResponse (
            cached = True,
            data = book_cache [isbn]
        )

    # Fetch from Open Library API
    try:
        url = f"http://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
        response = requests.get (url)
        response.raise_for_status ()
        data = response.json ()

        # Check if book data exists
        book_key = f"ISBN:{isbn}"
        if book_key not in data:
            raise HTTPException (status_code = 404, detail = "Book not found. ")

        book_data = data [book_key]
        title = book_data.get ("title", "Unknown")
        authors = book_data.get ("authors", [{"name": "Unknown"}]) [0] ["name"]
        publish_date = parse_date (book_data.get ("publish_date", "Unknown"))

        book = Book (
            title = title,
            author = authors,
            publish_date = publish_date,
            isbn = isbn
            )

        book_cache [isbn] = book

        return CachedBookResponse (cached = False, data = book)
    
    except requests.RequestException as e:
        raise HTTPException (status_code = 500, detail = f"Error fetching book data: {str (e)}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run (app, host = "0.0.0.0", port = 8000)