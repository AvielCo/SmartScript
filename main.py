import argparse

from consts import *
from crop import main as crop_main
from evaluate_model import main as test_main
from network import main as train_main
from predict import predict_on_shape

parser = argparse.ArgumentParser(prog="smartscript",
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=description,
                                 epilog=epilog)
group = parser.add_mutually_exclusive_group()

group.add_argument("-t", "--train", type=str, metavar=("model", "times"), nargs=2,
                   help="train a model (new or exist)")
group.add_argument("-tt", "--test", type=str, metavar="model", nargs=1,
                   help="test a trained model")
group.add_argument("-p", "--predict", type=str,
                   help="predict an image on a trained model")
group.add_argument("-c", "--crop", type=str, metavar='times', nargs=1,
                   help="crop images into patches")
args = parser.parse_args()

try:
    if args.train:
        model_type = str(args.train[0]).lower()
        if model_type not in models:
            raise NameError(f"model must contain one of: {models}")
        times = int(args.train[1])
        if times <= 0:
            times = 1
        train_main(model_type, times)

    elif args.test:
        model_type = str(args.test[0]).lower()
        if model_type not in models:
            raise NameError(f"model must contain one of: {models}")
        test_main(model_type)

    elif args.predict:
        predict_on_shape()

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
