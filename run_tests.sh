#!/bin/bash

python=python3.10

cd $(dirname $0)

files=$(find ./examples -type f -name "*.py" | sort)
for file in $files; do
  if test "$($python $file)" == "$($python main.py $file)"; then
    echo -e "$(basename $file) -------------------------------- Pass"
  else
    echo -e "$(basename $file) -------------------------------- Failed"
  fi
done

# find . -type d -name "__pycache__" | xargs -i rm -r {}
