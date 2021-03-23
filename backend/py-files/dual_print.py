import logging as log


def dual_print(massage, level="info"):
    if level == "info":
        log.info(massage)
        # print(massage)
    elif level == "error":
        log.error(massage)
        # print(massage)
