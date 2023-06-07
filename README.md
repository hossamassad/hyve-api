#  API

This code represents a simple API for managing users, products, and their relationships. It's built using the Flask framework, with SQLAlchemy as an ORM for interacting with the PostgreSQL database.

## Setup

Before running the API, you need to make sure that you have PostgreSQL installed on your machine and create a database named "hyve". You can change the database URL in the `app.config` section of the code to match your PostgreSQL setup.

In order to run the API, you need to install the required dependencies first. You can do this by running:

```
pip install -r requirements.txt
```

After installing the dependencies, you can start the API by running:

```
python app.py
```

This will start the Flask development server and make the API available at `http://localhost:5000`.

## API Endpoints

### Users

- `GET /users`: Returns a paginated list of all users. You can specify the page number and the number of items per page by using the `page` and `per_page` query parameters.
- `GET /users/<int:user_id>`: Returns the details of a single user based on their ID.
- `POST /users`: Adds a new user to the database. The request body should be a JSON object containing the `name` and `email` of the user.
- `PUT /users/<int:user_id>`: Updates the details of an existing user based on their ID. The request body should be a JSON object containing the fields that you want to update (`name`, `email`, or both).
- `DELETE /users/<int:user_id>`: Deletes an existing user based on their ID.

### Products

- `GET /products`: Returns a paginated list of all products. You can specify the page number and the number of items per page by using the `page` and `per_page` query parameters.
- `GET /products/<int:product_id>`: Returns the details of a single product based on its ID.
- `POST /products`: Adds a new product to the database. The request body should be a JSON object containing the `name` and `price` of the product.
- `PUT /products/<int:product_id>`: Updates the details of an existing product based on its ID. The request body should be a JSON object containing the fields that you want to update (`name`, `price`, or both).
- `DELETE /products/<int:product_id>`: Deletes an existing product based on its ID.

### User Products

- `GET /users/<int:user_id>/products`: Returns a list of all products associated with a specific user based on their ID.
- `POST /users/<int:user_id>/products`: Associates a product with a user based on their IDs. The request body should be a JSON object containing the `product_id` of the product that you want to associate with the user.
- `DELETE /users/<int:user_id>/products/<int:product_id>`: Removes the association between a product and a user based on their IDs.

## Testing with Postman

You can use Postman to test the API endpoints. Here are the steps for testing the `GET /users` endpoint:

1. Open Postman and create a new request by clicking on the "New Request" button.
2. Enter a name for the request (e.g. "Get All Users") and select the HTTP method "GET".
3. Enter the URL `http://localhost:5000/users` in the address bar.
4. Click on the "Send" button to send the request.
5. Postman should display the response from the API in the "Body" section of the window. If everything is working correctly, you should see a JSON array containing the details of the users in the database.

You can test the other endpoints in a similar way. Just make sure to use the correct HTTP method and URL for each endpoint. You can also pass any required parameters or request body in the appropriate sections of the request in Postman.
And here are the Postman snippets for each endpoint:

### GET /users

```
GET /users HTTP/1.1
Host: localhost:5000
```

### GET /users/<int:user_id>

```
GET /users/<user_id> HTTP/1.1
Host: localhost:5000
```
Make sure to replace `<user_id>` with the actual ID of the user you want to retrieve.

### POST /users

```
POST /users HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
    "name": "John Doe",
    "email": "johndoe@example.com"
}
```

### PUT /users/<int:user_id>

```
PUT /users/<user_id> HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
    "name": "Jane Doe",
    "email": "janedoe@example.com"
}
```
Make sure to replace `<user_id>` with the actual ID of the user you want to update.

### DELETE /users/<int:user_id>

```
DELETE /users/<user_id> HTTP/1.1
Host: localhost:5000
```
Make sure to replace `<user_id>` with the actual ID of the user you want to delete.

### GET /products

```
GET /products HTTP/1.1
Host: localhost:5000
```

### GET /products/<int:product_id>

```
GET /products/<product_id> HTTP/1.1
Host: localhost:5000
```
Make sure to replace `<product_id>` with the actual ID of the product you want to retrieve.

### POST /products

```
POST /products HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
    "name": "Product X",
    "price": 10.99
}
```

### PUT /products/<int:product_id>

```
PUT /products/<product_id> HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
    "name": "Product Y",
    "price": 19.99
}
```
Make sure to replace `<product_id>` with the actual ID of the product you want to update.

### DELETE /products/<int:product_id>

```
DELETE /products/<product_id> HTTP/1.1
Host: localhost:5000
```
Make sure to replace `<product_id>` with the actual ID of the product you want to delete.

### GET /users/<int:user_id>/products

```
GET /users/<user_id>/products HTTP/1.1
Host: localhost:5000
```
Make sure to replace `<user_id>` with the actual ID of the user for whom you want to retrieve the associated products.

### POST /users/<int:user_id>/products

```
POST /users/<user_id>/products HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
    "product_id": <product_id>
}
```
Make sure to replace `<user_id>` with the actual ID of the user to whom you want to associate the product, and `<product_id>` with the actual ID of the product you want to associate.

### DELETE /users/<int:user_id>/products/<int:product_id>

```
DELETE /users/<user_id>/products/<product_id> HTTP/1.1
Host: localhost:5000
```
Make sure to replace `<user_id>` with the actual ID of the user from whom you want to remove the association, and `<product_id>` with the actual ID of the product you want to remove the association for.
