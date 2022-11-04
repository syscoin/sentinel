#!/usr/bin/env bash

# This script starts a local tanenbaum setup using Docker Compose.
# Don't run this script directly. Run it using the makefile, e.g. `make tanenbaum-up`.
# To clean up, run `make tanenbaum-clean`.

set -eu

L1_URL="http://localhost:8545"
# fill in with your cloudflare R2 auth info
PODA_DB_ACCOUNT_ID=
PODA_DB_KEY_ID=
PODA_DB_ACCESS_KEY=
NETWORK=testnet
# Helper method that waits for a given URL to be up. Can't use
# cURL's built-in retry logic because connection reset errors
# are ignored unless you're using a very recent version of cURL
function wait_up {
  echo -n "Waiting for $1 to come up..."
  i=0
  until curl -s -f -o /dev/null "$1"
  do
    echo -n .
    sleep 0.25

    ((i=i+1))
    if [ "$i" -eq 300 ]; then
      echo " Timeout!" >&2
      exit 1
    fi
  done
  echo "Done!"
}


# Bring up L1.
(
  echo "Bringing up L1..."
  DOCKER_BUILDKIT=1 docker-compose build --progress plain
  PODA_DB_ACCOUNT_ID="$PODA_DB_ACCOUNT_ID" \
  PODA_DB_KEY_ID="$PODA_DB_KEY_ID" \
  PODA_DB_ACCESS_KEY="$PODA_DB_ACCESS_KEY" \
  NETWORK="$NETWORK" \
  docker-compose up -d l1
  wait_up $L1_URL
)

echo "L1 ready. Running PoDA server."

