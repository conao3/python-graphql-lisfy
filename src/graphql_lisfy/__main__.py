from . import rep


def main():
    while True:
        try:
            text = input('graphql-lisfy> ')
        except (EOFError, KeyboardInterrupt):
            break

        if (val := rep.rep(text)) is not None:
            print(val)
