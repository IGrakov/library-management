Library Management System
----
Backend - Django + DRF  
Frontend - Vue3 + Vite + TailwindCSS + PrimeVue

## To build the entire project
if you want to rebuild the image from scratch
```
docker compose -f docker-compose.dev.yml build --no-cache
```
or if you want to keep the cached layers
```
docker compose -f docker-compose.dev.yml build
```

## To build frontend only
if you want to rebuild the frontend image from scratch
```
docker compose -f docker-compose.dev.yml build frontend --no-cache
```
or if you want to keep the cached layers
```
docker compose -f docker-compose.dev.yml build frontend
```

## To build backend only
if you want to rebuild the backend image from scratch
```
docker compose -f docker-compose.dev.yml build backend --no-cache
```
or if you want to keep the cached layers
```
docker compose -f docker-compose.dev.yml build backend
```

## To start the project
```
docker compose -f docker-compose.dev.yml up
```

## To remove containers
```
docker compose -f docker-compose.dev.yml down
```

## To run any manage.py commands, e.g.  python manage.py createsuperuser
```
docker compose -f docker-compose.dev.yml exec backend poetry run python manage.py createsuperuser
```