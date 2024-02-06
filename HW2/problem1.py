import math
import timeit
import numpy as np


def naive():
    n = 0
    running_sum = 0
    sum_sq = 0
    with open('measurement_data_uint8.bin', 'rb') as f:
        while True:
            data_byte = f.read(1)
            if data_byte:
                n += 1
                #num = int(data_byte.hex(), 16)
                num = int.from_bytes(data_byte, byteorder='big')
                running_sum += num
                sum_sq += num ** 2
            else:
                break
    # print(n)
    print("Mean is: ", running_sum / n)  # 133.70021891

    # print(sum_sq)
    variance = (sum_sq - (running_sum * running_sum) / n) / (n - 1)
    print("Variance is: ", variance)

    print("Standard deviation is: ", math.sqrt(variance))  # Standard Deviation
    # SD = 1.3677611877759654


def welford():
    mean = 0.0
    sum_of_squares = 0.0
    counter = 1
    with open('measurement_data_uint8.bin', 'rb') as f:
        while True:
            data_byte = f.read(1)
            if data_byte:
                #num = int(data_byte.hex(), 16)
                num = int.from_bytes(data_byte, byteorder='big')
                old_mean = mean
                mean = mean + (num - mean) / counter
                sum_of_squares = sum_of_squares + (num - mean) * (num - old_mean)
                counter += 1
            else:
                break
    print("Mean is: ", mean)
    welford_var = sum_of_squares / (100000000 - 1)
    print("Variance is: ", welford_var)
    print("Standard deviation is:", math.sqrt(welford_var))  # 1.3677611877762328


def onepass():
    old_mean = 0.0
    new_mean = 0.0
    old_central_sum = 0.0
    new_central_sum = 0.0
    n = 0

    with open('measurement_data_uint8.bin', 'rb') as f:
        while True:
            data_byte = f.read(1)
            if data_byte:
                n += 1
                #num = int(data_byte.hex(), 16)
                num = int.from_bytes(data_byte, byteorder='big')
                delta = num - old_mean
                new_mean = old_mean + delta / n
                old_mean = new_mean
                new_central_sum = old_central_sum + ((delta ** 2) * (n - 1)) / n
                old_central_sum = new_central_sum
            else:
                break

    print("Mean is: ", new_mean)
    print("Variance as per formula defined in the paper is: ", new_central_sum / n)
    print("Standard deviation is: ", math.sqrt(new_central_sum / n))


def histogram():
    histogram = np.zeros(256, dtype='int64')
    compute_array = np.arange(0, 256, 1, dtype='float64')

    with open('measurement_data_uint8.bin', 'rb') as f:
        while True:
            data_byte = f.read(1)
            if data_byte:
                #num = int(data_byte.hex(), 16)
                num = int.from_bytes(data_byte, byteorder='big')
                histogram[num] += 1
            else:
                break

    # As per the given formula for mean, and variance is calculated by extending that formula
    numerator = np.sum(np.multiply(histogram, compute_array))
    denominator = np.sum(histogram)
    mean = numerator / denominator
    print("Mean is: ", mean)

    compute_array = (compute_array - mean) ** 2
    var_num = np.sum(np.multiply(histogram, compute_array))
    print("Variance is: ", var_num / denominator)

    sd = math.sqrt(var_num / denominator)
    print("Standard deviation is: ", sd)



start = timeit.default_timer()
naive()
stop = timeit.default_timer()
print((stop - start) * 1000.0)

start = timeit.default_timer()
welford()
stop = timeit.default_timer()
print((stop - start) * 1000.0)

start = timeit.default_timer()
onepass()
stop = timeit.default_timer()
print((stop - start) * 1000.0)

start = timeit.default_timer()
histogram()
stop = timeit.default_timer()
print((stop - start) * 1000.0)

