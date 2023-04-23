import numpy as np
import geopy.distance

# weight in pounds
MAX_CARRY_WEIGHT = 20
# distance in miles
MAX_TRAVEL_DISTANCE = 20



def calculate_distance_matrix(dimension, locations_combined):
    distance_matrix = np.zeros((dimension, dimension))
    print(distance_matrix)
    for i in range(1, dimension+1):
        for j in range(1, dimension+1):
            distance_matrix[i-1][j-1] = (geopy.distance.geodesic(
                locations_combined[i-1], locations_combined[j-1]).miles)
    print(distance_matrix)
    return distance_matrix


