#!/bin/bash
# Test on Ubuntu
# Preinstall Ansible
workdir=`pwd`
miss=()
printf "Preinstall Start.\n"
printf "Now check the prerequisites.\n"
printf "Check python3.\n"
command -v python3 || miss[${#miss[@]}]="python3"
printf "Check pip.\n"
command -v pip || miss[${#miss[@]}]="pip"
printf "Check virtualenv.\n"
command -v virtualenv || miss[${#miss[@]}]="python-virtualenv"
if [ ${#miss[@]} -ne 0 ];then
  printf "Now install the missing:\n\t%s.\n" "${miss[*]}"
  sudo apt-get install ${miss[*]}
  if [ $? -ne 0 ];then
    printf "Install failed, check error log, then rerun this script.\n"
    exit 1
  fi
fi
command -v deactivate && deactivate
[ -f ansiblevirenv/bin/activate ] || virtualenv -p python3 ansiblevirenv
. ansiblevirenv/bin/activate
if [ ${VIRTUAL_ENV}"z" != ${workdir}"/ansiblevirenvz" ];then
  printf "Activate the virtualenv failed, Check error log, then rerun this script.\n"
  exit 1
fi
pip install paramiko PyYAML Jinja2 httplib2 six
printf "Preinstall Finished.\n"
