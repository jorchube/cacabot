#!/usr/bin/env bash

set -euo pipefail
IFS=$'\n\t'

dnf update -y
dnf install -y git neovim unzip pip
