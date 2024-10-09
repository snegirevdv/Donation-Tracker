# Donation Tracker

**Version:** 0.1.0
**API Specification:** OpenAPI 3.1

**Donation Tracker** is a simple platform for managing charity and fundraising projects, along with donations.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Requirements](#requirements)
4. [API Documentation](#api-documentation)
5. [Example API Requests](#example-api-requests)

## Features:

- Manage charity projects
- Track donations
- User authentication with JWT
- Role-based access for users and administrators

## Installation

1. Clone the repository and navigate into the project directory:

   ```
   git clone https://github.com/snegirevdv/Donation-Tracker.git
   cd DonationTracker
   ```

2. Install dependencies and set up the environment:

   `make install`

3. Run the development server:

   `make run`

## Requirements

- Python 3.12+

## API Documentation

The full API documentation is available once the server is running.
Access the interactive docs (Swagger) at:

`http://127.0.0.1:8000/docs`

## Example API Requests

- **Get All Projects (for superuser)**:

  ```
  curl -X GET 'http://127.0.0.1:8000/projects/'
  -H 'Authorization: Bearer <your-token>'
  ```

- **Get your Donations**:

  ```
  curl -X GET 'http://127.0.0.1:8000/donations/my'
  -H 'Authorization: Bearer <your-token>'
  ```

- **Create a New Donation**:

  ```
  curl -X POST 'http://127.0.0.1:8000/donations/' 
  -H 'Authorization: Bearer <your-token>' 
  -H 'Content-Type: application/json' 
  -d '{\"full_amount": 100}'
  ```
