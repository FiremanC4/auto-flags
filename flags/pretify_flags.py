from pprint import pprint

def load():
    with open('flags.txt', 'r', encoding="utf-8") as f:
        fls = eval(f.read())
    return fls


def save(data):
    with open('flags.txt', 'w', encoding="utf-8") as f:
        pprint(data, stream=f)


if __name__ == "__main__":
    data = load()
    save(data)