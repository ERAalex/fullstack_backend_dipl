#!/bin/sh

TIMEOUT=30
HOST=$1
PORT=$2
shift 2

echo "Waiting for $HOST:$PORT..."

until nc -z $HOST $PORT; do
  sleep 1
  TIMEOUT=$(($TIMEOUT - 1))
  if [ $TIMEOUT -eq 0 ]; then
    echo "Timeout waiting for $HOST:$PORT"
    exit 1
  fi
done

echo "$HOST:$PORT is available, starting the application..."
exec "$@"