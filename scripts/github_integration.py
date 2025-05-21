#!/usr/bin/env python3
"""
GitHub integration script for Codex Web-Native
This script provides utilities for working with GitHub repositories
and implementing Continuous Integration best practices.
"""

import os
import sys
import subprocess
import yaml
import re
from datetime import datetime
from pathlib import Path

# Resolve project root and audit directories
BASE_DIR = Path(__file__).resolve().parent.parent
AUDITS_DIR = BASE_DIR / "audits"
DIFFS_DIR = AUDITS_DIR / "diffs"


def verify_git_setup():
    """Verify that git is properly configured"""
    try:
        # Check if git is installed
        subprocess.run(["git", "--version"], check=True, capture_output=True)

        # Check if current directory is a git repository
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
        )

        # Check if a remote is configured
        remotes = subprocess.run(
            ["git", "remote", "-v"], check=True, capture_output=True, text=True
        ).stdout

        if not remotes:
            print("❌ No git remotes configured.")
            return False

        print("✅ Git repository is properly configured.")
        return True
    except subprocess.CalledProcessError:
        print("❌ Git is not properly configured.")
        return False


def check_coherence_markers(commit_msg):
    """Check if commit message has valid coherence marker"""
    # Load valid markers from registry
    try:
        registry_path = BASE_DIR / "prompt-registry.yaml"
        with open(registry_path, "r") as f:
            registry = yaml.safe_load(f)

        valid_markers = [item["name"] for item in registry.get("markers", [])]

        # Check for marker in commit message
        marker_pattern = r"^\[(\w+)\]"
        match = re.match(marker_pattern, commit_msg)

        if not match:
            print(f"❌ Commit message missing coherence marker: {commit_msg}")
            print(f"Valid markers: {', '.join(valid_markers)}")
            return False

        marker = match.group(1)
        if marker not in valid_markers:
            print(f"❌ Invalid coherence marker [{marker}]: {commit_msg}")
            print(f"Valid markers: {', '.join(valid_markers)}")
            return False

        print(f"✅ Valid coherence marker: [{marker}]")
        return True
    except Exception as e:
        print(f"❌ Error checking coherence markers: {e}")
        return False


def prepare_github_push(commit_msg):
    """Prepare changes for pushing to GitHub"""
    try:
        # Verify coherence marker
        if not check_coherence_markers(commit_msg):
            return False

        # Stage changes
        subprocess.run(["git", "add", "."], check=True)

        # Commit changes
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)

        print("✅ Changes committed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error preparing GitHub push: {e}")
        return False


def push_to_github(branch_name="main"):
    """Push committed changes to GitHub"""
    try:
        # Push changes
        subprocess.run(["git", "push", "origin", branch_name], check=True)

        print(f"✅ Changes pushed to GitHub ({branch_name} branch).")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error pushing to GitHub: {e}")
        return False


def create_pull_request(title, body, base_branch="main", head_branch=None):
    """Create a pull request on GitHub"""
    try:
        # Determine current branch if head_branch not specified
        if not head_branch:
            head_branch = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

        # Create the PR using GitHub CLI if available
        try:
            subprocess.run(["gh", "--version"], check=True, capture_output=True)

            # Create PR
            subprocess.run(
                [
                    "gh",
                    "pr",
                    "create",
                    "--title",
                    title,
                    "--body",
                    body,
                    "--base",
                    base_branch,
                    "--head",
                    head_branch,
                ],
                check=True,
            )

            print(f"✅ Pull request created successfully.")
            return True
        except subprocess.CalledProcessError:
            print(
                "GitHub CLI not installed. Please create PR manually or install GitHub CLI."
            )
            print(f"Branch to use for PR: {head_branch}")
            return False
    except Exception as e:
        print(f"❌ Error creating pull request: {e}")
        return False


def generate_diff_report(base_branch="main", head_branch=None):
    """Generate a diff report for changes"""
    try:
        # Determine current branch if head_branch not specified
        if not head_branch:
            head_branch = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

        # Create diffs directory if it doesn't exist
        os.makedirs(DIFFS_DIR, exist_ok=True)

        # Get changes
        diff_output = subprocess.run(
            ["git", "diff", "--name-status", f"{base_branch}..{head_branch}"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout

        # Parse changes
        changes = {"added": [], "modified": [], "deleted": []}
        for line in diff_output.strip().split("\n"):
            if not line:
                continue

            parts = line.split("\t", 1)
            if len(parts) != 2:
                continue

            status, file_path = parts

            if status.startswith("A"):
                changes["added"].append(file_path)
            elif status.startswith("M"):
                changes["modified"].append(file_path)
            elif status.startswith("D"):
                changes["deleted"].append(file_path)

        # Generate report content
        now = datetime.now()
        report_content = f"# Branch Diff Report: {head_branch}\n\n"
        report_content += f"Generated: {now.isoformat()}\n\n"

        report_content += "## Files Changed\n\n"
        report_content += f"- Added: {len(changes['added'])}\n"
        report_content += f"- Modified: {len(changes['modified'])}\n"
        report_content += f"- Deleted: {len(changes['deleted'])}\n\n"

        if changes["added"]:
            report_content += "### Added Files\n\n"
            for file in changes["added"]:
                report_content += f"- {file}\n"
            report_content += "\n"

        if changes["modified"]:
            report_content += "### Modified Files\n\n"
            for file in changes["modified"]:
                report_content += f"- {file}\n"
            report_content += "\n"

        if changes["deleted"]:
            report_content += "### Deleted Files\n\n"
            for file in changes["deleted"]:
                report_content += f"- {file}\n"
            report_content += "\n"

        # Get commit messages
        commit_output = subprocess.run(
            ["git", "log", "--format=%s", f"{base_branch}..{head_branch}"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout

        report_content += "## Commit Messages\n\n"
        for msg in commit_output.strip().split("\n"):
            if msg:
                report_content += f"- {msg}\n"

        # Extract markers from commit messages
        marker_pattern = r"^\[(\w+)\]"
        markers = []
        for msg in commit_output.strip().split("\n"):
            if not msg:
                continue

            match = re.match(marker_pattern, msg)
            if match:
                markers.append(match.group(1))

        if markers:
            report_content += "\n## Coherence Markers Used\n\n"
            for marker in sorted(set(markers)):
                report_content += f"- [{marker}]\n"

        # Save report
        timestamp = now.strftime("%Y%m%d%H%M%S")
        report_file = DIFFS_DIR / f"diff_{head_branch}_{timestamp}.md"
        with open(report_file, "w") as f:
            f.write(report_content)

        print(f"✅ Diff report generated: {report_file}")
        return str(report_file)
    except Exception as e:
        print(f"❌ Error generating diff report: {e}")
        return None


def create_feature_branch(feature_name):
    """Create a new feature branch"""
    try:
        # Clean feature name for branch
        clean_name = re.sub(r"[^\w-]", "-", feature_name.lower())
        branch_name = f"feat/{clean_name}"

        # Create and checkout branch
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)

        print(f"✅ Created and switched to feature branch: {branch_name}")
        return branch_name
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating feature branch: {e}")
        return None


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python github_integration.py verify")
        print('  python github_integration.py commit "[marker] Commit message"')
        print("  python github_integration.py push")
        print('  python github_integration.py feature "Feature name"')
        print('  python github_integration.py pr "PR title" "PR description"')
        print("  python github_integration.py diff")
        return 1

    command = sys.argv[1].lower()

    if command == "verify":
        verify_git_setup()
    elif command == "commit":
        if len(sys.argv) < 3:
            print("Error: Commit message required.")
            return 1
        prepare_github_push(sys.argv[2])
    elif command == "push":
        branch = sys.argv[2] if len(sys.argv) > 2 else "main"
        push_to_github(branch)
    elif command == "feature":
        if len(sys.argv) < 3:
            print("Error: Feature name required.")
            return 1
        create_feature_branch(sys.argv[2])
    elif command == "pr":
        if len(sys.argv) < 4:
            print("Error: PR title and description required.")
            return 1
        create_pull_request(sys.argv[2], sys.argv[3])
    elif command == "diff":
        base = sys.argv[2] if len(sys.argv) > 2 else "main"
        head = sys.argv[3] if len(sys.argv) > 3 else None
        generate_diff_report(base, head)
    else:
        print(f"Unknown command: {command}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
