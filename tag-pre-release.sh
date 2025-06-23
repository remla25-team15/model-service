#!/bin/bash

# Check for uncommitted changes
if [[ -n $(git status --porcelain) ]]; then
  echo "You have uncommitted changes. Please commit or stash them before tagging."
  exit 1
fi

# Get current version from bumpver
BASE_VERSION=v$(bumpver show --no-fetch | grep 'Current Version' | awk '{print $3}' | cut -d'-' -f1)

if [ -z "$BASE_VERSION" ]; then
  echo "Could not detect base version from bumpver"
  exit 1
fi

# Pull tags from origin
git fetch --tags

# Get branch name (replace slashes with dashes)
BRANCH=$(git rev-parse --abbrev-ref HEAD | sed 's|/|-|g')

# Find latest tag for this branch and version
LATEST_TAG=$(git tag --list "${BASE_VERSION}-alpha.${BRANCH}.*" \
             | grep -E "${BASE_VERSION}-alpha\.${BRANCH}\.[0-9]+" \
             | sort -V | tail -n 1)

if [[ -z "$LATEST_TAG" ]]; then
  NEXT_NUM=1
else
  LAST_NUM=$(echo "$LATEST_TAG" | grep -oE '[0-9]+$')
  NEXT_NUM=$((LAST_NUM + 1))
fi

NEW_TAG="${BASE_VERSION}-alpha.${BRANCH}.${NEXT_NUM}"
echo "About to create tag: $NEW_TAG"

# Confirmation prompt
read -p "Proceed with creating and pushing this tag? (y/N): " CONFIRM
CONFIRM=$(echo "$CONFIRM" | tr '[:upper:]' '[:lower:]')

if [[ "$CONFIRM" == "y" || "$CONFIRM" == "yes" ]]; then
  git tag "$NEW_TAG"
  git push origin "$NEW_TAG"
  echo "Tag $NEW_TAG created and pushed successfully."
else
  echo "Aborted: No tag was created or pushed."
fi
