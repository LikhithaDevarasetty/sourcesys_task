from datetime import datetime

def show_current_time():
    try:
        now = datetime.now()
        print("Current date and time:", now)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    show_current_time()