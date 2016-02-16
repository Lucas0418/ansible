# personal ansible tools
## Overview
**sshconfigkey.sh**, for automatic do the ssh key config on remote.

**deploy.sh**, for preinstall ansible.

**ai.py**, ansible dynamic inventory script.

## ai.py
According to ansible dynamic inventory script conventions. 
Read inventory data from mysql database,
then return the json.

More about the data tables structure in database in [Ansible_Supervisor](https://github.com/Lucas0418/ansible_supervisor),
that I am developing for ansible management with a few modules now.

## playbooks
Ansible playbooks.

### playbooks/tasks/authorized_key
Auto add ansible's authorized keys to remote managed machines

