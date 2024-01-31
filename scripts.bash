##env

#Change Execution Policy for the Current Session to enable virtual environment
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
##############################################################################################################################

##docker
#start the docker compose
docker-compose up -d

#start a spesific container
docker start container-name

#stop the docker compose
docker-compose down
##############################################################################################################################
##kafka

#creates a new topic in the kafka cluster main_project-kafka-1: name of the container  event: name of the topic 
docker exec -it main_project-kafka-1 kafka-topics --create --topic event --partitions 1 --replication-factor 1 --bootstrap-server localhost:29092

#list all the topics in the kafka cluster
docker exec -it main_project-kafka-1 kafka-topics --list --bootstrap-server localhost:29092


#see the events in the kafka cluster main_project-kafka-1 event topic
docker exec -it main_project-kafka-1 kafka-console-consumer --bootstrap-server kafka:9092 --topic event --from-beginning

#delete the topic
docker exec -it main_project-kafka-1 kafka-topics --delete --topic event --bootstrap-server localhost:29092

#see the currnt offset by the group; order_processing_group: group name
docker exec -it main_project-kafka-1 kafka-consumer-groups --bootstrap-server localhost:9092 --group order_processing_group --describe
                
#see that kafka is reciving messages
docker exec -it main_project-kafka-1 kafka-console-consumer --bootstrap-server localhost:9092 --topic event --from-beginning
##############################################################################################################################

##mongodb

#start mongo shell as superuser
docker-compose exec mongodb mongosh -u superuser -p a12s34 --authenticationDatabase 'admin'

#switch to or create `database1` and then create `events` collection
use database1
db.createCollection("events");

#see the events collcection inside database1
use database1
db.events.find().pretty();

#remove all th documents
db.events.remove({});

# Update a field in documents within `events` collection
db.events.updateMany({}, {$set: {message: 'hellow'}})

#Insert a new event into `events` collection
db.events.insertOne({message: "New Event", date: new Date(), location: "Location A"})

#Update a specific event
db.events.updateOne({id: 2}, {$set: {message: "New event message"}})

#Delete an event from `events` collection by its name
db.events.deleteOne({name: "Old Event"})
