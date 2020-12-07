import argparse

from crop import main as crop_main
from evaluate_model import main as test_main
from network import main as train_main
from consts import description, epilog, models

parser = argparse.ArgumentParser(prog="smartscript",
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=description,
                                 epilog=epilog)
group = parser.add_mutually_exclusive_group()
group.add_argument("-t", "--train", type=str, metavar=("model", "times"), nargs=2,
                   help="train a model (new or exist)")
group.add_argument("-tt", "--test", type=str, metavar='model', nargs=1,
                   help="test a trained model")
group.add_argument("-p", "--predict", type=str, metavar='model', nargs=1,
                   help="predict a image on a trained model")
group.add_argument("-c", "--crop", type=str, metavar='times', nargs=1,
                   help="crop images into patches")
args = parser.parse_args()


def train_model(model_, times_):
    if model_ == "main":
        train_main("input", times_)
    elif model_ == "cursive":
        train_main("input/cursive", times_)
    elif model_ == "semi_square":
        train_main("input/semi_square", times_)
    else:
        train_main("input/square", times_)


def test_model(model_):
    if model_ == "main":
        test_main("input", model_)
    elif model_ == "cursive":
        test_main("input/cursive", model_)
    elif model_ == "semi_square":
        test_main("input/semi_square", model_)
    else:
        test_main("input/square", model_)


try:
    if args.train:
        model = str(args.train[0]).lower()
        if not models.__contains__(model):
            raise NameError(f"model must contain one of: {models}")
        times = int(args.train[1])
        if times <= 0:
            raise ValueError
        train_model(model, times)

    elif args.test:
        model = str(args.test[0]).lower()
        if not models.__contains__(model):
            raise NameError(f"model must contain one of: {models}")
        test_model(model)

    elif args.predict:
        model = str(args.predict[0]).lower()
        if not models.__contains__(model):
            raise NameError(f"model must contain one of: {models}")
        pass  # TODO: add predict to each model

    elif args.crop:
        del models
        times = int(args.crop[0])
        if times <= 0:
            raise ValueError
        for i in range(times):
            crop_main("input")

except ValueError as e:
    print("times must be positive integer")
except NameError as e:
    print(e)

# print("Welcome\nWhat would you like to do?\nChoose an option from the menu:")
# first = "1"
# second = "1"
# while first != "1" or first != "2" or first != "3":
#     first = input("\n\t1. train\n\t2. test\n\t3. predict\n\t4. change height\n\t5. crop images\noption: ")
#     if first == "1" or first == "2" or first == "3" or first == "4" or first == "5":
#         break
#     print("An error has been occurred please choose again.")
#
# if first == "1":
#     print("Choose model to train: ")
#     while second != "1" or second != "2" or second != "3" or second != "4":
#         second = input("\n\t1. main\n\t2. cursive\n\t3. semi square\n\t4. square\noption: ")
#         try:
#             times = int(input(
#                 f"How many times ({EPOCHS} epochs each) you want to train the model?
#                 [leave blank for amount of output folders]\n"
#                 "times(int) = "))
#         except ValueError:
#             times = 0
#         print(f"training the model for {times} times")
#         if second == "1":
#             train_main("input", times)
#             break
#         elif second == "2":
#             train_main("input/cursive", times)
#             break
#         elif second == "3":
#             train_main("input/semi_square", times)
#             break
#         elif second == "4":
#             train_main("input/square", times)
#             break
#
#         print("An error has been occurred please choose again.")
#
# elif first == "2":
#     print("Choose model to test: ")
#     while second != "1" or second != "2" or second != "3" or second != "4":
#         second = input("\n\t1. main\n\t2. cursive\n\t3. semi square\n\t4. square\noption: ")
#         if second == "1":
#             test_main("input_test", "main")
#             break
#         elif second == "2":
#             test_main("input_test/cursive", "cursive")
#             break
#         elif second == "3":
#             test_main("input_test/semi_square", "semi_square")
#             break
#         elif second == "4":
#             test_main("input_test/square", "square")
#             break
#
#         print("An error has been occurred please choose again.")
#
# elif first == "3":
#     print("Not available")
#
# elif first == "4":
#     while second != "1" or second != "2" or second != "3" or second != "4":
#         second = input("Choose folder to change height (default is 4742 px):"
#                        "\n\t1. input\n\t2. input_test\noption: ")
#         if second == "1":
#             crop_images_height("input")
#             break
#         elif second == "2":
#             crop_images_height("input_test")
#             break
#         print("An error has been occurred please choose again.")
#
# elif first == "5":
#     times = int(input("How many times you want to crop to patches?[blank = 1]\n"
#                       "times(int) = "))
#     if not times:
#         times = 1
#     for _ in range(times):
#         crop_main("input")
