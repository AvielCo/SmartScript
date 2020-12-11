import argparse

from consts import *
from crop import main as crop_main
from evaluate_model import main as test_main
from network import main as train_main


def train_model(model_type_, times_):
    if model_type_ == "main":
        train_main("input", times_)
    elif model_type_ == CURSIVE:
        train_main(f"input/{CURSIVE}", times_)
    elif model_type_ == SEMI_SQUARE:
        train_main(f"input/{SEMI_SQUARE}", times_)
    else:
        train_main(f"input/{SQUARE}", times_)


def test_model(path_to_model_, model_type_):
    if model_type_ == "main":
        test_main("input_test", path_to_model_, model_type_)
    elif model_type_ == CURSIVE:
        test_main(f"input_test/{CURSIVE}", path_to_model_, model_type_)
    elif model_type_ == SEMI_SQUARE:
        test_main(f"input_test/{SEMI_SQUARE}", path_to_model_, model_type_)
    else:
        test_main(f"input_test/{SQUARE}", path_to_model_, model_type_)


parser = argparse.ArgumentParser(prog="smartscript",
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=description,
                                 epilog=epilog)
group = parser.add_mutually_exclusive_group()

group.add_argument("-t", "--train", type=str, metavar=("model", "times"), nargs=2,
                   help="train a model (new or exist)")
group.add_argument("-tt", "--test", type=str, metavar=("path", "model"), nargs=2,
                   help="test a trained model")
group.add_argument("-p", "--predict", type=str, metavar=("path", "model"), nargs=2,
                   help="predict a image on a trained model")
group.add_argument("-c", "--crop", type=str, metavar='times', nargs=1,
                   help="crop images into patches")
args = parser.parse_args()

try:
    if args.train:
        model_type = str(args.train[0]).lower()
        if not models.__contains__(model_type):
            raise NameError(f"model must contain one of: {models}")
        times = int(args.train[1])
        if times <= 0:
            times = 1
        train_model(model_type, times)

    elif args.test:
        model_type = str(args.test[1]).lower()
        model_path = str(args.test[0]).lower()
        if not model_path.endswith(".h5"):
            raise TypeError("model path must be .h5 file")
        if not models.__contains__(model_type):
            raise NameError(f"model must contain one of: {models}")
        test_model(model_path, model_type)

    elif args.predict:
        model_type = str(args.predict[0]).lower()
        if not models.__contains__(model_type):
            raise NameError(f"model must contain one of: {models}")
        pass  # TODO: add predict to each model

    elif args.crop:
        del models
        times = int(args.crop[0])
        if times <= 0:
            times = 1
        for i in range(times):
            crop_main("input")

except NameError as e:
    print(e)
except TypeError as e:
    print(e)
