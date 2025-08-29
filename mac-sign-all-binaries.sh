#!/bin/bash

APP_PATH="$1"
IDENTITY="${NOTARIZATION_CODESIGN_IDENTITY}"

if [ -z "$IDENTITY" ]; then
  echo "Error: Please set the NOTARIZATION_CODESIGN_IDENTITY environment variable."
  exit 1
fi

if [ -z "$APP_PATH" ]; then
  echo "Usage: $0 /path/to/YourApp.app"
  exit 1
fi

# Sign all files in Frameworks and MacOS subfolders of Contents
for subdir in Frameworks MacOS Resources; do
  target_dir="$APP_PATH/Contents/$subdir"
  if [ -d "$target_dir" ]; then
    find "$target_dir" -type f ! -type l | while read file; do
      if file "$file" | grep -E -q 'executable|shared object|shared library|binary|bundle'; then
        echo "Signing $file"
        codesign --force --options runtime --timestamp --sign "$IDENTITY" "$file"
      fi
    done
  fi
done

# Finally, sign the .app bundle itself
echo "Signing $APP_PATH"
codesign --force --options runtime --timestamp --sign "$IDENTITY" "$APP_PATH"
