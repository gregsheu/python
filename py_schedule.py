import schedule
import time

def print_me():
    print('Is schedule working?')

def main():
    schedule.every().day.at('20:00').do(print_me)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
