# Portofolio

Django portfolio application with PostgreSQL and Docker support.

---

## Deployment

### 1. Pull the Image

Images are published to `ghcr.io/<owner>/portofolio` on `release-*` tags.

```bash
# Authenticate (PAT with read:packages scope)
echo $GHCR_PAT | docker login ghcr.io -u <your-username> --password-stdin

# Pull
docker pull ghcr.io/<owner>/portofolio:release-v1.0.0
```

### 2. Run with Docker

```bash
docker run -d \
  --name portofolio \
  -p 8000:8000 \
  -e DB_HOST=your-db-host \
  -e DB_NAME=portofolio \
  -e DB_USER=your-db-user \
  -e DB_PASSWORD=your-db-password \
  -e SECRET_KEY=your-secret-key \
  -e ALLOWED_HOSTS=your-domain.com \
  ghcr.io/<owner>/portofolio:release-v1.0.0
```

### 3. Run with Docker Compose

```yaml
# docker-compose.yml
services:
  app:
    image: ghcr.io/<owner>/portofolio:release-v1.0.0
    ports:
      - "8000:8000"
    environment:
      DB_HOST: db
      DB_NAME: portofolio
      DB_USER: postgres
      DB_PASSWORD: ${DB_PASSWORD}
      SECRET_KEY: ${SECRET_KEY}
      ALLOWED_HOSTS: ${ALLOWED_HOSTS}
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:17-alpine
    environment:
      POSTGRES_DB: portofolio
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

```bash
docker compose up -d
```

### 4. GitHub Actions (CI/CD deploy)

The `GITHUB_TOKEN` has automatic package read access within the same org/repo:

```yaml
- name: Deploy
  run: |
    echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u ${{ github.actor }} --password-stdin
    docker pull ghcr.io/${{ github.repository }}:release-v1.0.0
    # ... deploy steps
```

---

## CI/CD — Release Tags

Push a tag to trigger the build:

```bash
git tag release-v1.0.0
git push origin release-v1.0.0
```

The workflow `.github/workflows/docker-release.yml` builds and pushes to GHCR automatically.
