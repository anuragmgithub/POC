# DOCKER CONCEPTS

## Docker Engine
Docker Engine is composed of two main components:
- **Docker Daemon (dockerd)**: Responsible for managing Docker containers on the host.
- **Docker Client**: Provides an interface to interact with the daemon, typically via CLI commands.

## Docker Images
Docker images are created from **Dockerfiles**, which are text files containing instructions to build the image layer by layer. Each layer in the Dockerfile corresponds to a step in the image build process.

## Docker Containers
Containers are runtime instances of Docker images. They are lightweight, isolated, and portable, making it easy to deploy applications consistently across environments.

## Docker Registry
The **Docker Registry** is a centralized repository for storing and sharing Docker images. The default public registry is [Docker Hub](https://hub.docker.com), where users can find a vast collection of images. Private registries can also be configured for internal use.

---

## Docker Compose
**Docker Compose** is a tool used to define and run multi-container Docker applications. It uses a `docker-compose.yml` file to configure services, networks, and volumes for your application.

### Differences Between Dockerfile and Docker Compose

- **Dockerfile**: Defines how to build a single container.
- **Docker Compose**: Defines how to run multiple containers together, including configurations and interactions between them.

### Key Advantages of Docker Compose

#### 1. Centralized Configuration
- **Dockerfile**: Focuses on one container at a time.
- **Docker Compose**: Centralizes configurations for multiple services, making it easier to manage complex environments.

#### 2. Networking and Links Simplified
- **Dockerfile**: Networking between containers must be manually set up.
- **Docker Compose**: Automatically sets up a network where services communicate by their names (e.g., a web service can connect to `db` without needing IP addresses).

#### 3. Automated Orchestration
- **Dockerfile**: You would need to manually run each container using commands like `docker run` or `docker network`.
- **Docker Compose**: Orchestrates the startup of all services, sets up networking, and handles dependencies between services with one command: `docker-compose up`.

#### 4. Multi-Stage Environment Support
- **Docker Compose**: Supports different profiles (e.g., development, testing, production) with minimal changes to the configuration file.

#### 5. Simplified Data Persistence
- **Docker Compose**: Easily defines shared volumes for data persistence across containers, simplifying what would otherwise require manual setup with `docker run` commands.

#### Example  
- **Problem Scenario: Using Only Dockerfile**   
You are working on a web application that requires three services:

- A frontend (React) container.
- A backend (Node.js/Express) container.
- A database (PostgreSQL) container.  

**When using only Dockerfiles,  would have to manually:**

- Create a Dockerfile for each service (frontend, backend, and database).
- Set up each container individually with docker run commands.
- Manually manage the networking between these containers (i.e., allowing frontend to talk to backend, and backend to talk to the database).
- Set up volumes for persisting database data.
- Handle dependencies, such as ensuring the database starts before the backend and that the backend starts before the frontend.

**Solution: Using Docker Compose**
Docker Compose solves all these problems by allowing you to define all your services in a single docker-compose.yml file. You can define the entire multi-container environment, including networking, volumes, and dependencies.

```
version: '3'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgres://user:password@db:5432/mydb
    depends_on:
      - db

  db:
    image: postgres:13
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb

volumes:
  db-data:
```

**How Docker Compose Solves the Problems:**

Simplified Startup: 
With Dockerfile: You needed to manually run each container and link them.  
With Docker Compose: You can start all services with a single command: docker-compose up. Compose takes care of the container lifecycle, bringing up the services in the correct order.  

Networking:  
With Dockerfile: Networking setup is manual, requiring network creation and IP configuration.  
With Docker Compose: Compose automatically creates a shared network where services can communicate by their service name (e.g., db for the database). No manual IP management needed

Data Persistence:  
With Dockerfile: You needed to manage data volumes for each container manually.   
With Docker Compose: You can define a shared volume (db-data) for PostgreSQL, and it’s automatically managed and mounted by Docker Compose.  

Dependency Management:  With Dockerfile: You needed to manage the startup order of containers manually, or the backend might fail to connect to the database if it starts too early.  

With Docker Compose: You can use depends_on to ensure that containers start in the correct order (e.g., the backend waits for the database to be ready).  


### Conclusion
Docker Compose provides a powerful way to manage multi-container applications, simplifying the orchestration, networking, and scaling of services compared to using Dockerfiles alone. It is especially useful in complex environments with multiple interacting services.

## Docker Volumes:
Docker volumes are used for persisting data generated by and used by Docker containers. They provide a way for containers to store and share data independently of the container lifecycle, ensuring data persistence and portability.  

## Docker Networking:
Docker provides networking capabilities for containers to communicate with each other and with external networks. It uses software-defined networks (SDN) to create virtual networks, enabling connectivity and isolation. Users can create custom networks, connect containers to networks, and define network policies using Docker commands or Docker Compose.  

---

## Docker Build context  
- The build context is essential for building Docker images because it determines which files are available to the Docker daemon.
- Proper management of the build context, including the use of a `.dockerignore file`, can greatly enhance performance and ensure that only necessary files are included in the image build process.  
**You can pass any of the following inputs as the context for a build:**
- The relative or absolute path to a local directory
- A remote URL of a Git repository, tarball, or plain-text file
- A plain-text file or tarball piped to the docker build command through standard input


When you run the docker build command, Docker takes the current directory (or the specified context) and sends all its contents to the Docker daemon. This directory structure and its files form the build context.

By controlling what files are included in the build context, you can optimize both build times and final image sizes. Using a .dockerignore file is essential for effective Docker image management, especially as projects grow in complexity.

**Best Practices**
- Use .dockerignore: Always create a .dockerignore file to exclude unnecessary files from the build context. This ensures that only relevant files are sent to the Docker daemon, speeding up the build process.
- Minimal Build Context: Keep your build context minimal. Only include files needed for building the image. If your application is complex, consider breaking it into smaller components with separate Dockerfiles.
- Review COPY Commands: Be explicit in your COPY commands to ensure you're only including the files necessary for the application to run

---
## Why Multi-Stage Builds?  
When you build an application, you often need additional tools and dependencies (like compilers, libraries, and debuggers) to compile the source code. However, once the application is built, these tools are no longer needed to run it. By using multi-stage builds, you can separate the build process from the runtime environment, resulting in smaller and more efficient Docker images.

---

## Build variables
Docker build variables allow you to make Dockerfiles more dynamic by passing values at build time.  
These values can be passed using build  
- arguments (ARG),
- environment variables (ENV),
- and also via runtime environment variables.  

**Using ARG to Pass Build-Time Variables**  

You can find the full Dockerfile example [here](Devops/Docker/CustomArgvarDockerfile).

**Combining ARG and ENV**  
Sometimes you want to pass build-time variables (ARG) and make them available as environment variables (ENV) within the container runtime.  
ARG values are only available <u>during the build process</u>, but you can forward them to the <u>final image using ENV</u>.  
- ARG is for the build process (compiling, installing specific versions, etc.).
- ENV is for configuring the application when it’s running, allowing you to customize the behavior of your containerized application at runtime without rebuilding the image.  

**Dynamic COPY Using Build-Time Variables**  
Copy environment-specific configuration files during the build.
```
# Base image
FROM node:14

# Define build-time argument for environment
ARG ENVIRONMENT=production

# Set environment variable
ENV ENVIRONMENT=${ENVIRONMENT}

# Copy environment-specific config
COPY config.${ENVIRONMENT}.json /app/config.json

# Install app dependencies
COPY package.json /app/
RUN npm install

# Set the default command
CMD ["npm", "start"]
```
*docker build -t my-app --build-arg ENVIRONMENT=development .*   
In this case: The COPY command dynamically copies either config.development.json or config.production.json based on the build-time argument.






