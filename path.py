import os
from typing import List, Dict, Any, Literal


class Path:
    def __init__(self, name: str, path: str, type: Literal["folder", "file"]) -> None:
        self.name = name
        self.path = path
        self.type = type
        self.children: List[Path] = []

    def add_child(self, child: "Path") -> None:
        self.children.append(child)

    def to_dict(self, show_empty: bool) -> Dict[str, Any]:
        children = []
        for child in self.children:
            child_dict = child.to_dict(show_empty)
            if child_dict != None:
                children.append(child_dict)
        if (
            self.type == "file"
            or show_empty
            or (self.type == "folder" and len(children) != 0)
        ):
            return {
                "name": self.name,
                "path": self.path,
                "type": self.type,
                "children": children,
            }
        else:
            return None

    @staticmethod
    def construct_from_root(
        name: str, root: str, accepted_ext: List[str]
    ) -> "Path":
        root = Path(name, root, "folder")

        def find_all_files(parent: Path):
            for name in os.listdir(parent.path):
                path = f"{parent.path}/{name}"
                if os.path.isdir(path):
                    child = Path(name, path, "folder")
                    find_all_files(child)
                    parent.add_child(child)
                else:
                    if name.split(".")[-1] in accepted_ext:
                        child = Path(name, path, "file")
                        parent.add_child(child)

        find_all_files(root)
        return root
