from crop import main as crop_main
from evaluate_model import main as test_main
from height import crop_images_height
from network import main as train_main

print("Welcome\nWhat would you like to do?\nChoose an option from the menu:")
first = "1"
second = "1"
while first != "1" or first != "2" or first != "3":
    first = input("\n\t1. train\n\t2. test\n\t3. predict\n\t4. change height\n\t5. crop images\noption: ")
    if first == "1" or first == "2" or first == "3" or first == "4" or first == "5":
        break
    print("An error has been occurred please choose again.")

if first == "1":
    print("Choose model to train: ")
    while second != "1" or second != "2" or second != "3" or second != "4":
        second = input("\n\t1. main\n\t2. cursive\n\t3. semi square\n\t4. square\noption: ")
        try:
            times = int(input(
                "How many times (50 epochs each) you want to train the model?[leave blank for amount of output folders]\n"
                "times(int) = "))
        except ValueError:
            times = 0
        print(f"training the model for {times} times")
        if second == "1":
            train_main("input", times)
            break
        elif second == "2":
            train_main("input/cursive", times)
            break
        elif second == "3":
            train_main("input/semi_square", times)
            break
        elif second == "4":
            train_main("input/square", times)
            break

        print("An error has been occurred please choose again.")

elif first == "2":
    print("Choose model to test: ")
    while second != "1" or second != "2" or second != "3" or second != "4":
        second = input("\n\t1. main\n\t2. cursive\n\t3. semi square\n\t4. square\noption: ")
        if second == "1":
            test_main("input_test")
            break
        elif second == "2":
            test_main("input_test/cursive")
            break
        elif second == "3":
            test_main("input_test/semi_square")
            break
        elif second == "4":
            test_main("input_test/square")
            break

        print("An error has been occurred please choose again.")

elif first == "3":
    print("Not available")

elif first == "4":
    while second != "1" or second != "2" or second != "3" or second != "4":
        second = input("Choose folder to change height (default is 4742 px):"
                       "\n\t1. input\n\t2. input_test\noption: ")
        if second == "1":
            crop_images_height("input")
            break
        elif second == "2":
            crop_images_height("input_test")
            break
        print("An error has been occurred please choose again.")

elif first == "5":
    times = int(input("How many times you want to crop to patches?[blank = 1]\n"
                      "times(int) = "))
    if not times:
        times = 1
    for _ in range(times):
        crop_main("input")
