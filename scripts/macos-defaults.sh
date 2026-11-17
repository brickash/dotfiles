#!/bin/sh
# Restore selected macOS preferences for the current user.
set -eu

if [ "$(uname -s)" != Darwin ]; then
  echo "This script requires macOS." >&2
  exit 1
fi

# Dock: position on the left and keep it visible.
defaults write com.apple.dock orientation -string left
defaults write com.apple.dock autohide -bool false
killall Dock
