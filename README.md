# Humanitarian Aid Management System
### Advanced Software Engineering — SDEV 4304 | IUG 2025/2026
**Student:** Batool Albreem | 220197079 | **Supervisor:** Dr. Abdelkareem Alashqar

---

## About
A microservices-based platform built with **Django + Docker** to manage and distribute humanitarian aid efficiently.

## Services

| Service | Port | Description |
|---|---|---|
| User Service | 8001 | Identity management — register, login, profiles |
| Aid Request Service | 8002 | Submit and track aid requests |
| Donation Service | 8003 | Manage donations and fund allocation |
| Distribution Service | 8004 | Schedule and track deliveries |
| Notification Service | 8005 | Send notifications via events |

## Quick Start

```bash
git clone https://github.com/[your-username]/humanitarian-aid-system
cd humanitarian-aid-system
docker compose up --build
```

All 5 services + 5 PostgreSQL databases + RabbitMQ start automatically.

## API Endpoints

| Method | URL | Description |
|---|---|---|
| POST | localhost:8001/api/users/register/ | Register user |
| POST | localhost:8002/api/aid-requests/ | Submit aid request |
| POST | localhost:8003/api/donations/ | Create donation |
| POST | localhost:8004/api/distributions/ | Schedule distribution |

## Architecture
- **Pattern:** Microservices (Newman, Building Microservices 2nd Ed.)
- **Communication:** Sync REST (DRF) + Async Events (RabbitMQ)
- **Database:** PostgreSQL — one per service (no shared DB)
- **Deployment:** Docker + Docker Compose
- **CI/CD:** GitHub Actions → Docker Hub
