from src.models import percolation

def run_simulation(config):
    if config['model'] == 'percolation':
        percolation.run(config)
    else:
        raise ValueError(f"Unknown model: {config['model']}")
