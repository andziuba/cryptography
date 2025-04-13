from bbs import bbs
from tests import single_bit_test, series_test, long_series_test, poker_test


def main():
    num_of_bits = 20000
    bits = bbs(num_of_bits)

    print("Single Bit Test:", "passed" if single_bit_test(bits) else "failed")
    print("Series Test:", "passed" if series_test(bits) else "failed")
    print("Long Series Test:", "passed" if long_series_test(bits) else "failed")
    print("Poker Test:", "passed" if poker_test(bits) else "failed")


if __name__ == "__main__":
    main()
