"""
Задача 2. Поиск самых релевантных объектов с динамическим обновлением признаков.

Теоретическая оценка сложности:
- Инициализация: O(d * n + d log d), где d — число документов, n — число признаков.
- Запрос типа 1 (выдача топ-k): O(k), так как массив отсортирован по убыванию релевантности (k <= 10).
- Запрос типа 2 (обновление 1 признака): O(1) на пересчет релевантности + O(d) в худшем случае на сдвиг
  элемента в отсортированном списке (бинарный поиск позиции O(log d) + сдвиг в списке Python на C).
- Итоговая временная сложность: O(d * n + d log d + q * (d + k)), что при n * d <= 10^5 и q <= 10^5
  работает за доли секунды.
- Затраты по памяти: O(d * n) для хранения матрицы признаков и вспомогательных массивов позиций.
"""

from bisect import bisect_left
from typing import List, Tuple


def solve_ranking(
    n: int,
    a: List[int],
    d: int,
    features: List[List[int]],
    queries: List[Tuple[int, ...]]
) -> List[List[int]]:
    """
    Обрабатывает запросы ранжирования и обновления признаков.
    Индексация документов и признаков в запросах 1-based.
    """
    # Копируем признаки, чтобы не мутировать входные данные
    f = [row[:] for row in features]

    # Вычисляем начальную релевантность каждого документа: (-relevance, doc_id)
    # Отрицательная релевантность используется для сортировки по убыванию через bisect
    scores = [0] * d
    for doc_idx in range(d):
        scores[doc_idx] = sum(a[j] * f[doc_idx][j] for j in range(n))

    # Храним кортежи (-score, doc_id), отсортированные по возрастанию (то есть по убыванию score)
    ranked: List[Tuple[int, int]] = sorted((-scores[i], i) for i in range(d))

    # pos[doc_id] хранит текущую позицию документа doc_id в отсортированном списке ranked
    pos = [0] * d
    for idx, (_, doc_id) in enumerate(ranked):
        pos[doc_id] = idx

    results: List[List[int]] = []

    for query in queries:
        q_type = query[0]
        if q_type == 1:
            k = query[1]
            # Возвращаем 1-based номера топ-k документов
            top_k = [ranked[idx][1] + 1 for idx in range(k)]
            results.append(top_k)
        elif q_type == 2:
            _, doc_1based, feat_1based, new_val = query
            doc_id = doc_1based - 1
            feat_id = feat_1based - 1

            old_val = f[doc_id][feat_id]
            if old_val == new_val:
                continue

            # Пересчитываем релевантность за O(1)
            f[doc_id][feat_id] = new_val
            scores[doc_id] += a[feat_id] * (new_val - old_val)

            # Удаляем старую запись из отсортированного массива и вставляем новую
            old_idx = pos[doc_id]
            ranked.pop(old_idx)

            new_entry = (-scores[doc_id], doc_id)
            new_idx = bisect_left(ranked, new_entry)
            ranked.insert(new_idx, new_entry)

            # Обновляем индексы только на затронутом отрезке [min(old_idx, new_idx), max(old_idx, new_idx)]
            start = min(old_idx, new_idx)
            end = max(old_idx, new_idx)
            for idx in range(start, end + 1):
                pos[ranked[idx][1]] = idx

    return results


if __name__ == "__main__":
    # Пример из условия
    n = 2
    a = [1, 100]
    d = 10
    features = [
        [1, 2],
        [2, 1],
        [3, 1],
        [4, 1],
        [5, 1],
        [6, 1],
        [7, 1],
        [8, 1],
        [9, 1],
        [10, 1],
    ]
    queries = [
        (1, 2),
        (1, 10),
        (2, 4, 1, 1000),
        (1, 10),
    ]

    answers = solve_ranking(n, a, d, features, queries)
    for row in answers:
        print(*row)
