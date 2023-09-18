# Banky

![Flask](https://img.shields.io/badge/Flask-Web%20Framework-brightgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL-blue)
![JWT](https://img.shields.io/badge/JWT-Authentication-yellow)
![CRUD](https://img.shields.io/badge/CRUD%20Operations-green)

Banky is a Python-based Banking API built using Flask, SQL, and PostgreSQL. It offers various banking functionalities, including JWT authentication, account creation, deposits, withdrawals, transfers, and statements. All sensitive user data is securely encrypted to ensure data protection.

## Features

- **JWT Authentication**: Secure authentication using JSON Web Tokens for protected routes.
- **Account Creation**: Users can create new accounts with a unique account number, name, last name, and password.
- **Deposits**: Users can deposit money into their accounts with ease.
- **Withdrawals**: Easy withdrawal of funds from user accounts.
- **Transfers**: Securely transfer funds between accounts, including sender and receiver account validation.
- **Account Statements**: Retrieve account statements to view transaction history.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/banky.git
cd banky
```

2. Set up your PostgreSQL database and update the database connection details in the `db_connect` function.
3. Run the application:

```bash
python app.py
```

## Usage

### Authentication

To access protected routes, you need to authenticate using JWT (JSON Web Tokens). Follow these steps:
1. **Register a User**: Send a POST request to `/account` with a JSON payload containing `name`, `last_name`, `password`, and a unique `account_number`.
2. **Login**: Send a GET request to `/login` with Basic Authentication (username: `account_number`, password: `password`). You will receive a JWT token in response.
3. **Use the JWT Token**: Include the JWT token in the `x-access-token` header when making requests to protected routes, such as `/accounts`, `/deposits`, `/withdraws`, `/transfers`, and `/statement`.

### Account Operations
- **Create an Account**: Send a POST request to `/account` with a JSON payload containing `name`, `last_name`, `password`, and a unique `account_number` to create a new account.
- **Read an Account**: Send a GET request to `/account/<account_number>` to retrieve account details by account number.
- **Update an Account**: Send a PUT request to `/account/<account_number>` with a JSON payload containing `name` and/or `last_name` to update account details.
- **Delete an Account**: Send a DELETE request to `/account/<account_number>` to delete an account.
- **Get All Accounts**: Send a GET request to `/accounts` to retrieve a list of all accounts. You can specify the `limit` and `offset` as query parameters for pagination.

### Deposit Operations

- **Create a Deposit**: Send a POST request to `/deposit` with a JSON payload containing `account_number` and `amount` to make a deposit.
- **Read a Deposit**: Send a GET request to `/deposit/<deposit_id>` to retrieve deposit details by deposit ID.
- **Get All Deposits**: Send a GET request to `/deposits/<account_number>` to retrieve a list of all deposits for a specific account. You can specify the `limit` and `offset` as query parameters for pagination.

### Withdrawal Operations

- **Create a Withdrawal**: Send a POST request to `/withdraw` with a JSON payload containing `account_number` and `amount` to make a withdrawal.
- **Read a Withdrawal**: Send a GET request to `/withdraw/<withdraw_id>` to retrieve withdrawal details by withdrawal ID.
- **Get All Withdrawals**: Send a GET request to `/withdraws/<account_number>` to retrieve a list of all withdrawals for a specific account. You can specify the `limit` and `offset` as query parameters for pagination.

### Transfer Operations

- **Create a Transfer**: Send a POST request to `/transfer` with a JSON payload containing `sender_account_number`, `receiver_account_number`, and `amount` to make a transfer.
- **Read a Transfer**: Send a GET request to `/transfer/<transfer_id>` to retrieve transfer details by transfer ID.
- **Get All Transfers**: Send a GET request to `/transfers/<account_number>` to retrieve a list of all transfers for a specific account. You can specify the `limit` and `offset` as query parameters for pagination.

### Statement Operations

- **Get Account Statement**: Send a GET request to `/statement` to retrieve a statement of account transactions. You can specify the `limit` and `offset` as query parameters for pagination.
