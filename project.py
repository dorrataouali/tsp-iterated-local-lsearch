import random 
import math 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
def distance(city1, city2):
    return math.sqrt((city2[0] - city1[0]) ** 2 + (city2[1] - city1[1]) ** 2)

def generate_cities(num_cities):
    return [(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_cities)]

def total_distance(cities, route):
    dist = 0
    for i in range(len(route)-1):
        dist += distance(cities[route[i]], cities[route[i+1]])
    dist += distance(cities[route[-1]], cities[route[0]])  
    return dist
def local_search(cities, route):
    best_route = route
    best_distance = total_distance(cities, route)
    
    for i in range(len(route)):
        for j in range(i+1, len(route)):
            new_route = route[:]
            new_route[i], new_route[j] = new_route[j], new_route[i] 
            new_distance = total_distance(cities, new_route)
            
            if new_distance < best_distance:
                best_route = new_route
                best_distance = new_distance
                print(f"Local Search - Swapped cities {route[i]} and {route[j]} to improve the distance")
    
    return best_route, best_distance

def perturbation(route):
    new_route = route[:]
    random.shuffle(new_route)
    return new_route
def iterated_local_search(cities, city_names, max_iterations=1000):
    route = list(range(len(cities)))
    random.shuffle(route)
    
    
    best_route = route
    best_distance = total_distance(cities, best_route)
    
    print(f"Initial Route: {best_route}, Distance: {best_distance}")
   
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title('TSP Solution with ILS')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    
    line, = ax.plot([], [], marker='o', linestyle='-', color='b')  
    scatter = ax.scatter([], [], color='red') 
    
    
    def plot_route(route, title):
        x, y = zip(*[cities[i] for i in route] + [cities[route[0]]])  
        line.set_data(x, y)
        scatter.set_offsets(list(zip(x, y)))  
        
       
        for i, city_idx in enumerate(route):
            ax.text(x[i], y[i], city_names[city_idx], fontsize=9, ha='right')
        
        ax.set_title(title)
        plt.draw()

   
    def update(frame):
        nonlocal best_route, best_distance
        
        if frame == 0:
            plot_route(best_route, "Initial Solution")
            return line, scatter
    
        new_route, new_distance = local_search(cities, best_route)
        
        if new_distance < best_distance:
            best_route = new_route
            best_distance = new_distance
            plot_route(best_route, f"Iteration {frame} - Local Search")
            print(f"Iteration {frame}: Local Search - New Best Distance: {best_distance}")
        
       
        else:
            best_route = perturbation(best_route)
            plot_route(best_route, f"Iteration {frame} - Perturbation")
            print(f"Iteration {frame}: Perturbation - New Route: {best_route}")
        
        return line, scatter

    ani = FuncAnimation(fig, update, frames=range(max_iterations), blit=False, interval=1000)
    plt.show()
    
    return best_route, best_distance


num_cities = 10
cities = generate_cities(num_cities)
city_names = [f'City {i}' for i in range(num_cities)]  
best_route, best_distance = iterated_local_search(cities, city_names)
print(f"Best Route Found: {best_route}, Distance: {best_distance}")
