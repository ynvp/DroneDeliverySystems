import math

# Function to calculate the distance between two points


def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)   

# Function to calculate the nearest charging point to a location


def find_nearest_charging_point(location, charging_points):
    min_distance = float('inf')
    nearest_charging_point = None

    for charging_point in charging_points:
        distance = calculate_distance(location, charging_point)
        if distance < min_distance:
            min_distance = distance
            nearest_charging_point = charging_point

    return nearest_charging_point

# Function to generate the optimal delivery route using Open TSP algorithm


def calculate_optimal_route(warehouses, charging_points, delivery_locations):
    # Your implementation of the Open TSP algorithm here
    # Return the optimal route as a list of locations

    # Example: Just returning a random order for demonstration purposes
    return warehouses + charging_points + delivery_locations

# Main function to handle package delivery


def deliver_packages(warehouses, charging_points, delivery_locations, package_weights, drone_max_distance, drone_max_charge):
    current_location = warehouses[0]
    current_charge = drone_max_charge

    route = calculate_optimal_route(
        warehouses, charging_points, delivery_locations)

    for location in route:
        if location in delivery_locations:
            package_index = delivery_locations.index(location)
            package_weight = package_weights[package_index]

            distance = calculate_distance(current_location, location)

            if distance > drone_max_distance:
                print(
                    f"Cannot deliver package to {location}. Distance exceeds drone's maximum travel distance.")
                continue

            if distance > current_charge:
                charging_point = find_nearest_charging_point(
                    current_location, charging_points)
                route.insert(route.index(location), charging_point)
                current_location = charging_point
                current_charge = drone_max_charge
                print(
                    f"Added charging point at {charging_point} before delivering to {location}.")

            current_location = location
            current_charge -= distance * package_weight
            print(
                f"Delivered package to {location}. Current charge: {current_charge}")

    print("Delivery completed. Returning to the starting point.")


# Example usage
warehouses = [(0, 0), (2, 2)]
charging_points = [(1, 1)]
delivery_locations = [(3, 3), (4, 4)]
package_weights = [1, 2]
drone_max_distance = 5
drone_max_charge = 10

deliver_packages(warehouses, charging_points, delivery_locations,
                 package_weights, drone_max_distance, drone_max_charge)
