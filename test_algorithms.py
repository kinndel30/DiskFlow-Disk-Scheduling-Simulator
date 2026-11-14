
from algorithms.fcfs import fcfs
from algorithms.sstf import sstf
from algorithms.scan import scan
from utils.validation import parse_inputs


# Sample input
head, requests, minimum, maximum, direction = parse_inputs(
    "53",
    "98, 183, 37, 122, 14, 124, 65, 67",
    "0",
    "199",
    "right"
)

# Run algorithms
results = [
    fcfs(head, requests),
    sstf(head, requests),
    scan(head, requests, minimum, maximum, direction)
]

# Display results
for result in results:

    print("\nAlgorithm:", result["algorithm"])

    print("Sequence:", [head] + result["sequence"])

    print("Movement per step:")

    for step in result["movements"]:
        print(
            f"{step['from']} -> {step['to']} "
            f"= {step['movement']}"
        )

    print("Total:", result["total_movement"])


# Test invalid input
print("\nTesting invalid input:")

try:
    parse_inputs(
        "53",
        "98, 250, 37",
        "0",
        "199",
        "right"
    )

except ValueError as error:
    print("Validation successful:", error)
