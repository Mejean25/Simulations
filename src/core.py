from src.models import percolation, ising  

def run_simulation(config):
    model = config['model']
    if model == 'percolation':
        percolation.run(config)
    elif model == 'ising':  
        ising.run(config)
    else:
        raise ValueError(f"Unknown model: {model}")
