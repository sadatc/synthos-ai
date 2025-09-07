#!/bin/bash

# Exit if any command fails
set -e

echo "📘 Building the Synthos Jupyter Book..."
jupyter-book build .

echo "🚀 Publishing to GitHub Pages using ghp-import..."
ghp-import -n -p -f _build/html

echo "✅ Done! Your site should be live shortly at:"
echo "   https://drsadat.github.io/synthos/"
echo "🕒 It may take a minute or two for the changes to appear."
