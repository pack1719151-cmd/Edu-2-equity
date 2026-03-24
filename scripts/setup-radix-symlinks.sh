#!/bin/bash
# Setup script to create symlinks for radix-ui packages in apps/web/node_modules
# This is needed because npm hoists workspace dependencies to the root

set -e

WEB_NODE_MODULES="/home/vinoth22/eduequity/eduequity-os/apps/web/node_modules"
ROOT_NODE_MODULES="/home/vinoth22/eduequity/eduequity-os/node_modules"

# Create apps/web/node_modules directory if it doesn't exist
mkdir -p "$WEB_NODE_MODULES"

# Create @radix-ui directory
mkdir -p "$WEB_NODE_MODULES/@radix-ui"

# Create symlinks for all radix-ui packages
cd "$WEB_NODE_MODULES/@radix-ui"

ln -sf ../../node_modules/@radix-ui/react-alert-dialog react-alert-dialog 2>/dev/null || true
ln -sf ../../node_modules/@radix-ui/react-avatar react-avatar 2>/dev/null || true
ln -sf ../../node_modules/@radix-ui/react-dialog react-dialog 2>/dev/null || true
ln -sf ../../node_modules/@radix-ui/react-dropdown-menu react-dropdown-menu 2>/dev/null || true
ln -sf ../../node_modules/@radix-ui/react-label react-label 2>/dev/null || true
ln -sf ../../node_modules/@radix-ui/react-select react-select 2>/dev/null || true
ln -sf ../../node_modules/@radix-ui/react-separator react-separator 2>/dev/null || true
ln -sf ../../node_modules/@radix-ui/react-slot react-slot 2>/dev/null || true
ln -sf ../../node_modules/@radix-ui/react-tabs react-tabs 2>/dev/null || true
ln -sf ../../node_modules/@radix-ui/react-toast react-toast 2>/dev/null || true
ln -sf ../../node_modules/@radix-ui/react-tooltip react-tooltip 2>/dev/null || true

echo "✓ Radix-ui symlinks created in apps/web/node_modules/@radix-ui/"

