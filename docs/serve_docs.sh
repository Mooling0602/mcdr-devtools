#!/bin/sh

cd "$(dirname "$0")" || exit 1

LANG_CODE=$1

if [ -n "$LANG_CODE" ]; then
  echo "Starting docs preview for language: $LANG_CODE..."
  sphinx-autobuild -D language="$LANG_CODE" --port 8000 source/ "build/html_$LANG_CODE/"
else
  echo "Starting docs preview in English (en_US)..."
  sphinx-autobuild --port 8000 source/ build/html/
fi
