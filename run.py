import yaml
from src.core import run_simulation

if __name__ == "__main__":
    with open("config/default.yaml", "r") as f:
        config = yaml.safe_load(f)
    run_simulation(config)
