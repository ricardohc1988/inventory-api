# Inventory API

## Overview
inventory-api is a RESTful API built using Django and Django Rest Framework, designed to manage categories, products, and stock movements within an inventory system. It provides endpoints for managing product categories, adding and updating products, and tracking stock movements (both incoming and outgoing) in real-time.

This project includes validation to ensure data consistency and security, and restricts certain actions to staff members only.

## Features
- **Categories**: Create, retrieve, update, and delete categories for organizing products.
- **Products**: Manage products with name, description, price, category, and stock quantity.
- **Stock Movements**: Track incoming and outgoing stock movements, updating product stock accordingly.
- **Permissions**: Only staff members can create, update, or delete categories, products, and stock movements.
- **Validation**: Ensures that products and stock movements adhere to business rules (e.g., non-negative stock quantities, valid movement types).

## Setup

### Requirements
- Python 3.9+
- Django 3.2+
- Django Rest Framework
- SQLite (or any other preferred database)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/inventory-api.git
   cd inventory-api

2. Install dependencies
   ```bash
   pipenv install

3. Apply migrations
    ```bash
    pipenv run python manage.py migrate

4. Create a superuser
    ```bash
    pipenv run python manage.py createsuperuser

5. Run the development server
    ```bash
    pipenv run python manage.py runserver

## Usage

### API Endpoints

*Categories*
- **GET /categories/**  - List all categories
- **POST /categories/** - Create a new category
- **GET /categories/{id}/** - Retrieve a specific category
- **PUT /categories/{id}/** - Update a category
- **DELETE /categories/{id}/** - Delete a category
Products

*Products*
- **GET /products/** - List all products
- **POST /products/** - Create a new product
- **GET /products/{id}/** - Retrieve a specific product
- **PUT /products/{id}/** - Update a product
- **DELETE /products/{id}/** - Delete a product
Stock Movements

*Stock movements*
- **GET /stock_movements/** - List all stock movements
- **POST /stock_movements/** - Create a new stock movement
- **GET /stock_movements/{id}/** - Retrieve a specific stock movement
- **PUT /stock_movements/{id}/** - Update a stock movement
- **DELETE /stock_movements/{id}/** - Delete a stock movement

## Permissions
All API views require authentication via TokenAuthentication.
Only staff users have permission to create, update, or delete categories, products, and stock movements.