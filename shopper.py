import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import logging
from PIL import Image
from typing import List, Tuple, Dict


# Define a function to input the shopping list
def input_shopping_list_from_csv(csv_file_path: str) -> Dict[str, str]:
    """
    Reads shopping items and their categories from a csv file.
    Returns a dictionary with items as keys and categories as values.
    """
    Shopping_data = pd.read_csv(csv_file_path)
    shopping_list = {
        item.lower().strip(): category.lower().strip()
        for item, category in zip(Shopping_data['Item'], Shopping_data['Category'])
    }
    return shopping_list


# Define a function to sort the shopping list by category
def sort_shopping_list(shopping_list: Dict[str, str], category_zones: Dict[str, Tuple[int, List[Tuple[int, int]]]]) -> \
        Dict[str, List[str]]:
    sorted_list = {}
    known_categories = set(category_zones.keys())
    for item, category in shopping_list.items():
        if category not in known_categories:
            logging.warning(f'Unknown category: {category}')
        if category not in sorted_list:
            sorted_list[category] = []
        sorted_list[category].append(item)

    sorted_categories = sorted(category_zones.keys(), key=lambda c: category_zones[c][0])
    sorted_list = {k: sorted_list[k] for k in sorted_categories if k in sorted_list}
    return sorted_list


# Define a function to display the shopping list on a map
def display_shopping_map(sorted_list: Dict[str, List[str]], map_image_path: str,
                         category_zones: Dict[str, Tuple[int, List[Tuple[int, int]]]]) -> None:
    """
    Displays the sorted shopping list on a map with category zones.
    Parameters:
    - sorted_list: Dictionary with categories as keys and lists of items as values.
    - map_image_path: Path to the map image file.
    - category_zones: Dictionary with categories as keys and tuples with number and list of (x, y) coordinates.
    """
    # Load map image
    map_image = Image.open(map_image_path)
    fig, ax = plt.subplots()
    ax.imshow(map_image)
    ax.axis('off')

    # List to hold centroids of each zone as we go through them
    centroids = []

    # Draw category zones
    # We are sorting categories based on zone numbers before drawing and annotation
    for category in sorted(sorted_list, key=lambda x: category_zones[x][0] if x in category_zones else float('inf')):
        if category in category_zones:
            (number, zone) = category_zones[category]
            polygon = patches.Polygon(zone, closed=True, fill=False, edgecolor='black', linewidth=2)
            ax.add_patch(polygon)
            # Annotate category number near the polygon
            centroid_x = sum([point[0] for point in zone]) / len(zone)
            centroid_y = sum([point[1] for point in zone]) / len(zone)
            # ax.text(centroid_x, centroid_y, str(number), fontsize=12, ha='center', color='blue')  # Change here

            # Add the centroid coordinates to the list
            centroids.append((centroid_x, centroid_y))

    # Draw arrows between zone centroids
    for i in range(len(centroids) - 1):
        x1, y1 = centroids[i]
        x2, y2 = centroids[i + 1]
        ax.arrow(x1, y1, x2 - x1, y2 - y1, color='red', linestyle='dashed', width=0.5)
    xs, ys = zip(*centroids)  # This transforms list of (x, y) tuples into separate x and y coordinate lists
    ax.plot(xs, ys, 'r--')  # Draw lines in red dashed style

    plt.axis('off')
    plt.savefig('output/shopping_map.png', bbox_inches='tight', dpi=300)
    # plt.show()


def export_shorted_list():
    # Write sorted list to file
    with open('output/sorted_list.txt', 'w') as f:
        first = True
        for key, values in sorted_list.items():
            if first:
                first = False
            else:
                f.write("\n")
            for value in values:
                f.write(f"{value} - {key}\n")


if __name__ == "__main__":
    # Example usage
    shopping_list = input_shopping_list_from_csv('input/shoppinglist.csv')

    # https://www.image-map.net/
    category_zones = {
        'édesség': (
            1,
            [(-2, 3414), (15, 2495), (1077, 2504), (1077, 2647), (1212, 2706), (1204, 3498), (689, 3515), (689, 3195),
             (1204, 2706), (1086, 2647), (276, 3431)]),
        'nemzetközi': (2, [(21, 2335), (1101, 2343), (1084, 2445), (30, 2453)]),
        'fűszer': (3, [(13, 2032), (1084, 2032), (1101, 2301), (30, 2301)]),
        'ital': (4, [(32, 1998), (23, 1079), (251, 1079), (268, 919), (1304, 927), (1305, 1028), (1617, 1028),
                     (1617, 2175), (1456, 2175), (268, 910), (251, 1062), (1077, 2006)]),
        'egészség': (5, [(1227, 3507), (1253, 2689), (1556, 2436), (1548, 3515)]),
        'tej': (6, [(1582, 2428), (1573, 3498), (2189, 3515), (2189, 2428)]),
        'sajt': (7, [(1628, 2178), (1628, 1032), (2008, 1023), (2008, 2170)]),
        'felvágott': (
            8, [(2016, 2161), (2016, 1040), (2201, 1040), (2640, 1428), (3044, 1040), (3305, 1276), (2387, 2178)]),
        'pékáru': (9, [(3154, 1049), (3575, 1032), (3567, 2161), (3348, 2178), (2876, 1748), (3356, 1251)]),
        'zöldség-gyümölcs': (10, [(2235, 2440), (2218, 3510), (2985, 3519), (2985, 2912), (3145, 2886), (3154, 2414)]),
        'illatszer': (11, [(3617, 1049), (3617, 2178), (4115, 2195), (4115, 1040)]),
        'baba': (12, [(3600, 2406), (3584, 3519), (3828, 3502), (3845, 2431)]),
        'vegyi': (13, [(3862, 2431), (3862, 3485), (4738, 3510), (4738, 2423)]),
        'textil': (14, [(4154, 953), (5867, 953), (5867, 2183), (4154, 2183)]),
        'háztartás': (15, [(4787, 2402), (5948, 2402), (5948, 3522), (4759, 3508)]),
        'cd-könyv': (16, [(5878, 932), (6241, 918), (6241, 2192), (5850, 2178)]),
        'játék': (17, [(6241, 932), (6521, 946), (6521, 2164), (6241, 2178)]),
        'háztasrtási gép': (18, [(5989, 2402), (6940, 2444), (6926, 3508), (5975, 3508)]),
        'szezon': (19, [(6547, 2166), (6547, 927), (7432, 927), (7432, 2175), (7651, 2150), (8612, 2158), (8620, 2655),
                        (7634, 2647), (7651, 2158), (7440, 2166), (7432, 2411), (7440, 3507), (6951, 3498),
                        (6968, 2428), (7440, 2411), (7449, 2175)]),
        'állatfelszerelés': (20, [(7639, -6), (7625, 918), (8618, 904), (8604, 8)]),
        'autó-barkács': (21, [(7651, 1138), (8595, 1138), (8603, 2116), (7643, 2107)]),
        'sport': (22, [(7651, 2681), (8603, 2672), (8603, 2773), (7651, 2782)]),
        'iroda': (23, [(7659, 2832), (8603, 2841), (8603, 3507), (7643, 3524)]),
        'kert': (24, [(8654, 540), (9539, 540), (9539, 2723), (8646, 2731)]),
        'mirelit': (99, [(3187, 2414), (3187, 2929), (3011, 2945), (3002, 3485), (3558, 3493), (3558, 2423)]),

    }

    sorted_list = sort_shopping_list(shopping_list, category_zones)

    export_shorted_list()

    # Path to the map image (example)
    map_image_path = 'data/dunakeszi_terkep.jpg'

    display_shopping_map(sorted_list, map_image_path, category_zones)
