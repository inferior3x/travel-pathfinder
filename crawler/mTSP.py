import random
from itertools import permutations
import json

def calculate_total_distance(route, distance_matrix):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i+1]]
    return total_distance

def divide_destinations(num_destinations, num_salesmen):
    destinations = list(range(1, num_destinations))
    random.shuffle(destinations)
    return [destinations[i::num_salesmen] for i in range(num_salesmen)]

def find_best_route_for_group(group, distance_matrix, start_point):
    all_routes = permutations(group)
    best_route = None
    min_distance = float('inf')
    for route in all_routes:
        full_route = [start_point] + list(route) + [start_point]
        total_distance = calculate_total_distance(full_route, distance_matrix)
        if total_distance < min_distance:
            min_distance = total_distance
            best_route = full_route
    return best_route, min_distance

def do_mTSP(json_string):
    json_object = json.loads(json_string)
    num_salesmen = int(json_object['n'])
    distance_matrix = json_object['matrix']
    groups = divide_destinations(len(distance_matrix), num_salesmen)

    # Find the best route for each group
    best_routes = []
    total_min_distance = 0
    for group in groups:
        route, distance = find_best_route_for_group(group, distance_matrix, 0)
        best_routes.append(route)
        total_min_distance += distance
    print(json.dumps(best_routes))
    return json.dumps(best_routes)
