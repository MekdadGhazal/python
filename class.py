import math


class NumberAnalyzer:
    
    def __init__(self, number):
        if not isinstance(number, int) :
            raise ValueError("Input must be an integer.")
        
        self.number = number


    def is_prime(self):
        if not isinstance(self.number, int) or self.number < 2:
            return False
        for i in range(2, int(math.sqrt(self.number)) + 1):
            if self.number % i == 0:
                return False
                
        return True
    

    def get_factorial(self):
        if not isinstance(self.number, int) or self.number < 0:
            return "Error: Factorial is only defined for non-negative integers."

        if self.number == 0:
            return 1

        result = 1
        for i in range(1, self.number + 1):
            result *= i
        return result
    

    def is_armstrong_number(self):
        if not isinstance(self.number, int) or self.number < 0:
            return "Error: Armstrong  Number is only defined for non-negative integers."

        if self.number == 0:
            return True
        
        number = str(self.number)
        lenght = len(number)

        result = 0
        for i in number:
            result += int(i) ** lenght

        if result == int(number) :
            return True
        return False
    


num_analyzer = NumberAnalyzer(153)

print(num_analyzer.is_prime()) 
print("-" * 20)

print(num_analyzer.is_armstrong_number()) 
print("-" * 20)

factorial_analyzer = NumberAnalyzer(5)
print(factorial_analyzer.get_factorial())