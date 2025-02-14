import glob
import inspect
import os

from ...utils.lazy_import import lazy_import

# Lazy import of aifs, imported when needed to speed up start time
aifs = lazy_import("aifs")


class Skills:
    def __init__(self, computer):
        self.computer = computer
        self.skills_dir = None

    def search(self, query, module=None, paths=None):
        if paths:
            return aifs.search(query, file_paths=paths, python_docstrings_only=True)

        if module is None:
            module = self.computer

        # Get the path of the module
        module_path = os.path.dirname(inspect.getfile(module.__class__))

        # Use aifs to search over the files in the module path
        results = aifs.search(query, path=module_path, python_docstrings_only=True)
        return results

    def import_skills(self):
        self.computer.save_skills = False
        for file in glob.glob(os.path.join(self.skills_dir, "*.py")):
            with open(file, "r") as f:
                self.computer.run("python", f.read())
        self.computer.save_skills = True
