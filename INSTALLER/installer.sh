unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac

OS="`uname`"
SEP=""
case $OS in
  'Linux')
    OS='Linux'
    SEP="/"
    alias ls='ls --color=auto'
    ;;
  'FreeBSD')
    OS='FreeBSD'
    SEP="/"
    alias ls='ls -G'
    ;;
  'WindowsNT')
    OS='Windows'
    SEP="\\"
    ;;
  'Darwin') 
    OS='Mac'
    SEP="/"
    ;;
  'SunOS')
    OS='Solaris'
    SEP="/"
    ;;
  'AIX') ;;
  *) ;;
esac



echo $OS
echo $SEP
SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

# Installing nightcapcore plugin/requirements
pip_updater="python -m pip install --upgrade pip"
eval $pip_updater

core_installer="python -m pip install -e "$SCRIPTPATH$SEP".."$SEP"nightcapcore"$SEP
cli_installer="python -m pip install -e "$SCRIPTPATH$SEP".."$SEP"nightcapcli"$SEP
packages_installer="python -m pip install -e "$SCRIPTPATH$SEP".."$SEP"nightcappackages"$SEP

eval $core_installer
eval $cli_installer
eval $packages_installer
eval $server_installer
# eval $client_installer

core_re_installer="python -m pip install -r "$SCRIPTPATH$SEP".."$SEP"nightcapcore"$SEP"requirements.txt"
packages_re_installer="python -m pip install -r "$SCRIPTPATH$SEP".."$SEP"nightcappackages"$SEP"requirements.txt"
cli_re_installer="python -m pip install -r "$SCRIPTPATH$SEP".."$SEP"nightcapcli"$SEP"requirements.txt"

eval $core_re_installer
eval $packages_re_installer
eval $server_re_installer
eval $cli_re_installer
# eval $client_re_installer

main_re_installer="python -m pip install -r "$SCRIPTPATH$SEP".."$SEP"requirements.txt"

eval $main_re_installer

