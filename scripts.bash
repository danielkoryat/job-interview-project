#Change Execution Policy for the Current Session to enable virtual environment
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

#creates a new topic in the kafka cluster main_project-kafka-1: name of te container  event: name of the topic 
docker exec -it main_project-kafka-1 kafka-topics --create --topic event --partitions 1 --replication-factor 1 --bootstrap-server localhost:29092

#list all the topics in the kafka cluster
docker exec -it main_project-kafka-1 kafka-topics --list --bootstrap-server localhost:29092

#start the docker compose
docker-compose up -d

#see the events in the kafka cluster main_project-kafka-1 event topic
docker exec -it main_project-kafka-1 kafka-console-consumer --bootstrap-server kafka:9092 --topic event --from-beginning

#delete the topic
docker exec -it main_project-kafka-1 kafka-topics --delete --topic event --bootstrap-server localhost:29092


