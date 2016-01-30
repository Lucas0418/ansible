#!/bin/sh
# A shell script to help ansible admin to add ssh key to managed machine
usage(){
    printf "./sshkeyconfig.sh -u [username] -h [host]\n"
    exit 1
}
while getopts "u:h:" opt
do
    case $opt in
        'u')
            user=$OPTARG
            ;;
        'h')
            host=$OPTARG
            ;;
    esac
done
[ -f ~/.ssh/id_rsa.pub ] || ssh-keygen -t rsa -P ""
[ $user"" = "" -o $host"" = "" ]&&usage
grep "^\<${host}\>" $ANSIBLE_INVENTORY 1>/dev/null 2>&1 || printf "%s\n" ${host} >> $ANSIBLE_INVENTORY
cat <<EOF > sshkeyconfigremote.sh
mkdir -p ~/.ssh/
chmod 700 ~/.ssh
cat /tmp/id_rsa.pub>>~/.ssh/authorized_keys
rm /tmp/id_rsa.pub
chmod 600 ~/.ssh/authorized_keys
EOF
scp ~/.ssh/id_rsa.pub sshkeyconfigremote.sh ${user}@${host}:/tmp
ansible ${host} -u ${user} -k -a "bash /tmp/sshkeyconfigremote.sh"
ansible ${host} -u ${user} -k -a "rm /tmp/sshkeyconfigremote.sh"
rm sshkeyconfigremote.sh
