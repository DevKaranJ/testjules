FROM node:18-alpine

WORKDIR /app

# Copy package.json and install
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

# Copy source code
COPY frontend/ .

# Build Next.js application
RUN npm run build

# Expose port
EXPOSE 3000

CMD ["npm", "start"]
