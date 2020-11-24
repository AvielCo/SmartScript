from evaluate_model import main as test_main
from height import crop_images
from network import main as train_main
import logging as log
from datetime import datetime

print("Welcome\nWhat would you like to do?\nChoose an option from the menu:")
first = "1"
second = "1"
while first != "1" or first != "2" or first != "3":
    first = input("\n\t1. train\n\t2. test\n\t3. predict\n\t4. change height\noption: ")
    if first == "1" or first == "2" or first == "3" or first == "4":
        break
    print("An error has been occurred please choose again.")

if first == "1":
    print("Choose model to train: ")
    while second != "1" or second != "2" or second != "3" or second != "4":
        second = input("\n\t1. main\n\t2. cursive\n\t3. semi square\n\t4. square\noption: ")
        if second == "1":
            train_main("input")
            break
        elif second == "2":
            train_main("input/cursive")
            break
        elif second == "3":
            train_main("input/semi_square")
            break
        elif second == "4":
            train_main("input/square")
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
    print("Choose folder to change height (default is 4742 px): ")
    while second != "1" or second != "2" or second != "3" or second != "4":
        second = input("\n\t1. input\n\t2. input_test\noption: ")
        if second == "1":
            crop_images("input")
            break
        elif second == "2":
            crop_images("input_test")
            break
        print("An error has been occurred please choose again.")
