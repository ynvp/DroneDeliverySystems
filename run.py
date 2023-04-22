import implementation as ip
from python_tsp.exact import solve_tsp_dynamic_programming

warehouse_locations = [['W1', (34.98401, -101.30404)], ['W2', (34.99031, -101.23098)]]
customer_locations = [['C1', (34.99847, -101.2848)], ['C2', (34.97048, -101.28463)], [
    'C3', (34.96936, -101.25287)], ['C4', (35.00213, -101.25304)]]
charging_point_locations = [['CP1', (34.98694, -101.27501)]]

# Package weights at warehouse
products_weights = [['C1', 10], ['C2', 20], ['C3', 6], ['C4', 4]]

# Sort the products and weights in ascending order of weight
sorted_products_weights = sorted(products_weights, key=lambda x: x[1])


# Initialize the total weight and selected products list
total_weight = 0
selected_products = []

# Iterate over the sorted products and weights
for product, weight in sorted_products_weights:
    # Check if adding the weight of the product exceeds the maximum carrying weight
    if total_weight + weight > ip.MAX_CARRY_WEIGHT:
        # If it does, stop iterating
        break

    # If it doesn't, add the weight of the product to the total weight and append the product to the selected products list
    total_weight += weight
    selected_products.append(product)

print("Selected products: ", sorted(selected_products))

current_location = warehouse_locations[0]


# Added 1 for current location
# future: add CPs
dimension = 1+len(selected_products)

# Add CPs
locations_combined = [current_location[1]] + \
    [customer[1] for selected_customer in sorted(selected_products) for customer in customer_locations if selected_customer ==
        customer[0]]
print(locations_combined)
locations_combined_labels = [current_location[0]]+sorted(selected_products)

print(locations_combined_labels)
distance_matrix = ip.calculate_distance_matrix(dimension, locations_combined)

# Separate matrices for easier calculator
distance_between_warehouses = distance_matrix[0: len(
    warehouse_locations), 0:len(warehouse_locations)]
distance_between_customers = distance_matrix[len(warehouse_locations): len(warehouse_locations)+len(
    customer_locations), len(warehouse_locations): len(warehouse_locations)+len(
    customer_locations)]

# distance_between_charging_points =
print(distance_between_warehouses)
print(distance_between_customers)


distance_matrix[:, 0] = 0
permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
# print(locations_combined_labels[permutation], distance)
for i in permutation:
    print(locations_combined_labels[i]+"-->", end="")

print(distance)
# if(distance>ipMAX_TRAVEL_DISTANCE)
