# FastAPI Authentication Service

A authentication service built with FastAPI and MongoDB.

## Features

- User Registration
- User Login with JWT Authentication
- Access and Refresh Tokens
- HTTP-only Cookie Support
- MongoDB Integration
- Docker Support
- Kubernetes Deployment

## Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)
- Kubernetes cluster (for production deployment)
- kubectl CLI tool

## Setup and Running

### Using Docker Compose (Development)

1. Clone the repository:
```
git clone <repository-url>
cd <repository-name>
```

2. Start the services:
```
docker-compose up --build
```

The API will be available at `http://localhost:8001`

### Local Development

1. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate 

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Start MongoDB (make sure it's installed and running)

4. Create a `.env` file with the following content:
```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=auth_db
ACCESS_TOKEN_EXPIRE_MINUTES=1
REFRESH_TOKEN_EXPIRE_DAYS=7
SECRET_KEY=your-secret-key-for-jwt
ALGORITHM=HS256
PORT=8001
```

5. Run the application:
```
python -m uvicorn app.main:app 
```

### Kubernetes Deployment (Production)

1. Build and tag the Docker image:
```
docker build -t auth-api:latest .
```

2. Apply the Kubernetes manifests:
```
kubectl apply -f k8s/mongodb.yaml
kubectl apply -f k8s/api.yaml
kubectl apply -f k8s/nginx.yaml
```

3. Wait for all pods to be ready:
```
kubectl get pods -w
```

4. Get the external IP of the Nginx service:
```
kubectl get service nginx
```

The API will be available at the external IP address of the Nginx service.

## API Endpoints

### 1. Register User
- **URL**: `/auth/register`
- **Method**: `POST`
- **Body**:
```json
{
    "email": "user@example.com",
    "password": "strongpassword",
    "full_name": "John Doe"
}
```

### 2. Login
- **URL**: `/auth/login`
- **Method**: `POST`
- **Body**:
```json
{
    "email": "user@example.com",
    "password": "strongpassword"
}
```

### 3. Get User Details
- **URL**: `/auth/me`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <access_token>`

## Security Features

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- HTTP-only cookies for token storage
- Access token expires in 1 minute
- Refresh token expires in 1 week

## Kubernetes Architecture

The application is deployed with the following components:

1. MongoDB Deployment
   - Single instance with persistent storage
   - Internal ClusterIP service
   - Not exposed to public network

2. Backend API Deployment
   - 3 replicas for high availability
   - Internal ClusterIP service
   - Communicates with MongoDB service

3. Nginx Deployment
   - Load balancer for API requests
   - Exposed to public network
   - Ingress configuration for routing

## Project Structure

```
.
├── app/
│   ├── api/
│   │   └── auth.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   └── user.py
│   ├── schemas/
│   │   └── auth.py
│   ├── services/
│   │   ├── auth.py
│   │   └── user.py
│   └── main.py
├── k8s/
│   ├── mongodb.yaml
│   ├── api.yaml
│   └── nginx.yaml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
``` 
