Here's an algorithm that considers the given conditions of delivering packages using a drone with charging and maximum traveling distance. It incorporates the Open Traveling Salesman Problem (TSP) as the route calculator and handles insufficient charging for the next delivery by adding a charging point to the route:

    Initialize the drone's current location to the starting point (e.g., a warehouse).
    Calculate the optimal delivery route using the Open TSP algorithm. This algorithm takes into account the distances between the warehouses, charging points, and delivery locations, as well as the weights of the packages.
    Iterate through each delivery location in the calculated route:
    a. Check if the drone's current charging level is sufficient to reach the next delivery location. If it is, proceed to the next step.
    b. If the drone's current charging level is not sufficient, add a charging point to the route.
    c. Calculate the nearest charging point to the upcoming delivery location based on the current drone location.
    d. Update the route to include the charging point before the upcoming delivery location.
    e. Move the drone to the charging point and recharge until the battery is full.
    f. Update the drone's current location to the charging point.
    Once the route is finalized and charging points are added if necessary, start the package delivery process.
    Iterate through each delivery location in the route:
    a. Move the drone to the delivery location.
    b. Deliver the package at the current location.
    c. Update the drone's remaining battery based on the weight of the delivered package and the distance traveled.
    Repeat steps 5a-5c until all packages are delivered.
    Return to the starting point (e.g., warehouse) to complete the delivery process.

Please note that this algorithm assumes the availability of a suitable Open TSP implementation to calculate the optimal route. Additionally, it considers adding a charging point only when the drone's current charging level is insufficient for the next delivery location.