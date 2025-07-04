#!/usr/bin/env python

import json
import subprocess
from pathlib import Path
import questionary
import requests

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"

CATEGORIES = {
    "tools": SRC_DIR / "tools",
    "tests": SRC_DIR / "tests",
    "servers": "uv run -m src.core_module",  # special case
}

def list_modules(category_path: Path, category_name: str) -> dict:
    """
    Recursively finds all .py modules under category_path.
    Returns a dict like: {'subfolder --- filename': 'src.category.subfolder.filename'}
    """
    modules = {}
    for file in category_path.rglob("*.py"):
        if file.name.startswith("_") or file.name == "__main__.py":
            continue
        relative = file.relative_to(SRC_DIR)
        parts = relative.with_suffix('').parts  # remove .py and split path
        label = " --- ".join(parts[1:])  # skip category prefix
        module_path = ".".join(["src", *parts])
        modules[label] = module_path
    return modules

def run_module(module_path: str):
    print(f"🚀 Running: uv run -m {module_path}\n")
    subprocess.run(["uv", "run", "-m", module_path])

def run_server():
    print("🚀 Starting server via: uv run -m src.core_module\n")
    subprocess.run(["uv", "run", "-m", "src.core_module"])

def print_link_session_report():
    # Adjust URL and session_id as needed
    session_id = questionary.text("Enter session_id to fetch report:", default="0").ask()
    url = f"http://127.0.0.1:8192/session_report/{session_id}"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            print("=== Link Session Report ===")
            print(json.dumps(resp.json(), indent=4, ensure_ascii=False))
        else:
            print(f"Failed to fetch report: HTTP {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"Error fetching report: {e}")

def main():
    top_choices = [
        "Run link_session_cli (uv run -m src.tools.cli.link_session_cli)",
        "Print LinkSession report",
        "Choose category to run module",
    ]
    choice = questionary.select("Select an option:", choices=top_choices).ask()

    if choice == top_choices[0]:
        run_module("src.tools.cli.link_session_cli")
        return
    elif choice == top_choices[1]:
        print_link_session_report()
        return

    # Normal category selection
    category = questionary.select(
        "Choose category:",
        choices=list(CATEGORIES.keys())
    ).ask()

    if not category:
        print("No category selected.")
        return

    if category == "servers":
        run_server()
        return

    category_path = CATEGORIES[category]
    modules = list_modules(category_path, category)

    if not modules:
        print("No modules found.")
        return

    module_label = questionary.select(
        f"Choose {category} module to run:",
        choices=list(modules.keys())
    ).ask()

    if module_label:
        run_module(modules[module_label])

if __name__ == "__main__":
    main()
