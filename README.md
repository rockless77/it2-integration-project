# Multi-Service FastAPI Integration Project

This project consists of three FastAPI services communicating with each other inside Docker:

Website-A → Integration Service → Website-B



Each website stores user data in its own PostgreSQL database:

Website-A → DB-A
Website-B → DB-B



The system demonstrates:

- API key validation
- Request forwarding
- Inter-service communication
- Independent data storage
- Fully containerized architecture

---

## 📂 Project Structure

it2/
│ docker-compose.yml
│ README.md
│
├── website-a/
│ ├── Dockerfile
│ ├── .env
│ └── app/
│ ├── main.py
│ └── requirements.txt
│
├── integration/
│ ├── Dockerfile
│ ├── .env
│ └── app/
│ ├── main.py
│ ├── validator.py
│ └── requirements.txt
│
└── website-b/
├── Dockerfile
├── .env
└── app/
├── main.py
├── models.py
└── requirements.txt



---

##  Running the System

### 1️⃣ Start all services

```bash
docker-compose up --build -d
2️⃣ Check status

docker-compose ps
Expected:

it2-website-a-1     Up      8001->8000
it2-integration-1   Up      8002->8000
it2-website-b-1     Up      8003->8000
it2-db-a-1          Up
it2-db-b-1          Up
All 5 services must be Up.

🔧 Environment Variables
Website-A (website-a/.env)

INTEGRATION_URL=http://integration:8000/api/send
INTEGRATION_API_KEY=a_to_integration_key
Integration Service (integration/.env)

INCOMING_API_KEY=a_to_integration_key
WEBSITE_B_URL=http://website-b:8000/api/receive
WEBSITE_B_API_KEY=b_secret_key
Website-B (website-b/.env)

DATABASE_URL=postgresql://b_user:b_pass@db-b:5432/b_db
📡 API Endpoints
Website-A → POST /api/send
Sends user data to the Integration Service.

Example:


curl -X POST http://localhost:8001/api/send \
  -H "Content-Type: application/json" \
  -H "api-key: a_to_integration_key" \
  -d '{"id":1,"name":"Alice","phone":"+123","joined_at":"2025-12-10"}'
Expected:


{
  "status": "OK",
  "forward_status": 200
}
Integration Service → POST /api/send
Validates API key and forwards payload to Website-B:


http://website-b:8000/api/receive
Website-B → POST /api/receive
Stores received user in DB-B.

Example:


curl -X POST http://localhost:8003/api/receive \
  -H "Content-Type: application/json" \
  -d '{"id":111,"name":"Test","phone":"+1","joined_at":"2025-12-10"}'
Response:


{ "status": "stored" }
 Full System Test
1️⃣ Send data to Website-A:

curl -X POST http://localhost:8001/api/send \
  -H "Content-Type: application/json" \
  -H "api-key: a_to_integration_key" \
  -d '{"id":42,"name":"Charlie","phone":"+447700900000","joined_at":"2025-12-10"}'
2️⃣ Expected flow
Step	Component	Action
1	Website-A	Accepts → validates → forwards
2	Integration	Validates → forwards to Website-B
3	Website-B	Stores to DB-B
4	Integration → Website-A	Returns success

Final expected output:


{
  "status": "OK",
  "forward_status": 200
}
 Docker Images Used
it2-website-a

it2-integration

it2-website-b

postgres:15 (two instances)

 Summary
This project successfully:

✔ Communicates between 3 microservices
✔ Validates API keys in 2 layers
✔ Stores data separately in DB-A and DB-B
✔ Uses Docker networking (website-a, integration, website-b)
✔ Deploys fully with one command