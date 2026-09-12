#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'TXT'
Usage:
  install_skill.sh --target codex|claude-code|cursor
  install_skill.sh --target dir --path /path/to/skills
  install_skill.sh --target <target> --dry-run
TXT
}

target=""
dest_root=""
dry_run=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target)
      target="${2:-}"
      shift 2
      ;;
    --path)
      dest_root="${2:-}"
      shift 2
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [ -z "$target" ]; then
  usage >&2
  exit 2
fi

case "$target" in
  codex) dest_root="${HOME}/.codex/skills" ;;
  claude-code) dest_root="${HOME}/.claude/skills" ;;
  cursor) dest_root="${HOME}/.cursor/skills" ;;
  dir)
    if [ -z "$dest_root" ]; then
      echo "--path is required for --target dir" >&2
      exit 2
    fi
    ;;
  *)
    echo "Unsupported target: $target" >&2
    exit 2
    ;;
esac

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
skill_root=$(CDPATH= cd -- "$script_dir/.." && pwd)
skill_name=$(basename -- "$skill_root")
dest="${dest_root}/${skill_name}"

echo "Source: $skill_root"
echo "Destination: $dest"
if [ "$dry_run" -eq 1 ]; then
  exit 0
fi

mkdir -p "$dest_root"
rm -rf "$dest"
cp -R "$skill_root" "$dest"
echo "Installed: $dest"
