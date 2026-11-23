# You can remove 'pass' if you written code in the function
# Do NOT use .append() or .pop() inside Enqueue() and Dequeue() - move the pointers yourself.
from encodings.quopri_codec import quopri_encode

# Exercise 1
Queue = [-1,-1,-1,-1,-1,-1]
HeadPointer = 0
TailPointer = -1
# Write code here to fill Queue with 8 elements, all -1


def IsEmpty():
    if HeadPointer>TailPointer:
        return True
    else:
        return False

def IsFull():
    if TailPointer==7:
        return True
    else:
        return False

# Exercise 2
def Enqueue(Item):
    global TailPointer,Queue,HeadPointer
    if TailPointer==7:
        return False
    TailPointer=TailPointer+1
    Queue[TailPointer]=Item
    return True

# Exercise 3
def Dequeue():
    global TailPointer, Queue, HeadPointer, Item
    if HeadPointer>TailPointer:
        return -1
    Item=Queue[HeadPointer]
    HeadPointer=HeadPointer+1
    return Item


# Exercise 4
def Peek():
    if HeadPointer>TailPointer:
        return -1
    return Queue[HeadPointer]
def ShowQueue():
    if HeadPointer>TailPointer:
        return ""
    result=""
    for i in range(HeadPointer,TailPointer+1):
        if result!="":
            result=result+" "
        result=result+str(Queue[i])
    return result



# Exercise 5
def Canteen(Commands):
    # Write your code here
    pass
