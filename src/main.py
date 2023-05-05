from utils import *
import matplotlib.pyplot as plt
from SA import Annealing
import argparse

import timeit

start = timeit.default_timer()

parser = argparse.ArgumentParser()
# TODO: Force different seed from argparse if it exists against the one in the json file
parser.add_argument("--cooling", type=float, default=0.99)
parser.add_argument("--schedule", default="i_exp")
parser.add_argument("--temp", type=int, default=100)
args = parser.parse_args()


visualize = True  # False
visualization_rate = 0.01

initial_temp = args.temp  # 500
cooling_rate = args.cooling  # 0.999
cooling_schedule = args.schedule  # linear

city_csv_file_path = "cities/city.csv"
csv_data = read_csv(city_csv_file_path)
cities = get_most_populated_cities(30, csv_data)
cities = get_distances(get_xy_coord(get_lon_lat_cities(cities)))

try:
    fig, ax = None, None
    if visualize:
        plt.ion()
        plt.show(block=True)
        fig, ax = plt.subplots()

    start = timeit.default_timer()
    costs, temps, new_solution, new_solution_cost = Annealing(
        cities,
        initial_temp,
        cooling_rate,
        cooling_schedule=cooling_schedule,
        visualize=visualize,
        visualization_rate=visualization_rate,
        fig=fig,
        ax=ax,
    )
    stop = timeit.default_timer()

    print("Time: ", stop - start)
    print(f"Final Cost: {costs[-1]}")
    print(f"Number of steps: {len(costs)}")

    path = generate_path(new_solution)
    title = f"Final solution, Cost={costs[-1]:.3f}\nInitial temp={initial_temp}, Cooling rate={cooling_rate}, Cooling Schedule={cooling_schedule}"
    plot_animation(fig, ax, cities, path, pause=5, title=title)
    # plt.savefig(f"results/output_{initial_temp}_{cooling_rate}.png")
    clear_plot(ax)
    plt.plot(
        [i for i in range(len(costs))], [c / costs[0] for c in costs], label="Cost"
    )
    plt.legend()
    plt.plot(
        [i for i in range(len(temps))], [t / temps[0] for t in temps], label="Temp"
    )
    plt.legend()
    plt.title(
        f"Initial temp={initial_temp}, Cooling rate={cooling_rate}, Cooling Schedule={cooling_schedule}"
    )
    plt.draw()
    # plt.savefig(f"results/comparison/cost_temp_{costs[-1]}_{initial_temp}.png")
    plt.pause(5)

except KeyboardInterrupt:
    print("Exiting...")
    if visualize:
        plt.ioff()
    exit()
