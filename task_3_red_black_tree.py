"""
Задача 3. Реализация красно-черного дерева с балансировкой при вставке.

Теоретическая оценка сложности:
- Временная сложность:
  * Вставка элемента (insert): O(log n), где n — количество узлов в дереве.
  * Балансировка (_fix_insert): O(log n) перекрашиваний и не более 2 поворотов (O(1) на каждый поворот).
  * Поиск (search) и обход (inorder): O(log n) и O(n) соответственно.
- Затраты по памяти: O(n) для хранения узлов дерева и O(1) дополнительной памяти на операцию балансировки
  (итеративная реализация без рекурсии).
"""

from typing import Optional, List


RED = True
BLACK = False


class RBNode:
    def __init__(self, key: int, color: bool = RED, left=None, right=None, parent=None):
        self.key = key
        self.color = color
        self.left: Optional['RBNode'] = left
        self.right: Optional['RBNode'] = right
        self.parent: Optional['RBNode'] = parent


class RedBlackTree:
    def __init__(self):
        # Единый фиктивный листовой узел NIL (всегда черный)
        self.NIL = RBNode(key=0, color=BLACK)
        self.root: RBNode = self.NIL

    def _left_rotate(self, x: RBNode) -> None:
        """Левый поворот вокруг узла x за O(1)."""
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _right_rotate(self, y: RBNode) -> None:
        """Правый поворот вокруг узла y за O(1)."""
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x

        x.right = y
        y.parent = x

    def insert(self, key: int) -> None:
        """Вставляет новый ключ в дерево и запускает балансировку."""
        new_node = RBNode(key=key, color=RED, left=self.NIL, right=self.NIL)
        parent = None
        curr = self.root

        # Стандартная вставка в бинарное дерево поиска
        while curr != self.NIL:
            parent = curr
            if new_node.key < curr.key:
                curr = curr.left
            else:
                curr = curr.right

        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Восстанавливаем свойства красно-черного дерева
        self._fix_insert(new_node)

    def _fix_insert(self, z: RBNode) -> None:
        """Балансировка красно-черного дерева после вставки красного узла z."""
        while z.parent is not None and z.parent.color == RED:
            grandparent = z.parent.parent
            if z.parent == grandparent.left:
                uncle = grandparent.right
                # Случай 1: Дядя красный -> перекрашиваем отца, дядю и деда
                if uncle.color == RED:
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    grandparent.color = RED
                    z = grandparent
                else:
                    # Случай 2: Дядя черный, z — правый потомок -> левый поворот (сводим к случаю 3)
                    if z == z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    # Случай 3: Дядя черный, z — левый потомок -> перекрашивание и правый поворот
                    z.parent.color = BLACK
                    grandparent.color = RED
                    self._right_rotate(grandparent)
            else:
                # Симметричные случаи, когда отец — правый потомок деда
                uncle = grandparent.left
                if uncle.color == RED:
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    grandparent.color = RED
                    z = grandparent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = BLACK
                    grandparent.color = RED
                    self._left_rotate(grandparent)

        # Корень всегда должен быть черным
        self.root.color = BLACK

    def inorder_traversal(self) -> List[tuple]:
        """Возвращает список (ключ, цвет) в отсортированном порядке."""
        res = []

        def _dfs(node: RBNode):
            if node != self.NIL:
                _dfs(node.left)
                res.append((node.key, "RED" if node.color == RED else "BLACK"))
                _dfs(node.right)

        _dfs(self.root)
        return res


if __name__ == "__main__":
    rbt = RedBlackTree()
    for val in [10, 20, 30, 15, 25, 5, 1]:
        rbt.insert(val)
    print("In-order обход (ключ, цвет):", rbt.inorder_traversal())
    print("Корень:", rbt.root.key, "RED" if rbt.root.color == RED else "BLACK")
