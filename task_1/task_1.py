import networkx as nx
from collections import deque
import pandas as pd
import matplotlib.pyplot as plt

# --- Побудова графа ---
G = nx.DiGraph()

# Додавання ребер з пропускними здатностями
edges = [
    ("Термінал 1", "Склад 1", 25),
    ("Термінал 1", "Склад 2", 20),
    ("Термінал 1", "Склад 3", 15),
    ("Термінал 2", "Склад 3", 15),
    ("Термінал 2", "Склад 4", 30),
    ("Термінал 2", "Склад 2", 10),
    ("Склад 1", "Магазин 1", 15),
    ("Склад 1", "Магазин 2", 10),
    ("Склад 1", "Магазин 3", 20),
    ("Склад 2", "Магазин 4", 15),
    ("Склад 2", "Магазин 5", 10),
    ("Склад 2", "Магазин 6", 25),
    ("Склад 3", "Магазин 7", 20),
    ("Склад 3", "Магазин 8", 15),
    ("Склад 3", "Магазин 9", 10),
    ("Склад 4", "Магазин 10", 20),
    ("Склад 4", "Магазин 11", 10),
    ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5),
    ("Склад 4", "Магазин 14", 10),
]

# Візуалізація графа
G.add_weighted_edges_from(edges, weight="capacity")
pos = nx.spring_layout(G, seed=11)
plt.figure(figsize=(15, 10))
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=1500,
    node_color="skyblue",
    font_size=6,
    font_weight="bold",
    arrows=True,
    arrowsize=10,
)
plt.title("Логістична мережа")
plt.show()


# --- Алгоритм Едмондса-Карпа ---
def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    """
    Виконуємо BFS для знаходження шляху з позитивною пропускною здатністю.
    parent[] використовується для відтворення шляху від source до sink.
    """
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()
        for neighbor in range(len(capacity_matrix)):
            # Перевіряємо, чи ребро має вільну пропускну здатність
            if (
                not visited[neighbor]
                and capacity_matrix[current_node][neighbor]
                - flow_matrix[current_node][neighbor]
                > 0
            ):
                parent[neighbor] = current_node  # зберігаємо батьківський вузол
                visited[neighbor] = True
                if neighbor == sink:
                    return True  # якщо знайдено шлях до магазину
                queue.append(neighbor)
    return False  # якщо шлях не знайдено


def edmonds_karp(capacity_matrix, source, sink):
    """
    Основна функція алгоритму Едмондса-Карпа.
    max_flow - сумарний максимальний потік від джерела до стоку.
    flow_matrix відстежує фактичні потоки між усіма вузлами.
    """
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    parent = [-1] * num_nodes
    max_flow = 0

    # Повторюємо, поки BFS знаходить шлях з позитивною пропускною здатністю
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        path_flow = float("inf")
        current_node = sink

        # 1-й крок: знаходимо обмежуюче ребро (мінімальна пропускна здатність на шляху)
        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(
                path_flow,
                capacity_matrix[previous_node][current_node]
                - flow_matrix[previous_node][current_node],
            )
            current_node = previous_node

        # 2-й крок: оновлюємо потоки на кожному ребрі шляху
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node

        # 3-й крок: збільшуємо сумарний максимальний потік
        max_flow += path_flow

        # Коментар: на кожній ітерації ми знаходимо один шлях, додаємо його обмежений потік
        # і повторюємо пошук, поки не використаємо всі можливі шляхи.

    return max_flow, flow_matrix


# --- Підготовка матриці пропускних спроможностей ---
nodes = list(G.nodes)
node_index = {node: i for i, node in enumerate(nodes)}
size = len(nodes)
capacity_matrix = [[0] * size for _ in range(size)]

# Заповнюємо матрицю capacity, враховуючи пропускну здатність ребер
for u, v, data in G.edges(data=True):
    capacity_matrix[node_index[u]][node_index[v]] = G[u][v]["capacity"]

# --- Обчислення максимальних потоків для кожного терміналу ---
results = []

for terminal in ["Термінал 1", "Термінал 2"]:
    for shop in [n for n in nodes if n.startswith("Магазин")]:
        # Кожен запуск дає максимальний потік від терміналу до конкретного магазину
        max_flow, flow_matrix = edmonds_karp(
            capacity_matrix, node_index[terminal], node_index[shop]
        )
        if max_flow > 0:
            results.append(
                {
                    "Термінал": terminal,
                    "Магазин": shop,
                    "Фактичний Потік (одиниць)": max_flow,
                }
            )

# --- Вивід результатів у таблицю ---
df = pd.DataFrame(results)
print(df.sort_values(["Термінал", "Магазин"]))