FROM node:20-alpine AS build
WORKDIR /app

# Required for esbuild on Alpine
RUN apk add --no-cache libc6-compat
RUN corepack enable

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .

# Allow overriding the API base at build time
ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN pnpm run build

FROM nginx:1.29.3-alpine
WORKDIR /usr/share/nginx/html
COPY --from=build /app/dist .
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
