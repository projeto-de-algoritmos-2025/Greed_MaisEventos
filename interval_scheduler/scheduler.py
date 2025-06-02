def interval_scheduling(events):
    # Ordena pelo fim (datetime)
    sorted_events = sorted(events, key=lambda x: x[1])
    selected = []
    last_end = None

    for start, end in sorted_events:
        if last_end is None or start >= last_end:
            selected.append((start, end))
            last_end = end

    return selected
