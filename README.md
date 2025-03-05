# HaHaHub - A Flask-Based Joke Sharing Platform

HaHaHub is a web application that allows users to submit, view, and vote on jokes. It features user authentication, an admin dashboard, and an API for joke retrieval and voting. The application is currently hosted at [bhavya31.pythonanywhere.com](https://bhavya31.pythonanywhere.com).

## Features

- **User Authentication**: Users can register, log in, and submit their own jokes.
- **Joke Voting**: Users can upvote or downvote jokes.
- **Admin Dashboard**: Admins can manage jokes, view statistics, and delete or edit jokes..
- **Password Management**: Users can change their passwords securely.
- **REST API Support**: Provides endpoints for retrieving and voting on jokes.

## Installation

### Prerequisites

- Python 3.x
- Flask
- SQLite (bundled with Python)

### Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/HaHaHub.git
   cd HaHaHub
   ```

2. Create a virtual environment and install dependencies:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   
   ```

3. Set up the database:
   ```sh
   python setup_db.py
   ```

4. Run the application:
   ```sh
   python app.py
   ```
   The app will be available at `http://127.0.0.1:5080/`.

## API Usage

### 1. Get a Random Joke
**Endpoint:** `/api/joke`  
**Method:** `GET`  
**Response:**
```json
{
    "id": 1,
    "joke": "Why don’t skeletons fight each other? They don’t have the guts."
}
```

### 2. Vote on a Joke
**Endpoint:** `/api/vote/<direction>/<int:joke_id>`  
**Method:** `POST`  
**Parameters:**
- `direction`: "up" for upvote, "down" for downvote.
- `joke_id`: The ID of the joke.

**Response:**
```json
{
    "status": "success",
    "id": 2,
    "joke": "Another joke after voting"
}
```

### 3. Register a New User
**Endpoint:** `/register`  
**Method:** `POST`  
**Request Body:**
```json
{
    "username": "newuser",
    "password": "password123"
}
```
**Response:**
```json
{
    "status": "success"
}
```

### 4. Login User
**Endpoint:** `/login`  
**Method:** `POST`  
**Request Body:**
```json
{
    "username": "newuser",
    "password": "password123"
}
```
**Response:**
```json
{
    "status": "success"
}
```

### 5. Submit a Joke
**Endpoint:** `/submit_joke`  
**Method:** `POST`  
**Request Body:**
```json
{
    "joke": "Why did the chicken cross the road? To get to the other side!"
}
```
**Response:**
```json
{
    "status": "success"
}
```

### 6. Get User Dashboard Jokes
**Endpoint:** `/user`  
**Method:** `GET`  
**Response:**
```json
{
    "jokes": [
        "Joke 1",
        "Joke 2"
    ]
}
```

### 7. Admin Dashboard
**Endpoint:** `/admin`  
**Method:** `GET`  
**Response:**
```json
{
    "total_jokes": 100,
    "top_jokes": [
        {
            "id": 1,
            "joke": "Top voted joke"
        }
    ]
}
```

### 8. Edit a Joke (Admin Only)
**Endpoint:** `/admin/edit/<int:joke_id>`  
**Method:** `POST`  
**Request Body:**
```json
{
    "joke_text": "Updated joke content."
}
```
**Response:**
```json
{
    "status": "success"
}
```

### 9. Delete a Joke (Admin Only)
**Endpoint:** `/admin/delete/<int:joke_id>`  
**Method:** `POST`  
**Response:**
```json
{
    "status": "success"
}
```

### 10. Change Password
**Endpoint:** `/change_password`  
**Method:** `POST`  
**Request Body:**
```json
{
    "old_password": "currentpassword",
    "new_password": "newpassword123",
    "confirm_password": "newpassword123"
}
```
**Response:**
```json
{
    "status": "success"
}
```

## Deployment

The application is deployed on [PythonAnywhere](https://bhavya31.pythonanywhere.com/). To deploy:

1. Upload your project files.
2. Set up a virtual environment and install dependencies.
3. Configure the WSGI file to point to your Flask app.
4. Restart the web app from the PythonAnywhere dashboard.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make changes and commit (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License.

---

Enjoy sharing and laughing with HaHaHub! 🎉

