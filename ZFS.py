"""
ZFS.py - the "filesystem" for FakeOS.

A tree of dicts, kept in memory and mirrored to a JSON file on disk
(fakeos_fs.json) so state survives between sessions. Folders are dicts,
files are strings (their content). Wire this into core.py by importing
the FakeFS class and calling its methods from your command handlers.
"""

import json
import os

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fakeos_fs.json")


class FakeFSError(Exception):
    pass


class FakeFS:
    def __init__(self):
        self.root = {"home": {"guest": {}}, "etc": {}, "tmp": {}}
        self.cwd = ["home", "guest"]
        self.load()

    # ---------- persistence ----------

    def save(self):
        with open(SAVE_FILE, "w") as f:
            json.dump({"root": self.root, "cwd": self.cwd}, f, indent=2)

    def load(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    data = json.load(f)
                self.root = data.get("root", self.root)
                self.cwd = data.get("cwd", self.cwd)
            except (json.JSONDecodeError, OSError):
                pass  # corrupt/missing save -> fall back to fresh fs

    # ---------- path helpers ----------

    def pwd(self):
        return "/" + "/".join(self.cwd)

    def _resolve(self, path):
        """Turn an absolute or relative path string into a list of parts."""
        if path in ("", "."):
            return list(self.cwd)
        parts = path.split("/")
        stack = list(self.cwd) if not path.startswith("/") else []
        for part in parts:
            if part in ("", "."):
                continue
            elif part == "..":
                if stack:
                    stack.pop()
            else:
                stack.append(part)
        return stack

    def _get_node(self, parts):
        """Walk the tree to the dict/str at `parts`. Raises FakeFSError if missing."""
        node = self.root
        for part in parts:
            if not isinstance(node, dict) or part not in node:
                raise FakeFSError(f"no such file or directory: {part}")
            node = node[part]
        return node

    def _get_parent(self, parts):
        if not parts:
            raise FakeFSError("cannot operate on root")
        parent = self._get_node(parts[:-1])
        if not isinstance(parent, dict):
            raise FakeFSError("not a directory")
        return parent, parts[-1]

    # ---------- commands ----------

    def ls(self, path=""):
        node = self._get_node(self._resolve(path))
        if isinstance(node, dict):
            return "  ".join(sorted(node.keys()))
        raise FakeFSError("not a directory")

    def echo(self, text, redirect=None, append=False):
        """
        echo text            -> just returns the text (print it in core.py)
        echo text > file     -> overwrite file with text
        echo text >> file    -> append text to file (newline-separated)
        """
        if redirect is None:
            return text
        parent, leaf = self._get_parent(self._resolve(redirect))
        if append and isinstance(parent.get(leaf), str):
            parent[leaf] = parent[leaf] + "\n" + text
        else:
            parent[leaf] = text
        self.save()
        return ""

    def cd(self, path):
        target = self._resolve(path)
        node = self._get_node(target)
        if not isinstance(node, dict):
            raise FakeFSError("not a directory")
        self.cwd = target
        self.save()

    def mkdir(self, name):
        parent, leaf = self._get_parent(self._resolve(name))
        if leaf in parent:
            raise FakeFSError("already exists")
        parent[leaf] = {}
        self.save()

    def touch(self, name, content=""):
        parent, leaf = self._get_parent(self._resolve(name))
        if leaf not in parent:
            parent[leaf] = content
        self.save()

    def write(self, name, content):
        parent, leaf = self._get_parent(self._resolve(name))
        parent[leaf] = content
        self.save()

    def cat(self, name):
        node = self._get_node(self._resolve(name))
        if isinstance(node, dict):
            raise FakeFSError("is a directory")
        return node

    def rm(self, name):
        parent, leaf = self._get_parent(self._resolve(name))
        if leaf not in parent:
            raise FakeFSError("no such file or directory")
        del parent[leaf]
        self.save()

    def tree(self, path="", indent=0):
        node = self._get_node(self._resolve(path))
        lines = []
        if isinstance(node, dict):
            for key in sorted(node.keys()):
                lines.append("  " * indent + key)
                if isinstance(node[key], dict):
                    lines.extend(self.tree_lines(node[key], indent + 1))
        return "\n".join(lines)

    def tree_lines(self, node, indent):
        lines = []
        for key in sorted(node.keys()):
            lines.append("  " * indent + key)
            if isinstance(node[key], dict):
                lines.extend(self.tree_lines(node[key], indent + 1))
        return lines
