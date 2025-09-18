def num():
    numb = int(input("please enter your number: "))

    if numb % 9 == 0:
        print("The number is divisible by 3 and 9.")
    elif numb % 3 == 0:
        print("The number is divisible by 3.")
    else:
        print("It is not divisible by any.")

num()
