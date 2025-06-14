import yaml
import os
from src.core import run_simulation

if __name__ == "__main__":
    # Load the default configuration relative to this file so that running the
    # script from another directory still works.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config", "default.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    run_simulation(config)
