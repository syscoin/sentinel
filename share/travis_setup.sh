#!/bin/bash
set -evx

mkdir ~/.syscoin

# safety check
if [ ! -f ~/.syscoin/.syscoin.conf ]; then
  cp share/syscoin.conf.example ~/.syscoin/syscoin.conf
fi
