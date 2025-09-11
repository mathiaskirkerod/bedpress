# Use the official Node.js image from the Docker Hub
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# Build the React app
RUN npm run build

# Install serve globally for production serving
RUN npm install -g serve

# Expose the port that the app runs on
EXPOSE 3000

# Command to serve the built application
CMD ["serve", "-s", "build", "-l", "3000"]