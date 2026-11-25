"""
Задача 1. Реверс односвязного списка.

Теоретическая оценка сложности:
- Временная сложность: O(n), где n — количество узлов в списке (проходим по каждому узлу ровно один раз).
- Затраты по памяти: O(1) дополнительной памяти (используем только три указателя: prev, curr, next_node).
"""

from typing import Optional, List


class ListNode:
    def __init__(self, val: int = 0, next_node: Optional['ListNode'] = None):
        self.val = val
        self.next = next_node


def reverse_linked_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Разворачивает односвязный список и возвращает новую голову."""
    prev = None
    curr = head
    while curr is not None:
        next_node = curr.next  # Сохраняем ссылку на следующий узел
        curr.next = prev       # Переворачиваем указатель текущего узла назад
        prev = curr            # Сдвигаем prev вперед
        curr = next_node       # Сдвигаем curr вперед
    return prev


def build_linked_list(values: List[int]) -> Optional[ListNode]:
    """Вспомогательная функция для создания односвязного списка из массива."""
    if not values:
        return None
    head = ListNode(values[0])
    curr = head
    for val in values[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head


def linked_list_to_list(head: Optional[ListNode]) -> List[int]:
    """Вспомогательная функция для преобразования односвязного списка в обычный список."""
    res = []
    curr = head
    while curr is not None:
        res.append(curr.val)
        curr = curr.next
    return res


if __name__ == "__main__":
    # Пример из условия: 1, 2, 3, 4, 5 -> 5, 4, 3, 2, 1
    head = build_linked_list([1, 2, 3, 4, 5])
    reversed_head = reverse_linked_list(head)
    print("Исходный список:", [1, 2, 3, 4, 5])
    print("Результат:", linked_list_to_list(reversed_head))
