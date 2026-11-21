# FastAPI Backend — Book Information API

A Python-based REST API that retrieves book information from the Open Library API using ISBN identifiers. The project includes a FastAPI backend, a Typer command-line client, input validation, HTTP Basic Authentication, and in-memory caching.

## Features

- **ISBN Lookup:** Retrieve a book's title, author, publication date, and ISBN.
- **ISBN Validation:** Accept 10- or 13-digit ISBN identifiers.
- **Publication Date Validation:** Validate publication years against a supported date range.
- **In-Memory Caching:** Store retrieved book information to reduce repeated external API requests.
- **Basic Authentication:** Protect the book lookup endpoint using HTTP Basic Authentication.
- **Command-Line Client:** Query the backend using Typer and display formatted JSON responses.
- **API Documentation:** Explore endpoints through FastAPI's automatically generated Swagger UI.

## Technology Stack

- Python
- FastAPI and Uvicorn
- Pydantic
- Typer
- Requests
- Open Library Books API
- Git and GitHub

## Project Structure

```text
FastAPI-Backend/
├── client/
│   └── client.py
├── server/
│   └── main.py
├── .gitignore
├── requirements.txt
├── README.md
└── FastAPI Backend.docx
```

## Getting Started

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

Start the FastAPI server:

```bash
cd server
python main.py
```

Access the interactive API documentation at:

`http://localhost:8000/docs`

In another terminal, navigate to the client directory and activate the virtual environment before running the client:

```bash
cd client
python3 client.py --help
```

## Example Request

Retrieve book information by ISBN:

```bash
python3 client.py 9780142437247 --username user --password pass
```

For local testing, the application uses demonstration credentials. Do not use hardcoded credentials in a production deployment.

## HTTP Status Codes

| Status | Description |
|---|---|
| 200 | Successful request |
| 400 | Invalid input |
| 401 | Unauthorized |
| 404 | Book not found |
| 500 | Internal server error |

## Documentation

See `FastAPI Backend.docx` for the project implementation report, testing evidence, and development documentation.

## Author

Brianna Willis  
Cybersecurity — Clark Atlanta University
