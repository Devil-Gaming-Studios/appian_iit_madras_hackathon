import numpy as np

def simulate_process(
    wip,
    arrival_rate,
    agents,
    avg_service_time,
    sla_hours,
    horizon_hours=8,
    runs=500
):
    sla_breaches = 0
    backlog_snapshots = []

    hourly_backlog_avg = np.zeros(horizon_hours)

    for _ in range(runs):
        queue = float(wip)

        for hour in range(horizon_hours):
            arrivals = np.random.poisson(arrival_rate)
            completed = min(queue, agents * (1 / avg_service_time))
            queue = max(queue + arrivals - completed, 0)

            hourly_backlog_avg[hour] += queue

        if queue > agents * sla_hours:
            sla_breaches += 1

    hourly_backlog_avg /= runs

    return {
        "breach_probability": round((sla_breaches / runs) * 100, 2),
        "expected_backlog": int(hourly_backlog_avg[-1]),
        "timeline": hourly_backlog_avg.tolist()
    }
