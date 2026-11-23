import ast
import importlib
import inspect
import textwrap

import pytest

import assignment


@pytest.fixture
def q():
    return importlib.reload(assignment)


def calls_in(function):
    tree = ast.parse(textwrap.dedent(inspect.getsource(function)))
    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                names.append(node.func.id)
            if isinstance(node.func, ast.Attribute):
                names.append("." + node.func.attr)
    return names


def check_no_list_methods(function):
    for name in calls_in(function):
        if name in [".append", ".pop", ".insert", ".remove", ".extend", ".clear"]:
            pytest.fail(
                function.__name__ + "() uses " + name + "(). "
                "Move HeadPointer / TailPointer and use Queue[...] instead."
            )


def build(q, items, head, tail):
    q.Queue = []
    for item in items:
        q.Queue.append(item)
    while len(q.Queue) < 8:
        q.Queue.append(-1)
    q.HeadPointer = head
    q.TailPointer = tail


def test1_initial_queue(q):
    assert q.Queue == [-1, -1, -1, -1, -1, -1, -1, -1]
    assert q.HeadPointer == 0
    assert q.TailPointer == -1


def test1_is_empty(q):
    assert q.IsEmpty() == True
    build(q, [5], 0, 0)
    assert q.IsEmpty() == False
    build(q, [10, 20, 30], 1, 2)
    assert q.IsEmpty() == False
    build(q, [10, 20, 30], 3, 2)
    assert q.IsEmpty() == True


def test1_is_full(q):
    assert q.IsFull() == False
    build(q, [1, 2, 3, 4, 5, 6, 7], 0, 6)
    assert q.IsFull() == False
    build(q, [1, 2, 3, 4, 5, 6, 7, 8], 0, 7)
    assert q.IsFull() == True
    build(q, [1, 2, 3, 4, 5, 6, 7, 8], 5, 7)
    assert q.IsFull() == True


def test2_enqueue(q):
    assert q.Enqueue(15) == True
    assert q.TailPointer == 0
    assert q.Queue[0] == 15
    assert q.Enqueue(27) == True
    assert q.TailPointer == 1
    assert q.Queue[1] == 27
    assert q.HeadPointer == 0


def test2_enqueue_after_dequeue(q):
    build(q, [10, 20, 30], 2, 2)
    assert q.Enqueue(40) == True
    assert q.TailPointer == 3
    assert q.Queue[3] == 40
    assert q.HeadPointer == 2


def test2_enqueue_when_full(q):
    for x in range(8):
        assert q.Enqueue(x) == True
    assert q.Enqueue(99) == False
    assert q.TailPointer == 7
    assert q.Queue == [0, 1, 2, 3, 4, 5, 6, 7]


def test2_uses_tail_pointer(q):
    check_no_list_methods(q.Enqueue)
    for x in range(10):
        q.Enqueue(x)
    assert len(q.Queue) == 8
    assert q.TailPointer == 7


def test3_dequeue(q):
    build(q, [10, 20, 30], 0, 2)
    assert q.Dequeue() == 10
    assert q.HeadPointer == 1
    assert q.Dequeue() == 20
    assert q.HeadPointer == 2
    assert q.Dequeue() == 30
    assert q.HeadPointer == 3
    assert q.TailPointer == 2


def test3_dequeue_when_empty(q):
    assert q.Dequeue() == -1
    assert q.HeadPointer == 0
    assert q.TailPointer == -1
    build(q, [10, 20, 30], 3, 2)
    assert q.Dequeue() == -1
    assert q.HeadPointer == 3
    assert q.TailPointer == 2


def test3_uses_head_pointer(q):
    check_no_list_methods(q.Dequeue)
    build(q, [10, 20, 30, 40], 0, 3)
    q.Dequeue()
    q.Dequeue()
    assert len(q.Queue) == 8
    assert q.HeadPointer == 2
    assert q.Queue[2] == 30
    assert q.Queue[3] == 40


def test4_peek(q):
    assert q.Peek() == -1
    build(q, [10, 20, 30, 40], 1, 3)
    assert q.Peek() == 20
    assert q.Peek() == 20
    assert q.HeadPointer == 1
    assert q.TailPointer == 3
    build(q, [10, 20, 30, 40], 4, 3)
    assert q.Peek() == -1


def test4_show_queue(q):
    assert q.ShowQueue() == ""
    build(q, [10], 0, 0)
    assert q.ShowQueue() == "10"
    build(q, [10, 20, 30, 40], 0, 3)
    assert q.ShowQueue() == "10 20 30 40"


def test4_show_ignores_old_items(q):
    build(q, [10, 20, 30, 40, 50, 60], 2, 4)
    assert q.ShowQueue() == "30 40 50"
    assert q.HeadPointer == 2
    assert q.TailPointer == 4
    assert q.ShowQueue() == "30 40 50"
    build(q, [10, 20, 30], 3, 2)
    assert q.ShowQueue() == ""


@pytest.mark.parametrize("commands, expected", [
    [["join Bat", "join Anu", "serve", "join Saraa", "serve", "serve"], ["Bat", "Anu", "Saraa"]],
    [["join Bat", "join Anu", "join Tom", "serve"], ["Bat"]],
    [["serve", "join Bat"], []],
    [["join Anu", "serve", "serve", "serve", "join Bold", "serve"], ["Anu", "Bold"]],
    [[], []],
])
def test5_canteen(q, commands, expected):
    assert q.Canteen(commands) == expected


def test5_queue_full(q):
    commands = []
    for name in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
        commands.append("join " + name)
    for x in range(10):
        commands.append("serve")
    assert q.Canteen(commands) == ["A", "B", "C", "D", "E", "F", "G", "H"]
    commands.append("join Z")
    commands.append("serve")
    assert q.Canteen(commands) == ["A", "B", "C", "D", "E", "F", "G", "H"]


def test5_starts_with_empty_queue(q):
    q.Enqueue("X")
    q.Enqueue("Y")
    assert q.Canteen(["join Bat", "serve"]) == ["Bat"]
    assert q.Canteen(["join Anu", "serve", "serve"]) == ["Anu"]


def test5_uses_the_queue(q):
    names = calls_in(q.Canteen)
    assert "Enqueue" in names, "Canteen() must call Enqueue()."
    assert "Dequeue" in names, "Canteen() must call Dequeue()."
    assert q.Canteen(["join Bat", "join Anu", "serve"]) == ["Bat"]
