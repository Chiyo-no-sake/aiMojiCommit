import subprocess
import os
import tempfile

class GitManager:
    @staticmethod
    def is_git_installed():
        try:
            subprocess.check_output(["type", "git"])
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def is_inside_repository():
        try:
            subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"])
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def get_diff_stats():
        try:
            output = subprocess.check_output(["git", "diff", "--cached", "--stat"])
            return output.decode("utf-8").strip()
        except subprocess.CalledProcessError:
            return ""

    @staticmethod
    def get_diff_changes():
        try:
            output = subprocess.check_output(["git", "diff", "--cached", "-U5"])
            return output.decode("utf-8").strip()
        except subprocess.CalledProcessError:
            return ""

    @staticmethod
    def add_changes():
        subprocess.call(["git", "add", "--all"])

    @staticmethod
    def commit_with_message(commit_message):
        temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
        temp_file.write(commit_message)
        temp_file.close()

        try:
            subprocess.call(["git", "commit", "-eF", temp_file.name])
        finally:
            os.unlink(temp_file.name)

    @staticmethod
    def get_merge_commit_message():
        merge_message_file = subprocess.check_output(["git", "rev-parse", "--git-dir"]).decode("utf-8").strip() + "/MERGE_MSG"
        if subprocess.call(["test", "-f", merge_message_file]) == 0:
            with open(merge_message_file, "r") as file:
                return file.read().strip()
        return None
