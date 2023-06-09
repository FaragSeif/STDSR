import random
import math
from copy import deepcopy
from utils import generate_path, plot_animation, to_list


def compute_cost(cities):
    cost = 0
    # Calculate the distance starting from the city with index 0 to the next city in the index
    for i in range(1, len(cities)):
        city0 = cities[i - 1]
        city1 = cities[i]
        cost += city0["distances"][city1["name"]]
    # close the loop
    cost += cities[-1]["distances"][cities[0]["name"]]
    return cost


def swap(cities, i, j):
    tmp_city = deepcopy(cities[i])
    cities[i] = cities[j]
    cities[j] = tmp_city
    return cities


def generate_solution(cities, iter=3):
    new_cities = deepcopy(cities)
    for i in range(iter):
        # pick two cities in the path
        new_idx = random.sample(range(0, len(cities)), 2)
        # exchange their positions in the path
        new_cities = swap(new_cities, *new_idx)
    # return the new proposed path
    return new_cities


# Reference: https://gist.github.com/MNoorFawi/4dcf29d69e1708cd60405bd2f0f55700
def Annealing(
    cities,
    initial_temp=10000,
    cooling_rate=0.95,
    cooling_schedule="exp",  # or "lin" for linear schedule
    visualize=False,
    visualization_rate=0.01,
    fig=None,
    ax=None,
):
    cities_dict = cities
    cities = to_list(cities)
    temp = initial_temp
    costs = []
    temps = []
    new_solution_cost = 0
    current_solution = cities
    current_solution_cost = compute_cost(cities)
    new_solution = None
    while temp > 0.1:
        temp_perc = min((temp / initial_temp) + 0.4, 1)
        # Get new solution
        new_solution = generate_solution(current_solution)
        # Calculate the cost for the new solution
        new_solution_cost = compute_cost(new_solution)
        # Calculate p
        p = safe_exp((current_solution_cost - new_solution_cost) / temp)
        # if new solution is better or random less than p
        if new_solution_cost < current_solution_cost or random.uniform(0, 1) < p:
            current_solution = new_solution
            current_solution_cost = new_solution_cost
        if visualize:
            path = generate_path(current_solution)
            title = f"Temp={temp:.3f}, Cost={current_solution_cost:.3f}\nInitial temp={initial_temp}, Cooling rate={cooling_rate}, Cooling Schedule={cooling_schedule}"
            plot_animation(
                fig,
                ax,
                cities_dict,
                path,
                temp_perc,
                temp,
                pause=visualization_rate,
                title=title,
            )

        # print(current_solution_cost)
        if cooling_schedule == "exp":
            temp *= cooling_rate
        if cooling_schedule == "linear":
            temp -= initial_temp * (1 - cooling_rate)
        if cooling_schedule == "i_exp":
            temp -= 0.01 * ((initial_temp / cooling_rate) - temp)
        costs.append(current_solution_cost)
        temps.append(temp)
    return costs, temps, new_solution, new_solution_cost


def safe_exp(v):
    try:
        return math.exp(v)
    except:
        return 0
