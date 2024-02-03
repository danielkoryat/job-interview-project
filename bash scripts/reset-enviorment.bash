# Reset Environment Script

# Kafka: Delete 'event' Topic amd the '__consumer_offsets' Topic
docker exec -it main_project-kafka-1 kafka-topics --delete --topic event --bootstrap-server localhost:29092
docker exec -it main_project-kafka-1 kafka-topics --delete --topic __consumer_offsets --bootstrap-server localhost:29092

# MongoDB: Drop 'events' Collection from 'database1'
docker exec -it main_project-mongodb-1 mongosh -u superuser -p a12s34 --authenticationDatabase 'admin' --eval "db.getSiblingDB('database1').events.drop()"

# Redis: Clear All Data
docker exec -it main_project-redis-1 redis-cli FLUSHALL