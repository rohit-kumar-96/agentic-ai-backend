from datetime import datetime

def get_current_time(_=None):
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")