#!/bin/sh
# wait-for-it.sh: wait for a host and port to be available before executing a command

set -e

host="$1"
shift
cmd="$@"

until nc -z "$host" 8000; do
  >&2 echo "FastAPI is unavailable - sleeping"
  sleep 1
done

>&2 echo "FastAPI is up - executing command"
exec $cmd
