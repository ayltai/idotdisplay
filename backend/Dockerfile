FROM node:24-trixie-slim AS build
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
WORKDIR /app/frontend
COPY frontend/ .
RUN pnpm i --force
RUN pnpm build

FROM python:3.13-slim-trixie
RUN apt update && apt --no-install-recommends install -y bluez libglib2.0-0 && apt clean autoclean && apt autoremove -y && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY backend/ ./
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt
COPY --from=build /app/frontend/dist ./web
EXPOSE 18000
CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--port=18000"]
