# Inventory Management System - Flask REST API

This project is a simple **Inventory Management System** built with **Flask**. It allows administrators to perform CRUD operations on inventory items and integrates with an external API (OpenFoodFacts) to fetch product details.

## Features

- **CRUD Operations:** Create, Read, Update, Delete inventory items.
- **External API Integration:** Search and add products from OpenFoodFacts.
- **CLI Interface:** Interactive command-line interface to manage inventory.
- **Modular Design:** Business logic encapsulated in `service.py`.
- **Unit Testing:** Ensures all routes and operations function correctly.

## Project Structure

```
inventory-api/
│── main.py          # Flask API routes
│── service.py       # Business logic + encapsulation
│── cli.py           # Command-line interface
│── test_app.py      # Unit tests for API
│── requirements.txt # Dependencies
│── README.md        # Project documentation
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/madoyakimberley/-inventory-api.git
cd -inventory-api
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### 1. Run the Flask API

```bash
python main.py
```

- The API will run on `http://127.0.0.1:5000`

### 2. Run the CLI Interface

```bash
python cli.py
```

- Use the menu to **view, add, delete, update items** or **search products** from the external API.

### 3. Run Unit Tests

```bash
python -m unittest test_app.py
```

- Ensures all API endpoints are working as expected.

## API Endpoints

- `GET /items` – Retrieve all inventory items.
- `POST /items` – Add a new item.
- `PATCH /items/<id>` – Update an existing item.
- `DELETE /items/<id>` – Delete an item.
- `GET /external/<query>` – Fetch product details from OpenFoodFacts.
- `GET /health` – Check API status.
