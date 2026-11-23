# Linear Queue 

Read the Abstract Data Types lecture (Queue section) before you start.
https://drive.google.com/file/d/1jXGQdSvuUYjGXl-PUuHMUzKWEBGQoARL/view?usp=sharing

A queue is **First In, First Out (FIFO)** — like a line at the canteen. People
join at the **back** and are served from the **front**.

**Rules for this assignment**

- The queue is a global array called `Queue` with **8** elements.
- `HeadPointer` is the index of the **front** item (the next one to leave).
- `TailPointer` is the index of the **last** item that joined.
- Do **not** use `.append()` or `.pop()` inside `Enqueue()` and `Dequeue()`.
  Move the pointers yourself and use `Queue[...]`.
- Functions **return** their answer — do not print.
- Every function that changes `Queue`, `HeadPointer` or `TailPointer` needs:
  `global Queue, HeadPointer, TailPointer`

**How a linear queue works**

    Start (empty):
      Index:   0    1    2    3    4    5    6    7
      Queue:  -1   -1   -1   -1   -1   -1   -1   -1
      HeadPointer = 0     TailPointer = -1

    After Enqueue(10), Enqueue(20), Enqueue(30):
      Queue:  10   20   30   -1   -1   -1   -1   -1
               ↑         ↑
             Head      Tail          HeadPointer = 0     TailPointer = 2

    After Dequeue()  → returns 10:
      Queue:  10   20   30   -1   -1   -1   -1   -1
                    ↑    ↑
                  Head  Tail         HeadPointer = 1     TailPointer = 2

- `10` is still in the array, but it is **not** in the queue any more — only
  the items from `HeadPointer` to `TailPointer` are in the queue.
- The queue is **empty** when `HeadPointer > TailPointer`.
- The queue is **full** when `TailPointer == 7` (the end of the array).

**Note:** this is a **linear** queue. Once `TailPointer` reaches 7, nothing else
can join — even if items have left from the front. The **circular** queue
fixes this problem (next lesson).

---

## Exercise 1

**Problem:**

Set up an **empty** queue.

- `Queue` → a global array of 8 elements, all `-1`
- `HeadPointer` → `0`
- `TailPointer` → `-1`

Then write two functions:

`IsEmpty()`

- Return `True` if the queue has no items (`HeadPointer > TailPointer`), otherwise `False`

`IsFull()`

- Return `True` if `TailPointer` is at the last index (`7`), otherwise `False`

**Example:**

    Input:                 Output:
      print(Queue)           [-1, -1, -1, -1, -1, -1, -1, -1]
      print(IsEmpty())       True
      print(IsFull())        False

---

## Exercise 2

**Problem:**

`Enqueue(Item)`

Add `Item` to the **back** of the queue.

1. If the queue is full, return `False`
2. Add 1 to `TailPointer`
3. Store `Item` at `Queue[TailPointer]`
4. Return `True`

**Example:**

    Input:
      print(Enqueue(15))
      print(Enqueue(27))
      print(Queue)
      print(HeadPointer, TailPointer)

    Output:
      True
      True
      [15, 27, -1, -1, -1, -1, -1, -1]
      0 1

When the queue already has 8 items, `Enqueue(99)` returns `False` and nothing changes.

---

## Exercise 3

**Problem:**

`Dequeue()`

Remove the item at the **front** of the queue and return it.

1. If the queue is empty, return `-1`
2. Save the item at `Queue[HeadPointer]` — **before** you move the pointer!
3. Add 1 to `HeadPointer`
4. Return the saved item

**Example:**

    Input:
      Enqueue(10)
      Enqueue(20)
      Enqueue(30)
      print(Dequeue())
      print(Dequeue())
      print(HeadPointer, TailPointer)

    Output:
      10
      20
      2 2

---

## Exercise 4

**Problem:**

`Peek()`

- Return the item at the **front** of the queue **without** removing it
- Return `-1` if the queue is empty
- Do **not** change `HeadPointer` or `TailPointer`

`ShowQueue()`

- Return a string of the items in the queue, from **front to back**,
  separated by one space
- Return `""` if the queue is empty
- Only show items from `HeadPointer` to `TailPointer` — ignore old items

**Example:**

    Input:
      Enqueue(10)
      Enqueue(20)
      Enqueue(30)
      Enqueue(40)
      Dequeue()
      print(Peek())
      print(ShowQueue())

    Output:
      20
      20 30 40

*Hint:* if your answer is `10 20 30 40` you started from index 0. Start from `HeadPointer`.

---

## Exercise 5

**Problem:**

`Canteen(Commands)`

The school canteen uses your queue. `Commands` is a list of strings:

- `"join <name>"` → that student joins the queue (use `Enqueue`)
- `"serve"` → the student at the front is served (use `Dequeue`)

Return a **list** of the names that were served, in order.

1. Start with an **empty** queue: `HeadPointer = 0` and `TailPointer = -1`
2. For each command:
    - `"serve"` → `Dequeue()`. If it returns `-1`, nobody was in the queue,
      so do **not** add anything to the list
    - otherwise → split the command and `Enqueue()` the name
3. Return the list of served names

If the queue is full, the student cannot join — `Enqueue()` returns `False`, just ignore them.

*Hint:* `"join Bat".split(" ")` gives `["join", "Bat"]` — the name is at index 1.

**Example:**

    Input:
      print(Canteen(["join Bat", "join Anu", "serve", "join Saraa", "serve", "serve"]))
      print(Canteen(["serve", "join Bat"]))

    Output:
      ['Bat', 'Anu', 'Saraa']
      []

