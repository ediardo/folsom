#!/usr/bin/env bash
set -eu
apt-get update
apt-get install python-dev python-pip
easy_install pip
pip install --upgrade --force pip
pip install python-barbicanclient
pip install python-keystoneclient

export PYTHONPATH=$PYTHONPATH:..
# don't forget to copy openrc to /opt
echo "source /etc/kolla/admin-openrc.sh" >> /root/.bashrc
# load new profile
exec bash

# create a fernet key and store it in Barbican
function generate_fernet_key {
python << EOL
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print key
EOL
}

if ! grep -q 'export key_ref' /root/.bashrc; then
  project_key=`generate_fernet_key`
  key_metadata=`barbican secret store --name 'project_key' --payload $project_key --secret-type symmetric --algorithm fernet -f shell`
  b=${key_metadata#*href=\"};
  key_ref=${b%%\"*};
  [[ -z "$key_ref" ]] && { echo "Warning: key reference is empty, please rexecute the script" ; exit 1; }
  echo "export key_ref=$key_ref" | tee -a /root/.bashrc
  exec bash
fi
