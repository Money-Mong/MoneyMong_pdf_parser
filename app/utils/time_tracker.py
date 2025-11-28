import time
from contextlib import contextmanager
@contextmanager
def time_tracker(task):
    start = time.time()
    yield
    print(f"{task} completed in {time.time()-start:.2f}s")
