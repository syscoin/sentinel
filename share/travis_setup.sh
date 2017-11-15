#!/bin/bash
set -evx

mkdir ~/.syscoincore

# safety check
if [ ! -f ~/.syscoincore/.syscoin.conf ]; then
  cp share/syscoin.conf.example ~/.syscoincore/syscoin.conf
fi
