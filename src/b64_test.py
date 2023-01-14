import timeit
import random
import string
from base64 import b64encode, b64decode
from Base64 import Base64

TEST_ITERATIONS = 100000


def gen_random_word(word_size: int) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for _ in range(word_size))


def verify_my_b64_encoding():
    for _ in range(TEST_ITERATIONS):
        word = gen_random_word(random.randint(0, 200))
        base64_norm = b64encode(word.encode()).decode()
        base64_own = Base64.b64encode(word.encode())
        if base64_norm != base64_own:
            print('Fehler')
            print(f'{base64_norm} != {base64_own}')
    print('Test OK')


def verify_my_b64_decoding():
    for _ in range(TEST_ITERATIONS):
        word = gen_random_word(random.randint(0, 100))
        base64_norm = b64decode(b64encode(word.encode())).decode()
        base64_own = Base64.b64decode(Base64.b64encode(word.encode()))
        if base64_norm != base64_own:
            print('Fehler')
            print(f'{base64_norm} != {base64_own}')
    print('Test OK')


def performance_test():
    my_setup = """from Base64 import Base64"""
    my_code = """Base64.b64encode("Lorem ipsum dolor sit amet".encode())"""
    print('My:\t\t{}'.format(timeit.timeit(setup=my_setup, stmt=my_code, number=TEST_ITERATIONS)))

    std_setup = """from base64 import b64encode"""
    std_code = """b64encode("Lorem ipsum dolor sit amet".encode())"""
    print('Std:\t{}'.format(timeit.timeit(setup=std_setup, stmt=std_code, number=TEST_ITERATIONS)))


def main():
    # verify_my_b64_encoding()
    performance_test()


if __name__ == '__main__':
    main()
