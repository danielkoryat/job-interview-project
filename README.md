
# Microservices Event Processing System

## Overview

This project demonstrates a microservices architecture designed to process and transfer EVENT objects between services using Apache Kafka, MongoDB, and Redis. The system is orchestrated using Docker and Docker Compose, ensuring easy setup and scalability. The architecture includes:

- **Apache Kafka** for queuing messages.  

- **MongoDB** as a document database to store events.

- **Redis** for efficient key-value storage.

- **Docker** to containerize and manage the microservices.

## Prerequisites

- Docker and Docker Compose installed on your system.

- At least 8 GB of RAM for optimal performance. 

## Architecture

The project consists of several microservices:

1. **Kafka Producer** (`kafka-provider`): Generates EVENT objects and sends them to a Kafka topic.

2. **Kafka Consumer to MongoDB** (`kafka-consumer`): Consumes events from Kafka and inserts them into MongoDB. 

3. **MongoDB to Redis ETL** (`redis-provider`): Transfers data from MongoDB to Redis.

## Setup Instructions 

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Start Zookeeper:** 

   ```bash
   docker compose up zookeeper -d
   ```

3. **Start Kafka:**

   ```bash
   docker compose up kafka -d
   ```

4. **Create the Kafka topic** `event`:

   ```bash
   docker exec -it <kafka-container-name> kafka-topics --create --topic event --partitions 1 --replication-factor 1 --bootstrap-server localhost:29092
   ```

5. **Run the Kafka Producer:**

   ```bash
   docker compose up kafka-provider
   ```

6. **Listen to new messages on the** `event` **topic:**

   ```bash
   docker exec -it <kafka-container-name> kafka-console-consumer --bootstrap-server kafka:9092 --topic event
   ```

7. **Start MongoDB:**

   ```bash
   docker compose up mongodb -d
   ```

8. **Create a collection named** `events` **in MongoDB:**

   ```bash
   docker exec -it <mongodb-container-name> mongosh -u <username> -p <password> --authenticationDatabase 'admin' --eval "db.getSiblingDB('database1').createCollection('events')"
   ```

9. **Run the Kafka to MongoDB Consumer:**

   ```bash
   docker compose up kafka-consumer
   ```

10. **Query all documents in the** `events` **collection:**

    ```bash
    docker exec -it <mongodb-container-name> mongosh -u <username> -p <password> --authenticationDatabase 'admin' --eval "const eventsCollection = db.getSiblingDB('database1').events; eventsCollection.find().forEach(doc => print(JSON.stringify(doc, null, 2))); print('Total documents in events collection:', eventsCollection.countDocuments({}));"
    ```

11. **Start Redis:**

    ```bash 
    docker compose up redis -d
    ```

12. **Run the Redis Provider (ETL from MongoDB to Redis):**

    ```bash
    docker compose up redis-provider
    ```

13. **Get all keys in Redis:**

    ```bash
    docker exec -it <redis-container-name> redis-cli KEYS '*' 
    ```

14. **Repeat steps 9 and 12 as needed to process additional data.**

## Additional Notes

- Ensure all environment variables are set correctly in the `docker-compose.yml` file.

- Use `docker container ls` to find container names for executing commands.

- Adjust the MongoDB and Redis connection details according to your setup.

