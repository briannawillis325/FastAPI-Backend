import typer
import requests
import json

app = typer.Typer ()
BASE_URL = "http://localhost:8000"

def print_response (response):
    try:
        print (f"Status Code: {response.status_code}")
        # Converts a Python object into a JSON string
        print (json.dumps (response.json (), indent = 2))
    except ValueError:
        print (f"Status Code: {response.status_code}")
        print (response.text)

@app.command ()
def get_book (isbn: str, min_year: int = typer.Option (None, "--min-year")):
    """Fetch book details by ISBN."""
    try:
        response = requests.get (f"{BASE_URL}/book/{isbn}")

        if response.status_code == 200 and min_year is not None:
            result = response.json ()
            book = result.get ("data", result)

            if int (book ["publish_date"]) < min_year:
                typer.echo (f"Book published before {min_year}.")
                return

        print_response (response)
    except requests.RequestException as e:
        typer.echo (f"Error: Failed to connect to server - {str (e)}")

if __name__ == '__main__':
    app ()