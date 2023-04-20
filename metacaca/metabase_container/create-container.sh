#!/usr/bin/env bash

CACABOT_APP=../

podman create -p 3000:3000 -v $CACABOT_APP/:/cacabot_app -v ./metabase_db/:/metabase.db --name=metacaca-container metacaca-image
