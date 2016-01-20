#!/bin/sh
# A shell script to help ansible admin to add ssh key to managed machine
usage(){
    printf "./sshkeyconfig.sh -u [username] -h [host]\n"
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
[ $user"" = "" -o $host"" = "" ]&&usage
grep "^\<${host}\>" $ANSIBLE_INVENTORY 1>/dev/null 2>&1 || printf "%s\n" ${host} >> $ANSIBLE_INVENTORY
cat <<EOF > sshkeyconfigremote.sh
cat /tmp/id_rsa.pub>>~/.ssh/authorized_keys
rm /tmp/id_rsa.pub
EOF
scp ~/.ssh/id_rsa.pub sshkeyconfigremote.sh ${user}@${host}:/tmp
ansible ${host} -u ${user} -k -a "bash /tmp/sshkeyconfigremote.sh"
ansible ${host} -u ${user} -k -a "rm /tmp/sshkeyconfigremote.sh"
