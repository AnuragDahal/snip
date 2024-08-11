# URL Shortener 

This project is a URL shortener API built using FastAPI. It provides endpoints to shorten long URLs and redirect short URLs to their original long URLs.

## Endpoints

### Shorten URL

- **Endpoint:** `/shorten`
- **Method:** `POST`
- **Description:** Shortens a long URL to a short URL.
- **Request Parameters:**
  - `long_url` (query parameter): The long URL to be shortened.
- **Response:**
  ```json
  {
    "short_url": "http://localhost:8000/shortened_string"
  }
  ```
