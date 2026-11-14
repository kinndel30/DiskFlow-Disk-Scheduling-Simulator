def format_result(result, initial_head):

    algorithm = result["algorithm"]
    movements = result["movements"]
    total = result["total_movement"]

    # 1. Build service sequence
    sequence = [initial_head] + result["sequence"]

    # 2. Build computation table
    rows = []

    for step, movement in enumerate(movements, start=1):

        rows.append({
            "step": step,
            "from": movement["from"],
            "to": movement["to"],
            "head_movement": (
                f'{movement["from"]} -> {movement["to"]}'
            ),
            "distance": movement["movement"]
        })

    # 3. Build mathematical solution
    distances = [
        movement["movement"]
        for movement in movements
    ]

    equation = " + ".join(
        str(distance) for distance in distances
    )

    if distances:
        solution = f"{equation} = {total}"
    else:
        solution = "0 = 0"

    # 4. Algorithm explanations
    explanations = {
        "FCFS": (
            "Requests are processed in their original "
            "queue order."
        ),

        "SSTF": (
            "The nearest pending request is selected "
            "at every step based on the current head position."
        ),

        "SCAN": (
            "The disk head moves toward the selected "
            "disk boundary before reversing direction."
        )
    }

    # 5. SSTF selection explanations
    selection_details = result.get(
        "selection_details", []
    )

    sstf_steps = []

    for detail in selection_details:

        sstf_steps.append({
            "current_head": detail["current_head"],
            "candidates": detail["candidates"],
            "selected": detail["selected"],
            "distance": detail["distance"]
        })

    # 6. SCAN explanation
    scan_details = result.get("scan_details", {})

    scan_events = scan_details.get("events", [])

    return {

        "algorithm": algorithm,

        "sequence": sequence,

        "rows": rows,

        "distances": distances,

        "equation": equation,

        "solution": solution,

        "total": total,

        "explanation": explanations.get(
            algorithm,
            "Disk scheduling computation."
        ),

        "sstf_steps": sstf_steps,

        "scan_details": scan_details,

        "scan_events": scan_events

    }
