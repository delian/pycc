#!/bin/sh
set -e

on_exit () {
	[ $? -eq 0 ] && exit
	echo 'ERROR: Feature "Chezmoi Dotfile Manager" (ghcr.io/rio/features/chezmoi) failed to install!'
}

trap on_exit EXIT

set -a
. ../devcontainer-features.builtin.env
. ./devcontainer-features.env
set +a

echo ===========================================================================

echo 'Feature       : Chezmoi Dotfile Manager'
echo 'Description   : Manage your dotfiles across multiple diverse machines, securely.'
echo 'Id            : ghcr.io/rio/features/chezmoi'
echo 'Version       : 1.1.0'
echo 'Documentation : '
echo 'Options       :'
echo '    VERSION="latest"'
echo 'Environment   :'
printenv
echo ===========================================================================

chmod +x ./install.sh
./install.sh
