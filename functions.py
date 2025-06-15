

import math

# --------------------------------------------------------
def factorial(n):
    if not isinstance(n, int) or n < 0:
        return "Error: Factorial is only defined for non-negative integers."

    if n == 0:
        return 1

    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# --------------------------------------------------------
def fibonacci(n):
    if not isinstance(n, int) or n < 0:
        return "Error: Input must be a non-negative integer."
    
    a, b = 0, 1
    if n == 0:
        return a
    if n == 1:
        return b
        
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# --------------------------------------------------------
def prime(n):
    if not isinstance(n, int) or n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
            
    return True

# --------------------------------------------------------
def GCD(a, b):
    while b:
        a, b = b, a % b
    return a
    
# --------------------------------------------------------
def is_palindrome(text):

    ## A text with space and other marks
    # temp = list(map(lambda i : i if str(i).lower().isalnum() else '' ,text))
    # temp = [i for i in temp if i != '']

    # To remove space and ,
    text = str(text).lower()
    temp = []
    for i in text:
        if i.isalnum():
            temp.append(i)

    length = len(temp) // 2

    for i in range (0, length) :
        if temp[i] != temp[len(temp) -1 - i] :
            return False
    return True

# --------------------------------------------------------

def is_armstrong_number(number):
    if not isinstance(number, int) or number < 0:
        return "Error: Armstrong  Number is only defined for non-negative integers."

    if number == 0:
        return True
    
    number = str(number)
    lenght = len(number)

    result = 0
    for i in number:
        result += int(i) ** lenght

    if result == int(number) :
        return True
    return False

# --------------------------------------------------------

def is_anagram(a, b):

    temp1 = set(sorted(list(a)))
    temp2 = set(sorted(list(b)))

    if temp1 != temp2 :
        return False 
    return True


# --------------------------------------------------------
def reverse(n) :
    n = str(n)
    # return n[::-1]
    temp = list( n[i] for i in range(len(n) - 1, -1, -1))
    return( temp)

# --------------------------------------------------------
def missing_number(arr):

    n = len(arr) + 1
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(arr)
    return expected_sum - actual_sum


# --------------------------------------------------------
def count_vowels_consonants(text):

    vowels_set = 'aeiou'
    vowels_count = 0
    consonants_count = 0
    for char in text.lower():
        if char.isalpha(): # Only count letters
            if char in vowels_set:
                vowels_count += 1
            else:
                consonants_count += 1
    return vowels_count, consonants_count


# --------------------------------------------------------

def tower_of_hanoi(n, from_rod='A', to_rod='C', aux_rod='B'):
    if n == 1:
        print(f"Move disk 1 from rod {from_rod} to rod {to_rod}")
        return
    tower_of_hanoi(n - 1, from_rod, aux_rod, to_rod)
    print(f"Move disk {n} from rod {from_rod} to rod {to_rod}")
    tower_of_hanoi(n - 1, aux_rod, to_rod, from_rod)



# --------------------------------------------------------
# --- Main Interactive Menu ---
# --------------------------------------------------------
def main():
    
    while True:
        print("\n==============================================")
        print("     Select a Logic Function to Test")
        print("==============================================")
        print("1. Factorial")
        print("2. N-th Fibonacci Number")
        print("3. Prime Number Check")
        print("4. Greatest Common Divisor (GCD)")
        print("5. Palindrome Check")
        print("6. Armstrong Number Check")
        print("7. Anagram Check")
        print("8. Reverse String/Number")
        print("9. Find Missing Number in Array")
        print("10. Count Vowels and Consonants")
        print("11. Tower of Hanoi")
        print("0. Exit")
        print("----------------------------------------------")

        choice = input("Enter your choice (0-11): ")

        if choice == '1':
            try:
                num = int(input("Enter a non-negative integer: "))
                print(f"Result: {factorial(num)}")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        elif choice == '2':
            try:
                num = int(input("Enter the position (n) in the Fibonacci sequence: "))
                print(f"Result: The {num}-th Fibonacci number is {fibonacci(num)}")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        elif choice == '3':
            try:
                num = int(input("Enter an integer to check if it's prime: "))
                result = "is PRIME" if prime(num) else "is NOT prime"
                print(f"Result: {num} {result}.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        elif choice == '4':
            try:
                num1 = int(input("Enter the first number: "))
                num2 = int(input("Enter the second number: "))
                print(f"Result: The GCD of {num1} and {num2} is {GCD(num1, num2)}")
            except ValueError:
                print("Invalid input. Please enter integers.")

        elif choice == '5':
            text = input("Enter a word, number, or phrase to check: ")
            result = "IS a palindrome" if is_palindrome(text) else "is NOT a palindrome"
            print(f"Result: '{text}' {result}.")

        elif choice == '6':
            try:
                num = int(input("Enter a number to check if it's an Armstrong number: "))
                result = "IS an Armstrong number" if is_armstrong_number(num) else "is NOT an Armstrong number"
                print(f"Result: {num} {result}.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        elif choice == '7':
            str1 = input("Enter the first word/phrase: ")
            str2 = input("Enter the second word/phrase: ")
            result = "ARE anagrams" if is_anagram(str1, str2) else "are NOT anagrams"
            print(f"Result: '{str1}' and '{str2}' {result}.")

        elif choice == '8':
            data = input("Enter a string or number to reverse: ")
            print(f"Result: The reverse of '{data}' is '{reverse(data)}'")

        elif choice == '9':
            print("Enter a list of numbers separated by spaces (e.g., 0 1 3 4):")
            try:
                arr_str = input()
                arr = [int(i) for i in arr_str.split()]
                arr.sort() # The logic works best with a sorted list to understand the range
                print(f"Result: The missing number in {arr} is {missing_number(arr)}")
            except ValueError:
                print("Invalid input. Please enter numbers separated by spaces.")

        elif choice == '10':
            text = input("Enter a text to count its vowels and consonants: ")
            v, c = count_vowels_consonants(text)
            print(f"Result: Vowels = {v}, Consonants = {c}")

        elif choice == '11':
            try:
                num_disks = int(input("Enter the number of disks for Tower of Hanoi: "))
                if num_disks < 1:
                    print("Number of disks must be at least 1.")
                else:
                    print("--- Tower of Hanoi Solution ---")
                    tower_of_hanoi(num_disks)
            except ValueError:
                print("Invalid input. Please enter an integer.")

        elif choice == '0':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 0 and 11.")

if __name__ == "__main__":
    main()

