#!/bin/zsh
# RPI Shell Tab Title — auto-names terminal tabs by project
# Source this from ~/.zshrc:  source ~/Projects/_RPI_STANDARDS/scripts/shell-tab-title.sh
# Propagates via git — update once, every machine gets it on pull.

function set_tab_title() {
  local dir="$PWD"
  local title=""
  case "$dir" in
    $HOME/Projects/_RPI_STANDARDS*) title="RPI-Standards" ;;
    $HOME/Projects/RAPID_TOOLS/*)   title=$(echo "$dir" | sed "s|$HOME/Projects/RAPID_TOOLS/||" | cut -d/ -f1) ;;
    $HOME/Projects/SENTINEL_TOOLS/*) title=$(echo "$dir" | sed "s|$HOME/Projects/SENTINEL_TOOLS/||" | cut -d/ -f1) ;;
    $HOME/Projects/PRODASHX_TOOLS/*) title=$(echo "$dir" | sed "s|$HOME/Projects/PRODASHX_TOOLS/||" | cut -d/ -f1) ;;
    $HOME/Projects/*)               title=$(echo "$dir" | sed "s|$HOME/Projects/||" | cut -d/ -f1) ;;
    $HOME)                          title="~" ;;
    *)                              title="${dir##*/}" ;;
  esac
  echo -ne "\033]0;${title}\007"
}

autoload -Uz add-zsh-hook
add-zsh-hook chpwd set_tab_title
set_tab_title
