#!/bin/bash
# wait-for-kafka.sh

set -e

host="$1"
shift
cmd="$@"

until nc -z "$host" 9092; do
  >&2 echo "Kafka is unavailable - sleeping"
  sleep 1
done

>&2 echo "Kafka is up - executing command"
exec $cmd

(venv) PS C:\Users\danko\Desktop\main_project> docker exec -it main_project-zookeeper-1 /bin/sh