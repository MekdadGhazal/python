
# alpha = ['a' ,'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

#  Using list of lists
def count_chars(text) :
    result = []
    for i in text:
        exist = False
        for j in range(len(result)) :
                if i == result[j][0]:
                    exist = True
                    break
        if not exist :
            result.append([i, 1])
        else:
            result[j][1] +=1
    return result


#  Using Dictionaries
def count_chars_dict(text):

    char_frequency = {}
    for char in text:
        if char in char_frequency:
            char_frequency[char] += 1
        else:
            char_frequency[char] = 1

    return char_frequency


# Pro using Class
from collections import Counter

def count_chars_professional(text):
    return Counter(text)


def find_first_non_repeating(text):
    result = count_chars_dict(text)
    for char in result :
        if result[char] == 1:
            return char
    return 'not found'


def binary_search(sorted_arr, target):

    left = 0
    right = len(sorted_arr) - 1

    while left <= right:
        mid = (left + right) //2

        if target < sorted_arr[mid] :
            right = mid -1

        elif target > sorted_arr[mid]:
            left = mid + 1

        else :
            return mid
        
    return -1



def is_balanced(text):
    closing_brackets = {')': '(', '}': '{', ']': '['}

    container = []
    for char in text :
        if char in "({[":
            container.append(char)
        elif char in closing_brackets:

            """
            if not stack or stack.pop() != closing_brackets[char]:
                return False
            
            """
            if len(container) == 0 :
                return False
            else:
                last_bracket = container.pop()
                if last_bracket != closing_brackets[char] :
                    return False
        else:
            continue
    return True

# print(is_balanced('ab(c)}'))

def main():
    
    while True:
        print("\n==============================================")
        print("     Select a Logic Function to Test")
        print("==============================================")
        print("1. Character Frequency")
        print("2. First Non-Repeating Character")
        print("3. Binary Search")
        print("4. Balanced Parentheses")
        print("0. Exit")
        print("----------------------------------------------")

        choice = input("Enter your choice (0-2): ")

        if choice == '1':
            try:
                print('There are 3 methods to calculate the Character Frequency')
                print('choose one below')
                print('1. Using list of lists\n2. Using dictionaries\n3. Using Collections Counter')
                method = int(input("Enter Choice : "))

                text = input("Enter the text: ")

                if method == 1 : 
                    result = count_chars(text)
                    print(f"Result: {result}")
                elif method == 2 :
                    result = count_chars_dict(text)
                    print(f"Result: {result}")
                elif method == 3:
                    result = count_chars_professional(text)
                    print(f"Result: {result}")
                else:
                    print("Invalid choice. Please enter a number between 0 and 3.")

                
            except ValueError:
                print("Invalid input. Please enter an integer.")

        elif choice == '2':
            try:
                text = input("Enter the text: ")
                print(find_first_non_repeating(text))
            except ValueError:
                print("Invalid input. Please enter an integer.")

        elif choice == '3':
            try:
                input_string = input("أدخل قائمة أرقام مفصولة بمسافة (مثال: 5 12 23 9): ")
                arr = [int(num) for num in input_string.split()]
                target = int(input("Enter target: "))
                
                print(binary_search(sorted(arr), target))
            except ValueError:
                print("Invalid input. Please enter an integer.")

        elif choice == '4':
            try:
                input_string = input('Enter your text to check your bracktes: ')
                
                print(is_balanced(input_string))
            except ValueError:
                print("Invalid input. Please enter an integer.")


        elif choice == '0':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 0 and 11.")



# if __name__ == '__main__' :
#     main()