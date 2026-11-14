def fcfs(initial_head, requests):

    current_head = initial_head
    sequence = []
    movements = []
    total_movement = 0

    for request in requests:

        movement = abs(current_head - request)

        movements.append({
            "from": current_head,
            "to": request,
            "movement": movement
        })

        total_movement += movement
        sequence.append(request)

        current_head = request

    return {
        "algorithm": "FCFS",
        "sequence": sequence,
        "movements": movements,
        "total_movement": total_movement
    }
