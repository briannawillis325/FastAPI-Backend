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
def get_book (isbn: str):
    """Fetch book details by ISBN."""
    try:
        response = requests.get (f"{BASE_URL}/book/{isbn}")
        print_response (response)
    except requests.RequestException as e:
        typer.echo (f"Error: Failed to connect to server - {str (e)}")

if __name__ == '__main__':
    app ()