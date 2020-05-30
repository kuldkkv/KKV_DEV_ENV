# -----------------------------
# KKV DEV ENV .profile settings
# -----------------------------
echo -n "setting DEV_ENV profile ..."
export HISTSIZE=5000
export PATH=$PATH:.
#export PS1='$(logname)@$(hostname -s):$PWD % '
export PS1=$'\E[34;7m$(logname)@$(hostname -s)\E[0m:\E[32;1m$PWD\E[0m$ '

set -o vi
echo "done"

