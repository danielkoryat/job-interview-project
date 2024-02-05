##env

#Change Execution Policy for the Current Session to enable virtual environment
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
##############################################################################################################################

##docker
#start the docker compose
docker-compose up -d

#start a spesific container
docker compose up "container name"


##############################################################################################################################
##kafka

#creates a new topic in the kafka cluster main_project-kafka-1: name of the container  event: name of the topic 
docker exec -it main_project-kafka-1 kafka-topics --create --topic event --partitions 1 --replication-factor 1 --bootstrap-server localhost:29092

#delete the topic
docker exec -it main_project-kafka-1 kafka-topics --delete --topic event --bootstrap-server localhost:29092

#list all the topics in the kafka cluster
docker exec -it main_project-kafka-1 kafka-topics --list --bootstrap-server localhost:29092


#see the events in the kafka cluster main_project-kafka-1 event topic
docker exec -it main_project-kafka-1 kafka-console-consumer --bootstrap-server kafka:9092 --topic event --from-beginning

#see the currnt offset by the group; order_processing_group: group name
docker exec -it main_project-kafka-1 kafka-consumer-groups --bootstrap-server localhost:9092 --group order_processing_group --describe
                
##############################################################################################################################

##mongodb

#start mongo shell as superuser
docker-compose exec mongodb mongosh -u superuser -p a12s34 --authenticationDatabase 'admin'

#switch to or create `database1` and then create `events` collection
docker-compose exec mongodb mongosh -u superuser -p a12s34 --authenticationDatabase 'admin' --eval 'db.getSiblingDB(`"database1`").createCollection(`"events`");'

#see the events collcection inside database1
docker-compose exec mongodb mongosh -u superuser -p a12s34 --authenticationDatabase 'admin' --eval 'db.getSiblingDB(`"database1`").events.find().pretty();'


#remove all th documents
docker-compose exec mongodb mongosh -u superuser -p a12s34 --authenticationDatabase 'admin' --eval 'db.getSiblingDB(`"database1`").events.remove({});'

# Update a field in documents within `events` collection
docker-compose exec mongodb mongosh -u superuser -p a12s34 --authenticationDatabase 'admin' --eval 'db.getSiblingDB(`"database1`").events.updateMany({}, {$set: {message: `"hello"`}});'

#Insert a new event into `events` collection
docker-compose exec mongodb mongosh -u superuser -p a12s34 --authenticationDatabase 'admin' --eval 'db.getSiblingDB(`"database1`").events.insertOne({message: `"New Event"`, date: new Date(), location: `"Location A"`});'

#Update a specific event
docker-compose exec mongodb mongosh -u superuser -p a12s34 --authenticationDatabase 'admin' --eval 'db.getSiblingDB(`"database1`").events.updateOne({id: 2}, {$set: {message: `"New event message"`}});'

#Delete an event from `events` collection by its name
docker-compose exec mongodb mongosh -u superuser -p a12s34 --authenticationDatabase 'admin' --eval 'db.getSiblingDB(`"database1`").events.deleteOne({name: `"Old Event"`});'

#delete the events collection
docker-compose exec mongodb mongosh -u superuser -p a12s34 --authenticationDatabase 'admin' --eval 'db.getSiblingDB(`"database1`").events.drop();'


#get a list of all the collections
docker-compose exec mongodb mongosh -u superuser -p a12s34 --authenticationDatabase 'admin' --eval 'db.getSiblingDB(`"admin`").getCollectionNames();'


#list indexes in all collections
docker-compose exec mongodb mongosh -u superuser -p a12s34 --authenticationDatabase 'admin' --eval 'db.getSiblingDB(`"database1`").events.getIndexes();'

#prove that the timestemp is stored as bson date
docker-compose exec mongodb mongosh -u superuser -p a12s34 --authenticationDatabase 'admin' --eval 'db.getSiblingDB(`"database1`").events.aggregate([{ $limit: 1 }, { $project: { timestampType: { $type: `$"timestamp"` } } }]);'


##########################################################################################################################
##redis

# Script to list all keys in Redis
docker-compose exec redis redis-cli KEYS '*'

# Script to get the value of a key
docker-compose exec redis redis-cli GET "key_name"

# Script to crete a key VALUE
docker-compose exec redis redis-cli SET key_name "value"

# Script to delete all keys from the current Redis database
docker-compose exec redis redis-cli FLUSHDB

#get the sorted value with an error becouse last_processes_timestamp
docker exec -i main_project-redis-1 redis-cli KEYS '*' | ForEach-Object { $_.Trim() } | Sort-Object { [int]($_ -split ':')[0] }