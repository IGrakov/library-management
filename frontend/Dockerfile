FROM node:24-alpine AS dev

# Enable pnpm via corepack
RUN corepack enable

WORKDIR /app

# Copy package.json and pnpm-lock.yaml
COPY package.json pnpm-lock.yaml ./

RUN echo -e "allowBuilds:\n  vue-demi: true" > pnpm-workspace.yaml

RUN corepack enable \
 && pnpm install --frozen-lockfile

# Copy project files
COPY . .

# Expose dev server port
EXPOSE 5173

# Start Vue 3 dev server
CMD ["pnpm", "run", "dev", "--host", "0.0.0.0"]