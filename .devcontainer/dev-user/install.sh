#!/usr/bin/env bash

set -euo pipefail
IFS=$'\n\t'

USER_NAME="${USERNAME}"
USER_UID="${USER_ID}"
USER_GID="${GROUP_ID}"

dnf update -y
dnf install -y sudo

groupadd --gid "${USER_GID}" "${USER_NAME}"
useradd --shell /bin/bash --uid "${USER_UID}" --gid "${USER_GID}" --create-home "${USER_NAME}"
echo -n "${USER_NAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

echo "${USER_NAME} ALL=(root) NOPASSWD:ALL" > "/etc/sudoers.d/${USER_NAME}"
chmod 0440 "/etc/sudoers.d/${USER_NAME}"

mkdir -p "/home/${USER_NAME}/.ssh"
chown -R "${USER_NAME}:${USER_NAME}" "/home/${USER_NAME}/.ssh"

mkdir -p "/home/${USER_NAME}/.config"
chown -R "${USER_NAME}:${USER_NAME}" "/home/${USER_NAME}/.config"

echo "Done!"
