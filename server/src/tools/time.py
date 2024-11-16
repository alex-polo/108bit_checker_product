from datetime import datetime


def get_current_time() -> str:
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M')
    return formatted_time