FROM node:23-slim

# Install pnpm globally
RUN npm install -g pnpm

WORKDIR /app

# Copy package.json and pnpm-lock.yaml
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy project files
COPY . .

# Change ownership to the existing node user
RUN chown -R node:node /app
USER node

# Expose dev server port
EXPOSE 5173

# Start Vue 3 dev server
CMD ["pnpm", "run", "dev", "--host", "0.0.0.0"]