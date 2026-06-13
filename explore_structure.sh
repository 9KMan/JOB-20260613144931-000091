#!/bin/bash
find . -type f -name "*.py" 2>/dev/null | head -50
echo "---"
find . -type f -name "*.md" 2>/dev/null | head -20
echo "---"
ls -la src/ 2>/dev/null || echo "No src directory"
