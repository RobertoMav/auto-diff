"""Calculator settings."""

SETTINGS: dict[int, int] = {5: 79, 4: 17, 3: 3, 2: 0, 1: 1}

total: int = 0
for val in SETTINGS.values():
    total += val

print(total)


def average_rating(ratings: dict[int, int]) -> float:
    """Calculate the average rating of the product."""
    total: float = 0.0
    for rate, share in ratings.items():
        total += rate * share / 100
        print(f"{total:.2f} in rate {rate} and share {share}")
    return total

pizza : str

pizza = 2
print(average_rating(SETTINGS))
