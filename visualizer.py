import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def swap(A, i, j):
    """Helper function to swap elements i and j of list A."""

    if i != j:
        A[i], A[j] = A[j], A[i]

def bubblesort(A):
    """In-place bubble sort."""

    if len(A) == 1:
        return

    swapped = True
    for i in range(len(A) - 1):
        if not swapped:
            break
        swapped = False
        for j in range(len(A) - 1 - i):
            if A[j] > A[j + 1]:
                swap(A, j, j + 1)
                swapped = True
            yield A

def insertionsort(A):
    """In-place insertion sort."""

    for i in range(1, len(A)):
        j = i
        while j > 0 and A[j] < A[j - 1]:
            swap(A, j, j - 1)
            j -= 1
            yield A

def mergesort(A, start, end):
    """Merge sort."""

    if end <= start:
        return

    mid = start + ((end - start + 1) // 2) - 1
    yield from mergesort(A, start, mid)
    yield from mergesort(A, mid + 1, end)
    yield from merge(A, start, mid, end)
    yield A

def merge(A, start, mid, end):
    """Helper function for merge sort."""
    
    merged = []
    leftIdx = start
    rightIdx = mid + 1

    while leftIdx <= mid and rightIdx <= end:
        if A[leftIdx] < A[rightIdx]:
            merged.append(A[leftIdx])
            leftIdx += 1
        else:
            merged.append(A[rightIdx])
            rightIdx += 1

    while leftIdx <= mid:
        merged.append(A[leftIdx])
        leftIdx += 1

    while rightIdx <= end:
        merged.append(A[rightIdx])
        rightIdx += 1

    for i, sorted_val in enumerate(merged):
        A[start + i] = sorted_val
        yield A

def quicksort(A, start, end):
    """In-place quicksort."""

    if start >= end:
        return

    pivot = A[end]
    pivotIdx = start

    for i in range(start, end):
        if A[i] < pivot:
            swap(A, i, pivotIdx)
            pivotIdx += 1
        yield A
    swap(A, end, pivotIdx)
    yield A

    yield from quicksort(A, start, pivotIdx - 1)
    yield from quicksort(A, pivotIdx + 1, end)

def selectionsort(A):
    """In-place selection sort."""
    if len(A) == 1:
        return

    for i in range(len(A)):
        # Find minimum unsorted value.
        minVal = A[i]
        minIdx = i
        for j in range(i, len(A)):
            if A[j] < minVal:
                minVal = A[j]
                minIdx = j
            yield A
        swap(A, i, minIdx)
        yield A

if __name__ == "__main__":
    # gets input to determine list size and sorting algo
    
    N = int(input("Enter number of integers: "))
    method_msg = "Enter sorting method:\n(b)ubble\n(i)nsertion\n(m)erge \
        \n(q)uick\n(s)election\n"
    method = input(method_msg)
    interval = input('(f)ast or (s)low? ')

    # Build and randomly shuffle list of integers.
    A = [x + 1 for x in range(N)]
    random.seed(time.time())
    random.shuffle(A)

    print(A)

    if method == "b":
        title = "Bubble sort"
        generator = bubblesort(A)
    elif method == "i":
        title = "Insertion sort"
        generator = insertionsort(A)
    elif method == "m":
        title = "Merge sort"
        generator = mergesort(A, 0, N - 1)
    elif method == "q":
        title = "Quicksort"
        generator = quicksort(A, 0, N - 1)
    else:
        title = "Selection sort"
        generator = selectionsort(A)

    fig, ax = plt.subplots()
    ax.set_title(title)

    bar_rects = ax.bar(range(len(A)), A)

    def update_fig(A, rects):
        for rect, val in zip(rects, A):
            rect.set_height(val)

    anim = animation.FuncAnimation(fig, func=update_fig,
        fargs=(bar_rects, ), frames=generator, interval=10 if interval == 's' else 1,
        repeat=False)

    plt.show()