"""
Задача 6. Алгоритм Беллмана-Форда для произвольного взвешенного графа.

Теоретическая оценка сложности:
- Временная сложность: O(V * E), где V — количество вершин графа, E — количество ребер.
  Выполняется (V - 1) фаз релаксации по всем E ребрам + 1 проверка на наличие отрицательных циклов.
  (С оптимизацией раннего выхода при отсутствии изменений работает быстрее на разреженных графах).
- Затраты по памяти: O(V + E) для хранения списка ребер и массива кратчайших расстояний.
"""

from typing import List, Tuple, Optional


def bellman_ford(
    num_vertices: int,
    edges: List[Tuple[int, int, float]],
    start: int
) -> Tuple[Optional[List[float]], bool]:
    """
    Находит кратчайшие пути от вершины `start` до всех остальных вершин (0 .. num_vertices - 1).

    Параметры:
    - num_vertices: количество вершин в графе
    - edges: список ребер вида (u, v, weight)
    - start: стартовая вершина

    Возвращает:
    - (distances, has_negative_cycle):
      если обнаружен достижимый цикл отрицательного веса, возвращает (None, True);
      иначе возвращает (список расстояний, False).
    """
    INF = float('inf')
    dist = [INF] * num_vertices
    dist[start] = 0.0

    # Основной этап: V - 1 итераций релаксации всех ребер
    for _ in range(num_vertices - 1):
        updated = False
        for u, v, weight in edges:
            if dist[u] != INF and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                updated = True
        # Если за всю фазу ни одно расстояние не улучшилось, алгоритм можно завершить досрочно
        if not updated:
            break

    # Проверка на наличие достижимого цикла отрицательного веса (V-я итерация)
    for u, v, weight in edges:
        if dist[u] != INF and dist[u] + weight < dist[v]:
            return None, True

    return dist, False


if __name__ == "__main__":
    # Пример графа с отрицательными весами ребер (без отрицательного цикла)
    V = 5
    graph_edges = [
        (0, 1, -1),
        (0, 2, 4),
        (1, 2, 3),
        (1, 3, 2),
        (1, 4, 2),
        (3, 2, 5),
        (3, 1, 1),
        (4, 3, -3),
    ]
    distances, neg_cycle = bellman_ford(V, graph_edges, start=0)
    print("Отрицательный цикл обнаружен:", neg_cycle)
    print("Кратчайшие расстояния от вершины 0:", distances)
