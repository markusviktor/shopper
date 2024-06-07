import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from typing import List, Tuple, Dict


# Define a function to input the shopping list
def input_shopping_list_from_csv(csv_file_path: str) -> Dict[str, str]:
    """
    Reads shopping items and their categories from a csv file.
    Returns a dictionary with items as keys and categories as values.
    """
    Shopping_data = pd.read_csv(csv_file_path)
    shopping_list = {item.lower(): category.lower() for item, category in
                     zip(Shopping_data['Item'], Shopping_data['Category'])}
    return shopping_list


# Define a function to sort the shopping list by category
def sort_shopping_list(shopping_list: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Sorts the shopping list by categories.
    Returns a dictionary with categories as keys and lists of items as values.
    """
    sorted_list = {}
    for item, category in shopping_list.items():
        if category not in sorted_list:
            sorted_list[category] = []
        sorted_list[category].append(item)
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
            polygon = patches.Polygon(zone, closed=True, fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(polygon)
            # Annotate category number near the polygon
            centroid_x = sum([point[0] for point in zone]) / len(zone)
            centroid_y = sum([point[1] for point in zone]) / len(zone)
            ax.text(centroid_x, centroid_y, str(number), fontsize=12, ha='center', color='blue')  # Change here

            # Add the centroid coordinates to the list
            centroids.append((centroid_x, centroid_y))

    # Draw lines between zone centroids
    xs, ys = zip(*centroids)  # This transforms list of (x, y) tuples into separate x and y coordinate lists
    ax.plot(xs, ys, 'r--')  # Draw lines in red dashed style

    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    # Example usage
    shopping_list = input_shopping_list_from_csv('shoppinglist.csv')
    sorted_list = sort_shopping_list(shopping_list)

    # https://www.image-map.net/
    category_zones = {
        'édesség': (1, [(30, 3422), (21, 2495), (1092, 2504), (1092, 2647), (291, 3448)]),
        'nemzetközi': (2, [(21, 2335), (1101, 2343), (1084, 2445), (30, 2453)]),
        'fűszer': (3, [(13, 2032), (1084, 2032), (1101, 2301), (30, 2301)]),
        'ital': (4, [(13, 1079), (30, 2015), (1076, 2006), (1455, 2166), (1599, 2150), (1590, 927), (21, 919)]),
        # 'textil': [(4154, 953), (5867, 953), (5867, 2183), (4154, 2183)],
    }
    # Define the category zones (example)

    # Path to the map image (example)
    map_image_path = 'dunakeszi_terkep.jpg'

    display_shopping_map(sorted_list, map_image_path, category_zones)
