# DoubleSide - Smart PDF Tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

DoubleSide is a modern, web-based tool for preparing PDFs for printing. It offers features like double-sided printing preparation, booklet creation, and N-up layouts, all with a beautiful glassmorphism UI.

## Features

-   **Double-Sided Printing**: Splits pages into "Front" and "Back" sets for easy manual double-sided printing on single-sided printers.
-   **2-in-1 (N-up)**: Places two pages side-by-side on a single landscape sheet (A4).
-   **Booklet Mode**: Arranges pages so they can be folded into a booklet.
-   **Split**: Extracts a range of pages.
-   **Decrypt**: Removes passwords from PDFs (if the password is empty or standard).
-   **Secure**: Files are processed locally/temporarily and automatically deleted after 1 hour.

## Tech Stack

-   **Frontend**: React (Vite), Tailwind CSS v4
-   **Backend**: Python (FastAPI), PyMuPDF (fitz)
-   **Deployment**: Docker, Docker Compose

## Getting Started

### Prerequisites

-   Docker and Docker Compose installed.

### Running with Docker (Recommended)

1.  Clone the repository.
2.  Run the following command in the project root:

    ```bash
    docker-compose up --build -d
    ```

3.  Open your browser and navigate to `http://localhost`.

### Running Locally (Development)

#### Backend

1.  Navigate to `backend`:
    ```bash
    cd backend
    ```
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    # source venv/bin/activate # Linux/Mac
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the server:
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

#### Frontend

1.  Navigate to `frontend`:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```
    The UI will be available at `http://localhost:5173` (or similar).

## API Documentation

Once the backend is running, you can access the interactive API documentation at:
`http://localhost:8000/docs`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
