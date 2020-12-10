import argparse

from consts import description, epilog, models
from crop import main as crop_main
from evaluate_model import main as test_main
from network import main as train_main


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
        test_main("input_test", model_)
    elif model_ == "cursive":
        test_main("input_test/cursive", model_)
    elif model_ == "semi_square":
        test_main("input_test/semi_square", model_)
    else:
        test_main("input_test/square", model_)


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

try:
    if args.train:
        model = str(args.train[0]).lower()
        if not models.__contains__(model):
            raise NameError("model must contain one of: " + models)
        times = int(args.train[1])
        if times <= 0:
            raise ValueError
        train_model(model, times)

    elif args.test:
        model = str(args.test[0]).lower()
        if not models.__contains__(model):
            raise NameError("model must contain one of: " + models)
        test_model(model)

    elif args.predict:
        model = str(args.predict[0]).lower()
        if not models.__contains__(model):
            raise NameError("model must contain one of: " + models)
        pass  # TODO: add predict to each model

    elif args.crop:
        del models
        times = int(args.crop[0])
        if times <= 0:
            raise ValueError
        for i in range(times):
            crop_main("input")

except ValueError as e:
    times = 1
except NameError as e:
    print(e)
