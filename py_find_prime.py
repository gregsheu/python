import math
def check_prime(n):
    if n <= 1:
        return False
    elif n == 2:
        return True
    elif n > 2 and n%2 == 0:
        return False
    else:
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n%i == 0:
                return False
    return True

def main():
    print(f"Is 2 prime: {check_prime(2)}")
    print(f"Is 3 prime: {check_prime(3)}")
    print(f"Is 27 prime: {check_prime(27)}")
    print(f"Is 57 prime: {check_prime(57)}")
    print(f"Is 53 prime: {check_prime(53)}")

if __name__ == '__main__':
    main()
