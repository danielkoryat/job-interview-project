#run ookeeper
docker compose up zookeeper -d

#run kafka
docker compose up kafka -d

#create event topic
docker exec -it main_project-kafka-1 kafka-topics --create --topic event --partitions 1 --replication-factor 1 --bootstrap-server localhost:29092

#print all the meassages in the event topic and listen to new messages recived
docker exec -it main_project-kafka-1 kafka-console-consumer --bootstrap-server kafka:9092 --topic event --from-beginning

#run the kafka provider
docker compose up kafka-provider 

#run mongodb
docker compose up mongodb -d

#create a collection named events
docker exec -it main_project-mongodb-1 mongosh -u superuser -p a12s34 --authenticationDatabase 'admin' --eval "db.getSiblingDB('database1').createCollection('events')"

#run the kafka consumer
docker compose up kafka-consumer 


#get all the documents in the events collection
docker exec -it main_project-mongodb-1 mongosh -u superuser -p a12s34 --authenticationDatabase 'admin' --eval "const eventsCollection = db.getSiblingDB('database1').events; eventsCollection.find().forEach(doc => print(JSON.stringify(doc, null, 2))); print('Total documents in events collection:', eventsCollection.countDocuments({}));"


#run redis
docker compose up redis -d

#run the redis provider
docker compose up redis-provider 

#get all the keys in redis
docker exec -it main_project-redis-1 redis-cli KEYS '*'

#get sorted keys from redis
docker exec -i main_project-redis-1 redis-cli KEYS '*' | ForEach-Object { $_.Trim() } | Sort-Object { [int]($_ -split ':')[0] }

#run again the kafka consumer
docker compose up kafka-consumer

#run gain the redis provider
docker compose up redis-provider  

#get all the keys frpm redis
docker exec -it main_project-redis-1 redis-cli KEYS '*'


