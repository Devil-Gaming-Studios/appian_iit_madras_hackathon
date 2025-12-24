from simulation import simulate_process

def run_scenario(base_config, agent_change=0, automation_factor=1.0):
    config = base_config.copy()

    config["agents"] = max(1, int(config["agents"] + agent_change))
    config["avg_service_time"] = float(config["avg_service_time"]) * float(automation_factor)

    return simulate_process(**config)
