# Notification Service Backend

A FastAPI-based notification backend service using PostgreSQL as the database and RabbitMQ for message processing. This project provides a simple yet powerful system for managing and delivering notifications.

---

## Prerequisites

- Docker & Docker Compose
- Python 3.9+
- Git
- Postman (for testing the API)

---

## Setup Guide

**1. Clone the repository**
git clone https://github.com/Hurshikesh/pepsales.git


cd pepsales

**2. Create `.env` file**

Create a `.env` file in the project root with the following variables:

DATABASE_URL=postgresql://postgres:password@localhost:5432/notificationdb


RABBITMQ_URL=amqp://guest:guest@localhost/


SMTP_HOST=smtp.mailtrap.io


SMTP_PORT=2525


SMTP_USER=your_email@example.com


SMTP_PASSWORD=your_email_password


**3. Start PostgreSQL**

Launch PostgreSQL using Docker Compose:

docker-compose up -d


**4. Start RabbitMQ**

Launch RabbitMQ in a Docker container:

docker run -d --hostname my-rabbit --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management


The RabbitMQ management interface will be available at [http://localhost:15672/](http://localhost:15672/) (default credentials: guest/guest).

**5. Set up Python Environment**

Create and activate a virtual environment, then install dependencies:

python3 -m venv venv


source venv/bin/activate 


On Windows: venv\Scripts\activate


pip install -r requirements.txt



**6. Initialize Database**

Connect to the PostgreSQL container and create the necessary tables:

docker exec -it notification_postgres psql -U postgres -d notificationdb


Once connected to PostgreSQL, execute the following SQL commands:

CREATE TABLE users (
id SERIAL PRIMARY KEY,
email VARCHAR UNIQUE NOT NULL,
name VARCHAR NOT NULL
);


CREATE TABLE notifications (
id SERIAL PRIMARY KEY,
user_id INTEGER REFERENCES users(id),
type VARCHAR NOT NULL,
content VARCHAR NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO users (email, name) VALUES ('alice@example.com', 'Alice'), ('bob@example.com', 'Bob');


Type `\q` to exit the PostgreSQL prompt.

**7. Start the FastAPI Server**

Run the FastAPI application:

uvicorn app.main:app --reload --port 5000


The API will be available at: [http://localhost:5000](http://localhost:5000)

**8. Start the Notification Worker**

In a separate terminal, run the worker to process notifications:

PYTHONPATH=. python3 app/worker.py
---

## Testing the API

**Send a notification**

Using Postman or curl, send a POST request:

- **POST** `http://localhost:5000/notifications`

With the JSON body:

{
"user_id": 1,
"type": "welcome",
"content": "Welcome to our platform! 🎉"
}


**Get notifications for a user**

To fetch notifications for a specific user:

- **GET** `http://localhost:5000/notifications/1`

Replace `1` with the desired user ID.

---

## API Endpoints

| Method | Endpoint                       | Description                        |
|--------|-------------------------------|------------------------------------|
| POST   | /notifications                | Queue a new notification           |
| GET    | /notifications/{user_id}      | Get notifications for a specific user |

---

## Development

The application consists of:

- FastAPI web server handling API requests
- Worker processing notifications from RabbitMQ
- PostgreSQL database storing users and notifications
- RabbitMQ message broker for notification queuing

---

## Troubleshooting

- If you encounter connection issues with PostgreSQL, check if the container is running with `docker ps`
- For RabbitMQ issues, verify the service is running and the connection URL is correct
- Ensure all environment variables in the `.env` file are properly set

---

## License

MIT License
