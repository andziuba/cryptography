def single_bit_test(bits):
    ones = sum(bits)
    return 9725 < ones < 10275


def series_test(bits):
    series_zero = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    series_one = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    current_series_length = 1
    current_bit = bits[0]

    for i in range(1, len(bits)):
        if bits[i] == current_bit:
            current_series_length += 1
        else:
            if current_bit == 0:
                series_zero[min(6, current_series_length)] += 1
            else:
                series_one[min(6, current_series_length)] += 1
            current_series_length = 1
            current_bit = bits[i]

    if current_bit == 0:
        series_zero[min(6, current_series_length)] += 1
    else:
        series_one[min(6, current_series_length)] += 1

    zero_passed = (2315 <= series_zero[1] <= 2685 and
                   1114 <= series_zero[2] <= 1386 and
                   527 <= series_zero[3] <= 723 and
                   240 <= series_zero[4] <= 384 and
                   103 <= series_zero[5] <= 209 and
                   103 <= series_zero[6] <= 209)

    one_passed = (2315 <= series_one[1] <= 2685 and
                  1114 <= series_one[2] <= 1386 and
                  527 <= series_one[3] <= 723 and
                  240 <= series_one[4] <= 384 and
                  103 <= series_one[5] <= 209 and
                  103 <= series_one[6] <= 209)

    return zero_passed and one_passed


def long_series_test(bits):
    max_series_length = 0
    current_series_length = 1

    for i in range(1, len(bits)):
        if bits[i] == bits[i - 1]:
            current_series_length += 1
        else:
            current_series_length = 1

        max_series_length = max(max_series_length, current_series_length)

    return max_series_length <= 26


def poker_test(bits):
    if len(bits) % 4 != 0:
        print("Nieodpowiednia długość ciągu")
        return False

    segments = [bits[i:i+4] for i in range(0, len(bits), 4)]  # podział na 4-bitowe bloki

    counts = {}
    for segment in segments:
        pattern = tuple(segment)
        counts[pattern] = counts.get(pattern, 0) + 1

    poker_value = (16 / 5000) * sum(count ** 2 for count in counts.values()) - 5000
    return 2.16 <= poker_value <= 46.17
