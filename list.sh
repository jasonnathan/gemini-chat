#!/bin/bash

function list_structure() {
  local dir="$1"
  for entry in "$dir"/*; do
    if [[ -d "$entry" && "$entry" != "venv" ]]; then
      if [[ ! "$entry" =~ (lib|bin|include) ]]; then
        echo "│  $entry"
        list_structure "$entry"
      fi
    else
      echo "└── $entry"
    fi
  done
}

list_structure .