def sort(lst):
    n = len(lst)
    for i in range(n - 1):

        min_index = i
        for j in range(i + 1, n):
            if lst[j] < lst[min_index]:
                min_index = j

        lst[i], lst[min_index] = lst[min_index], lst[i]

        print(f"Step {i+1}: {lst[:i+1]} | Remaining: {lst[i+1:]}")
    return lst


try:

    user_input = input("Enter a list of numbers separated by spaces: ")
    numbers = list(map(float, user_input.split())) 
    if not numbers:  
        raise ValueError("The list is empty!")

    print("\n--- Start sorting ---")
    sorted_list = sort(numbers)
    print("\nFinal sorted list: ", sorted_list)

except ValueError as e:
    print("Invalid input", e)
except Exception as e:
    print("Unexpected error", e)
