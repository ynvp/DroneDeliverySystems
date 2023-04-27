import math
import itertools


def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_weighted_tsp(warehouses, charging_points, delivery_locations):
    locations = warehouses + charging_points + delivery_locations
    num_locations = len(locations)

    # Calculate the distance matrix
    distance_matrix = [[0] * num_locations for _ in range(num_locations)]
    for i in range(num_locations):
        for j in range(num_locations):
            distance_matrix[i][j] = calculate_distance(
                locations[i], locations[j])

    # Initialize the dynamic programming table
    dp = {}
    for subset_size in range(1, num_locations):
        for subset in itertools.combinations(range(1, num_locations), subset_size):
            subset_mask = sum(1 << location for location in subset)
            dp[(subset_mask, subset[0])] = [float('inf')] * num_locations
            dp[(subset_mask, subset[0])][subset[0]
                                         ] = distance_matrix[0][subset[0]]

    # Fill in the dynamic programming table
    for subset_size in range(2, num_locations):
        for subset in itertools.combinations(range(1, num_locations), subset_size):
            for end in subset:
                subset_mask = sum(1 << location for location in subset)
                dp[(subset_mask, end)] = [float('inf')] * num_locations
                for prev_end in subset:
                    if prev_end == end:
                        continue
                    prev_mask = subset_mask ^ (1 << end)
                    min_distance = float('inf')
                    for prev_prev_end in subset:
                        if prev_prev_end == end or prev_prev_end == prev_end:
                            continue
                        min_distance = min(
                            min_distance,
                            dp[(prev_mask, prev_prev_end)][prev_end] +
                            distance_matrix[prev_end][end]
                        )
                    dp[(subset_mask, end)][end] = min_distance

    # Find the optimal route
    min_distance = float('inf')
    optimal_route = []
    subset_mask = (1 << num_locations) - 1
    for end in range(1, num_locations):
        distance = dp[(subset_mask, end)][end] + distance_matrix[end][0]
        if distance < min_distance:
            min_distance = distance
            optimal_route = [0, end]

    current_location = optimal_route[-1]
    subset_mask ^= 1 << current_location

    while subset_mask != 0:
        for next_location in range(1, num_locations):
            if next_location == current_location or (subset_mask >> next_location) & 1 == 0:
                continue
            if dp[(subset_mask, current_location)][current_location] + distance_matrix[current_location][next_location] == dp[(subset_mask, next_location)][next_location]:
                optimal_route.append(next_location)
                subset_mask ^= 1 << next_location
                current_location = next_location
                break

    return optimal_route, min_distance


# Example usage
warehouses = [(0, 0), (2, 2)]
charging_points = [(1, 1)]
delivery_locations = [(3, 3), (4, 4)]

optimal_route, min_distance = calculate_weighted_tsp(
    warehouses, charging_points, delivery_locations)

print("Optimal Route:", optimal_route)
print("Total Distance:", min_distance)
