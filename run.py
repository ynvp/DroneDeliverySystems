import implementation as ip
from python_tsp.exact import solve_tsp_dynamic_programming
import geopy.distance

# 'Warehouse1', (40.7194939, - 74.0767397)]
#  Charging Point [['CP1', (34.98694, -101.27501)]]
warehouses = {}
delivery_locations = {}
charging_points = {}
package_weights = {}
selected_packages = []
selected_packages_copy = []
final_path = []
distance_matrix = []


def calculate_shortest_path(current_location):
    print(current_location)
    # Package weights at warehouse

    # Sort the products and weights in ascending order of weight
    sorted_package_weights = sorted(
        package_weights.items(), key=lambda x: x[1])

    # Initialize the total weight and selected products list
    total_weight = 0
    # selected_packages = []

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
        dimension = 1+len(selected_packages)

        # Add CPs
        locations_combined = [current_location[1]] + \
            [delivery_locations[customer] for selected_customer in
             sorted(selected_packages) for customer in delivery_locations.keys() if selected_customer ==
                customer]
        print(locations_combined)
        locations_combined_labels = [
            current_location[0]]+sorted(selected_packages)

        print(locations_combined_labels)
        distance_matrix = ip.calculate_distance_matrix(
            dimension, locations_combined)

        # Separate matrices for easier calculator
        distance_between_warehouses = distance_matrix[0: len(
            warehouses), 0:len(warehouses)]
        distance_between_customers = distance_matrix[len(warehouses): len(warehouses)+len(
            delivery_locations), len(warehouses): len(warehouses)+len(
            delivery_locations)]

        # distance_between_charging_points =
        print('distance_between_warehouses: ', distance_between_warehouses)
        print('distance_between_customers: ', distance_between_customers)

        distance_matrix[:, 0] = 0
        path, distance = solve_tsp_dynamic_programming(distance_matrix)

        for i in path:
            print(locations_combined_labels[i]+"-->", end="")

        path_labels = [locations_combined_labels[i] for i in path]
        print(distance)
        return path_labels


def deliver_packages(starting_warehouse_location):
    drone_max_charge = 80
    drone_max_distance = 20
    current_charge = drone_max_charge

    route = calculate_shortest_path(
        starting_warehouse_location)
    print(route)
    current_location = starting_warehouse_location[1]
    print(current_location)

    for location in route:
        print(location)
        if location in delivery_locations.keys():
            print(location)
            package_index = location
            package_weight = package_weights[location]
            distance = calculate_distance(
                current_location, delivery_locations[location])
            print(distance)
            if distance > drone_max_distance:
                print(
                    f"Cannot deliver package to {location}. Distance exceeds drone's maximum travel distance.")
                continue
            print(distance, current_charge)
            if distance * package_weight > current_charge:
                charging_point = find_nearest_charging_point(
                    current_location, delivery_locations[location], charging_points)
                # # Check if drone able to reach the charging point with current charge
                # if cp_distance * package_weight > current_charge:

                route.insert(route.index(location),
                             charging_point)
                current_location = charging_points[charging_point]
                current_charge = drone_max_charge
                print(
                    f"Added charging point at {charging_point} before delivering to {location}.")

            current_location = delivery_locations[location]
            current_charge -= distance * package_weight
            print(
                f"Delivered package to {location}. Current charge: {current_charge}")

    print("Delivery completed. Returning to the starting point.")
    return route


def find_nearest_charging_point(current_location, upcoming_location, charging_points):
    min_distance = float('inf')
    nearest_charging_point = None
    for charging_point in list(charging_points.keys()):
        distance = calculate_distance(
            current_location, charging_points[charging_point])+calculate_distance(upcoming_location, charging_points[charging_point])

        if distance < min_distance and calculate_distance(
                current_location, charging_points[charging_point]) < 10:
            print(charging_point)
            min_distance = distance
            nearest_charging_point = charging_point

    return nearest_charging_point


def calculate_distance(location1, location2):
    return (geopy.distance.geodesic(location1, location2).miles)
