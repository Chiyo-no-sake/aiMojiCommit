# check_dependencies.sh

check_dependencies() {
  local missing_bash_dependencies=()
  local missing_python_dependencies=()

  # Check git
  type git >/dev/null 2>&1 || missing_bash_dependencies+=("git")

  # Check fzf
  type fzf >/dev/null 2>&1 || missing_bash_dependencies+=("fzf")

  # Check yq
  type yq >/dev/null 2>&1 || missing_bash_dependencies+=("yq")

  # Check python3
  type python3 >/dev/null 2>&1 || missing_bash_dependencies+=("python3")

  if [[ ${#missing_bash_dependencies[@]} -gt 0 ]]; then
      echo "Error: The following bash dependencies are missing: ${missing_bash_dependencies[*]}"
      exit 1
  fi

  # Check PyYAML module
  python3 -c "import yaml" &>/dev/null || missing_python_dependencies+=("PyYAML")

  # Check openai module
  python3 -c "import openai" &>/dev/null || missing_python_dependencies+=("openai")

  if [[ ${#missing_python_dependencies[@]} -gt 0 ]]; then
    echo "Error: The following Python dependencies are missing: ${missing_python_dependencies[*]}"
    echo "Installing dependencies..."
    exit 1
  fi
}