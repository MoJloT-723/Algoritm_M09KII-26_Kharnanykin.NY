"""
Задача 5. Определение дня с максимальным количеством посетителей в отеле.

Примечание по граничному условию:
В примере есть кортеж ("2024-09-15", "2024-09-15") — гость заехал и выехал в один и тот же день.
Чтобы учесть присутствие такого гостя в день заезда, при совпадении дат событие заезда (+1)
обрабатывается раньше события отъезда (-1) в пределах одного дня (то есть в день отъезда гость
еще числится в отеле до момента выезда).

Теоретическая оценка сложности:
- Временная сложность: O(m log m), где m — количество записей (посетителей). Сортировка 2m событий
  занимает O(m log m), линейный проход (метод сканирующей прямой) — O(m).
- Затраты по памяти: O(m) для хранения списка событий.
"""

from typing import List, Tuple


def find_peak_hotel_day(bookings: List[Tuple[str, str]]) -> Tuple[str, int]:
    """
    Принимает список кортежей (дата_заезда, дата_отъезда) в формате 'YYYY-MM-DD'.
    Возвращает кортеж (день_с_максимумом_гостей, количество_гостей).
    """
    if not bookings:
        return ("", 0)

    events: List[Tuple[str, int]] = []
    # Тип события: -1 для заезда (чтобы при сортировке заезд шел раньше выезда в ту же дату),
    # +1 для отъезда.
    for check_in, check_out in bookings:
        events.append((check_in, -1))
        events.append((check_out, 1))

    # Сортируем по дате лексикографически (формат ISO YYYY-MM-DD позволяет это делать напрямую),
    # а при равных датах сначала идут заезды (-1), затем выезды (+1).
    events.sort()

    current_guests = 0
    max_guests = 0
    peak_day = bookings[0][0]

    for date, event_type in events:
        if event_type == -1:
            current_guests += 1
            if current_guests > max_guests:
                max_guests = current_guests
                peak_day = date
        else:
            current_guests -= 1

    return peak_day, max_guests


if __name__ == "__main__":
    # Пример из условия
    sample_bookings = [
        ("2024-09-15", "2024-09-15"),
        ("2024-09-14", "2024-09-21"),
    ]
    day, count = find_peak_hotel_day(sample_bookings)
    print("Бронирования:", sample_bookings)
    print(f"День с максимальным числом посетителей: {day} (гостей: {count})")
