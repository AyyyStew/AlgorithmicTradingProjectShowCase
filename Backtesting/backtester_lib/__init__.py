# lib/strategies/__init__.py
import importlib
import pkgutil

# Dynamically import all submodules
package_name = __name__
__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__, package_name + "."):
    if not module_name == "backtester_lib.setup":
        importlib.import_module(module_name)
        __all__.append(module_name.split(".")[-1])
