#!/bin/bash

nvm_string="nvm-sh/nvm";

git_latest_version() {
   basename $(curl -fs -o/dev/null -w %{redirect_url} https://github.com/$1/releases/latest)
}

latest_version_number=$(git_latest_version "${nvm_string}");
echo NVM is at version: ${latest_version_number}
wget -qO- https://raw.githubusercontent.com/${nvm_string}/${latest_version_number}/install.sh | bash
