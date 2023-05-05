import csv
from shapely.affinity import translate
from shapely.geometry import Point
import matplotlib.pyplot as plt
from geopy import distance


# Source: https://realpython.com/python-csv/
def read_csv(filename):
    with open(filename, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = [row for row in csv_reader]
        return rows


def get_lon_lat_cities(cities_list):
    cities = {}
    for e in cities_list:
        cities[e["address"]] = {"geo": [float(e["geo_lat"]), float(e["geo_lon"])]}
    return cities


def get_most_populated_cities(num, cities_list):
    cities = {}
    for e in cities_list:
        cities[e["address"]] = [int(e["population"]), e]

    # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    sorted_cities = sorted(cities.items(), key=lambda x: x[1][0], reverse=True)
    filtered_cities = [e[1] for name, e in sorted_cities[:num]]
    return filtered_cities


def get_xy_coord(cities):
    new_cities = {}
    for city_name in cities.keys():
        city = cities[city_name]
        geo = city["geo"]
        xy = translate(Point(geo))
        y, x = xy.x, xy.y
        xy = {"xy": [x, y]}
        geo = {"geo": geo}
        new_cities[city_name] = {**xy, **geo}
    return new_cities


def get_distances(cities):
    new_cities = {}
    for city_name in cities.keys():
        city = cities[city_name]
        # m = city["xy"]
        m = city["geo"]
        distances = {}
        for city_name2 in cities.keys():
            city2 = cities[city_name2]
            # m2 = city2["xy"]
            m2 = city2["geo"]
            if city_name == city_name2:
                continue
            # city_distance = np.linalg.norm(np.array(m)-np.array(m2))
            city_distance = distance.distance(m, m2).km  # /1000

            distances[city_name2] = city_distance
        new_cities[city_name] = {**city, **{"distances": distances}}
    return new_cities


# https://stackoverflow.com/questions/14432557/matplotlib-scatter-plot-with-different-text-at-each-data-point
def plot_cities(fig, ax, cities):
    x, y, name = [], [], []
    for city_name in cities.keys():
        city = cities[city_name]
        xy = city["xy"]
        x.append(xy[0])
        y.append(xy[1])
        name.append(city_name)
    ax.scatter(x, y, marker="o", c="black")

    for i, txt in enumerate(name):
        ax.annotate(txt, (x[i], y[i]))
    return ax


def clear_plot(ax):
    ax.clear()


def plot_lines(fig, ax, cities, temp_perc):
    x, y, n = [], [], []

    for i in range(len(cities)):
        x.append(cities[i][0])
        y.append(cities[i][1])

    color = (temp_perc, 0, 1 - temp_perc)
    ax.plot(x, y, color=color)

    for i, txt in enumerate(n):
        ax.annotate(txt, (x[i], y[i]))
    return ax


def plot_animation(
    fig, ax, cities, lines, temp_perc=0.1, temp=0, title=None, pause=0.1
):
    clear_plot(ax)
    ax = plot_cities(fig, ax, cities)
    ax = plot_lines(fig, ax, lines, temp_perc)
    if title is not None:
        ax.set_title(title)
    plt.draw()
    # plt.savefig(f"results/gif_2/animation_{temp+1:.3f}.png")
    plt.pause(pause)


def to_list(cities):
    cities_list = []
    for city_name in cities.keys():
        city = cities[city_name]
        new_city = {**{"name": city_name}, **city}
        cities_list.append(new_city)
    return cities_list


def to_dict(cities_list):
    cities_dict = {}
    for i in range(len(cities_list)):
        cities_dict[cities_list[i]["name"]] = cities_list[i]
    return cities_dict


def generate_path(cities_list):
    xy = [cities_list[i]["xy"] for i in range(len(cities_list))]
    xy.append(cities_list[0]["xy"])
    return xy
