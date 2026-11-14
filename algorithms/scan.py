def scan(initial_head, requests, disk_min, disk_max, direction):

    current_head = initial_head
    direction = direction.lower().strip()

    # Validate direction
    if direction not in ["left", "right"]:
        raise ValueError("Invalid SCAN direction.")

    # Separate requests based on direction
    left = sorted(
        [r for r in requests if r < current_head],
        reverse=True
    )

    right = sorted(
        [r for r in requests if r >= current_head]
    )

    sequence = []
    events = []

    # Determine boundary and service order
    if direction == "right":

        boundary = disk_max

        sequence.extend(right)

        events.append({
            "type": "direction",
            "message": "Disk head initially moves RIGHT."
        })

        # Reach maximum boundary
        if current_head != disk_max:
            if not sequence or sequence[-1] != disk_max:
                sequence.append(disk_max)

        events.append({
            "type": "boundary",
            "position": disk_max,
            "message": f"Disk head reaches maximum boundary: {disk_max}."
        })

        events.append({
            "type": "reverse",
            "position": disk_max,
            "message": f"Disk head reverses direction at cylinder {disk_max}."
        })

        # Process requests on the left
        sequence.extend(left)

    else:

        boundary = disk_min

        sequence.extend(
            [r for r in requests if r <= current_head]
        )

        # Sort left side in descending order
        sequence = sorted(
            [r for r in requests if r <= current_head],
            reverse=True
        )

        events.append({
            "type": "direction",
            "message": "Disk head initially moves LEFT."
        })

        # Reach minimum boundary
        if current_head != disk_min:
            if not sequence or sequence[-1] != disk_min:
                sequence.append(disk_min)

        events.append({
            "type": "boundary",
            "position": disk_min,
            "message": f"Disk head reaches minimum boundary: {disk_min}."
        })

        events.append({
            "type": "reverse",
            "position": disk_min,
            "message": f"Disk head reverses direction at cylinder {disk_min}."
        })

        # Process requests on the right
        sequence.extend(right)

    # Calculate movement per step
    movements = []
    total_movement = 0

    for request in sequence:

        movement = abs(current_head - request)

        movements.append({
            "from": current_head,
            "to": request,
            "movement": movement
        })

        total_movement += movement
        current_head = request

    # SCAN explanation data
    scan_details = {
        "initial_direction": direction,
        "boundary": boundary,
        "reversed_at": boundary,
        "left_requests": left,
        "right_requests": right,
        "events": events
    }

    return {
        "algorithm": "SCAN",
        "sequence": sequence,
        "movements": movements,
        "total_movement": total_movement,
        "scan_details": scan_details
    }
