from rich.console import Console

console = Console()


def my_listener(event):
    """Handles scheduler events, displaying them in the console."""
    if event.exception:
        console.print(f'Job {event.job_id} failed', style="red")
    else:
        console.print(f'Job {event.job_id} completed', style="green")
