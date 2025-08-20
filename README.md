# Library

A command-line application for managing a personal library of books and tracking who has borrowed them.

## Features

* **Robust Data Persistence**: All book information is now stored in a lightweight and reliable **SQLite database file**, making data management more robust than simple JSON files.
* **Layered Architecture**: The application is built with a clear separation of concerns:
    * **CLI Layer** (Interface): Handles user commands and arguments.
    * **Services Layer** (Business Logic): Manages the core logic, like adding a new book.
    * **Data Layer** (Persistence): Abstracts the interaction with the database.
* **Command-Line Interface (CLI)**: Interact with the application using a command-based system (e.g., `library add ...`, `library list`).
* **Unit Tests**: Includes a dedicated test suite using **Pytest** to ensure key functionalities work as expected and prevent regressions.

## Project Structure

The project is organized to promote a clean and scalable design.

```
/library/
├── .gitignore
├── README.md
├── LICENSE.md
├── pyproject.toml
├── my_books/
│   ├── init.py
│   ├── cli.py
│   ├── services/
│   │   ├── init.py
│   │   └── book_service.py
│   ├── data/
│   │   ├── init.py
│   │   └── book_repository.py
│   └── models/
│       ├── init.py
│       └── book.py
└── tests/
└── test_book_repository.py
```

* `my_books/`: The main Python package containing the application logic.
* `my_books/models/`: Defines the data structures (`Book`).
* `my_books/data/`: Handles data storage and retrieval via the SQLite database.
* `my_books/services/`: Contains the core business logic.
* `my_books/cli.py`: The command-line interface powered by **Typer**.
* `tests/`: Stores unit tests to verify the application's functionality using **Pytest**.

## How to Get Started

### 1. Installation

Clone the repository and install the project in "editable" mode. This allows you to run the `library` command directly from your terminal.

```bash
cd your-repo-name
pip install -e .
```