import threading
from contextlib import contextmanager
from typing import Generator, Any

from tqdm import tqdm


@contextmanager
def active_progress(*args: Any, **kwargs: Any) -> Generator[tqdm, None, None]:
    """A tqdm wrapper that keeps the timer ticking via a background thread."""
    with tqdm(*args, **kwargs) as bar:
        bar.refresh()
        stop_event = threading.Event()

        def keep_alive() -> None:
            while not stop_event.wait(0.5):
                bar.refresh()

        thread = threading.Thread(target=keep_alive, daemon=True)
        thread.start()

        try:
            yield bar
        finally:
            stop_event.set()
