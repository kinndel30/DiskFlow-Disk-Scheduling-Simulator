def parse_inputs(head, queue, minimum, maximum, direction):

    # Convert numerical inputs
    try:
        head = int(head)
        minimum = int(minimum)
        maximum = int(maximum)

    except (ValueError, TypeError):
        raise ValueError("Head and disk boundaries must be whole numbers.")

    # Validate disk boundaries
    if minimum >= maximum:
        raise ValueError(
            "Minimum cylinder must be less than maximum cylinder."
        )

    # Validate initial head position
    if not minimum <= head <= maximum:
        raise ValueError(
            "Initial head position must be within the disk range."
        )

    # Validate request queue
    if not isinstance(queue, str) or not queue.strip():
        raise ValueError("Request queue cannot be empty.")

    try:
        values = queue.split(",")

        if any(not value.strip() for value in values):
            raise ValueError("Remove empty entries from the request queue.")

        requests = [int(value.strip()) for value in values]

    except ValueError:
        raise ValueError(
            "Request queue must contain valid whole numbers separated by commas."
        )

    # Validate each request
    for request in requests:

        if not minimum <= request <= maximum:
            raise ValueError(
                f"Cylinder {request} is outside the disk range "
                f"({minimum} to {maximum})."
            )

    # Validate SCAN direction
    direction = direction.lower().strip()

    if direction not in ["left", "right"]:
        raise ValueError("SCAN direction must be Left or Right.")

    return head, requests, minimum, maximum, direction
