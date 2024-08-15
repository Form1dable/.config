!/bin/bash

PKGLIST=./pkglist.txt

# Ensure that the package list exists
if [[ ! -f $PKGLIST ]]; then
  echo "Package list not found at $PKGLIST"
  exit 1
fi

sudo pacman -Syu --noconfirm

# Install packages from the list
xargs -a $PKGLIST sudo pacman -S --needed --noconfirm

echo "Package installation complete."
