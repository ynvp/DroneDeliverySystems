import implementation as ip
from python_tsp.exact import solve_tsp_dynamic_programming


warehouse_locations = [
    ['Warehouse1', (40.7194939, - 74.0767397)]]
customer_locations = []
charging_point_locations = [['CP1', (34.98694, -101.27501)]]
products_weights = []
selected_products = []
selected_products_copy = []
final_path = []


def calculate_shortest_path(current_location):
    print(current_location)
    # Package weights at warehouse

    # Sort the products and weights in ascending order of weight
    sorted_products_weights = sorted(products_weights, key=lambda x: x[1])

    # Initialize the total weight and selected products list
    total_weight = 0
    # selected_products = []

    # Iterate over the sorted products and weights
    for product, weight in sorted_products_weights:
        # Check if adding the weight of the product exceeds the maximum carrying weight
        if total_weight + weight > ip.MAX_CARRY_WEIGHT:
            # If it does, stop iterating
            break

        # If it doesn't, add the weight of the product to the total weight and append the product to the selected products list
        total_weight += weight
        selected_products.append(product)
        selected_products_copy.append(product)

    print("Selected products: ", sorted(selected_products))
    print(selected_products_copy)
    # current_location = current_loc

    if not selected_products:
        print("Package weights exceed maximum load capacity of drone.")
    else:
        # Added 1 for current location
        # future: add CPs
        dimension = 1+len(selected_products)

        # Add CPs
        locations_combined = [current_location[1]] + \
            [customer[1] for selected_customer in sorted(selected_products) for customer in customer_locations if selected_customer ==
                customer[0]]
        print(locations_combined)
        locations_combined_labels = [
            current_location[0]]+sorted(selected_products)

        print(locations_combined_labels)
        distance_matrix = ip.calculate_distance_matrix(
            dimension, locations_combined)

        # Separate matrices for easier calculator
        distance_between_warehouses = distance_matrix[0: len(
            warehouse_locations), 0:len(warehouse_locations)]
        distance_between_customers = distance_matrix[len(warehouse_locations): len(warehouse_locations)+len(
            customer_locations), len(warehouse_locations): len(warehouse_locations)+len(
            customer_locations)]

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
