def sstf(initial_head, requests):

    current_head = initial_head
    pending = list(enumerate(requests))

    sequence = []
    movements = []
    selection_details = []
    total_movement = 0

    while pending:

        # Calculate distance of every pending request
        candidates = []

        for index, request in pending:

            distance = abs(current_head - request)

            candidates.append({
                "request": request,
                "distance": distance,
                "original_index": index
            })

        # Select nearest request
        nearest = min(
            candidates,
            key=lambda item: (
                item["distance"],
                item["original_index"]
            )
        )

        request = nearest["request"]
        movement = nearest["distance"]

        # Record selection explanation
        selection_details.append({
            "current_head": current_head,
            "candidates": candidates,
            "selected": request,
            "distance": movement
        })

        # Record movement
        movements.append({
            "from": current_head,
            "to": request,
            "movement": movement
        })

        total_movement += movement
        sequence.append(request)

        current_head = request

        # Remove selected request
        selected_index = nearest["original_index"]

        pending = [
            item for item in pending
            if item[0] != selected_index
        ]

    return {
        "algorithm": "SSTF",
        "sequence": sequence,
        "movements": movements,
        "selection_details": selection_details,
        "total_movement": total_movement
    }
