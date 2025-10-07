import importlib
import os
from typing import Dict, Type

class PluginManager:
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, Type] = {}

    def load_plugins(self):
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
            return

        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("_"):
                module_name = filename[:-3]
                module_path = os.path.join(self.plugin_dir, filename)
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                if spec:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    if hasattr(module, "register"):
                        self.plugins[module_name] = module

    def get_plugin(self, name: str):
        return self.plugins.get(name)
