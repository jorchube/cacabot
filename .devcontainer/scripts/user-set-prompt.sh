#!/usr/bin/env bash

echo '. /usr/share/git-core/contrib/completion/git-prompt.sh' >> ~/.bashrc
echo 'export PS1="\[\e[01;32m\][\[\e[01;34m\]\W\[\e[00m\]\[\e[01;35m\]$(declare -F __git_ps1 &>/dev/null && __git_ps1 " %s")\[\e[00m\]\[\e[01;32m\]]\[\e[00m\]$\[\e[00m\] "' >> ~/.bashrc
