#!/usr/bin/env bash

podman create -v ./:/app --name=cacabot-container cacabot-image
