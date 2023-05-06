import implementation as ip
from python_tsp.exact import solve_tsp_dynamic_programming, solve_tsp_brute_force
import geopy.distance
import time


warehouses = {}
delivery_locations = {}
charging_points = {}
package_weights = {}
selected_packages = []
selected_packages_copy = []
final_path = []
distance_matrix = []


def calculate_shortest_path(current_location):
    # Clearing selected packages lists every run to not accumulate data in current list
    selected_packages.clear()
    selected_packages_copy.clear()

    # Sort the products and weights in ascending order of weight
    sorted_package_weights = sorted(package_weights.items(), key=lambda x: x[1])

    # Initialize the total weight and selected products list
    total_weight = 0

    # Iterate over the sorted products and weights
    for product, weight in sorted_package_weights:
        # Check if adding the weight of the product exceeds the maximum carrying weight
        if total_weight + weight > ip.MAX_CARRY_WEIGHT:
            # If it does, stop iterating
            break

        # If it doesn't, add the weight of the product to the total weight and append the product to the selected products list
        total_weight += weight
        selected_packages.append(product)
        selected_packages_copy.append(product)

    print("Selected products: ", sorted(selected_packages))
    print(selected_packages_copy)

    if not selected_packages:
        print("Package weights exceed maximum load capacity of drone.")
    else:
        # Added 1 for current warehouse location
        # future: add CPs
        dimension = 1 + len(selected_packages)

        # Add CPs
        locations_combined = [current_location[1]] + [
            delivery_locations[customer]
            for selected_customer in sorted(selected_packages)
            for customer in delivery_locations.keys()
            if selected_customer == customer
        ]
        print(locations_combined)
        locations_combined_labels = [current_location[0]] + sorted(selected_packages)

        print(locations_combined_labels)
        distance_matrix = ip.calculate_distance_matrix(dimension, locations_combined)

        # Separate matrices for easier calculator
        distance_between_warehouses = distance_matrix[
            0 : len(warehouses), 0 : len(warehouses)
        ]
        distance_between_customers = distance_matrix[
            len(warehouses) : len(warehouses) + len(delivery_locations),
            len(warehouses) : len(warehouses) + len(delivery_locations),
        ]

        # distance_between_charging_points =
        print("distance_between_warehouses: ", distance_between_warehouses)
        print("distance_between_customers: ", distance_between_customers)

        distance_matrix[:, 0] = 0
        start = time.time()
        path, distance = solve_tsp_dynamic_programming(distance_matrix)
        end = time.time()
        print("TSP time: ", end - start)
        start = time.time()
        path1, distance1 = solve_tsp_brute_force(distance_matrix)
        end = time.time()
        print("Greedy time: ", end - start)
        print(path1, distance1)

        concat_path = ""
        for i in path:
            concat_path += locations_combined_labels[i] + "-->"
        print(concat_path[:-3])

        path_labels = [locations_combined_labels[i] for i in path]
        print("Total_distance: ", distance)
        return path_labels


def deliver_packages(starting_warehouse_location):
    drone_max_charge = 100
    drone_max_distance = 20

    current_charge = drone_max_charge

    # Calculating route
    route = calculate_shortest_path(starting_warehouse_location)

    current_location = starting_warehouse_location[1]

    for location in route:
        if location in delivery_locations.keys():
            distance = calculate_distance(
                current_location, delivery_locations[location]
            )

            # print(distance, current_charge)
            if distance * (drone_max_charge / drone_max_distance) > current_charge:
                charging_point = find_nearest_charging_point(
                    current_location,
                    delivery_locations[location],
                    charging_points,
                    current_charge,
                )
                if charging_point == None:
                    print("Route does not contain enough charging points to map. ")
                    break
                else:
                    route.insert(route.index(location), charging_point)
                    current_location = charging_points[charging_point]
                    current_charge = drone_max_charge
                    print(
                        f"Added charging point at {charging_point} before delivering to {location}."
                    )
            else:
                current_location = delivery_locations[location]
                print(
                    current_charge, distance * (drone_max_charge / drone_max_distance)
                )
                current_charge -= distance * (drone_max_charge / drone_max_distance)
                print(
                    f"Delivered package to {location}. Current charge: {current_charge}"
                )
    # Searching for nearest warehouse location to reach
    route = find_nearest_warehouse(
        route, current_location, drone_max_charge, drone_max_distance, current_charge
    )
    current_charge = 100
    if route != None:
        print(f"Delivery completed. Returning to the {route[-1]} point.")
        return route
    else:
        return None


def find_nearest_charging_point(
    current_location, upcoming_location, charging_points, current_charge
):
    min_distance = float("inf")
    nearest_charging_point = None
    for charging_point in list(charging_points.keys()):
        distance1 = calculate_distance(
            current_location, charging_points[charging_point]
        )
        distance2 = calculate_distance(
            upcoming_location, charging_points[charging_point]
        )
        # print(charging_point, ' distance1: ', distance1)

        if distance1 <= current_charge / 5 and min_distance > distance2:
            nearest_charging_point = charging_point
            min_distance = distance2

    return nearest_charging_point


def find_nearest_warehouse(
    route, current_location, drone_max_charge, drone_max_distance, current_charge
):
    min_distance = float("inf")
    selected_warehouse = ""
    warehouse_nearest_charging_point = None
    for warehouse in warehouses:
        distance = calculate_distance(warehouses[warehouse], current_location)
        if distance < min_distance:
            min_distance = distance
            selected_warehouse = warehouse
            print(selected_warehouse)
    if (
        min_distance * (drone_max_charge / drone_max_distance)
        > current_charge + (drone_max_charge / drone_max_distance) * 5
    ):
        print(current_charge)
        warehouse_nearest_charging_point = find_nearest_charging_point(
            current_location,
            warehouses[selected_warehouse],
            charging_points,
            current_charge,
        )
        if warehouse_nearest_charging_point == None:
            print("Route does not contain enough charging points to map. ")
            return None
        if warehouse_nearest_charging_point != None:
            route.append(warehouse_nearest_charging_point)
            route.append(selected_warehouse)
            print(route)
            return route
    else:
        route.append(selected_warehouse)
        print(route)
        return route


def calculate_distance(location1, location2):
    return geopy.distance.geodesic(location1, location2).miles


def clear_current_data():
    warehouses.clear()
    delivery_locations.clear()
    charging_points.clear()
    package_weights.clear()
    selected_packages.clear()
    selected_packages_copy.clear()
    final_path.clear()
    distance_matrix.clear()
