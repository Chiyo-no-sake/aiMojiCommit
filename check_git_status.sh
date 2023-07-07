# check_git_status.sh

check_git_status() {
  if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "Error: Not a git repository. Exiting."
    exit 1
  fi

  if git diff --cached --quiet; then
    echo "No changes added to commit. Use 'git add' to track changes."
    exit 1
  fi
}