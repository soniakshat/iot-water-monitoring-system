from queue import Queue, Empty

# Shared anomaly queue for communication between the analysis script and SSE view
anomaly_queue = Queue(maxsize=200)


def add_to_queue(item):
    """
    Add a new item to the anomaly queue.
    Ensures the queue only keeps the latest 200 items.
    """
    if anomaly_queue.full():
        anomaly_queue.get()  # Remove the oldest item
    anomaly_queue.put(item)


def get_next_item(timeout=10):
    """
    Retrieve the next item from the anomaly queue.
    Blocks for the specified timeout if the queue is empty.
    Returns None if no item is available.
    """
    try:
        return anomaly_queue.get(timeout=timeout)
    except Empty:
        return None


def get_all_items():
    """
    Retrieve all items in the queue as a list (empties the queue).
    """
    items = []
    while not anomaly_queue.empty():
        items.append(anomaly_queue.get())
    return items
