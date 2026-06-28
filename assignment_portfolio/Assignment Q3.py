import threading
from time import perf_counter_ns
from statistics import mean

# Factorial numbers required by the assignment
FACTORIAL_NUMBERS = [50, 100, 200]

# Number of experimental rounds
NUMBER_OF_ROUNDS = 10

# =========================================================
# FACTORIAL FUNCTION
# =========================================================

def calculate_factorial(number):
    """
    Calculates the factorial of a given number.

    Time complexity: O(n)
    Space complexity: O(1)
    """

    if number < 0:
        raise ValueError(
            "Factorial cannot use a negative number."
        )

    result = 1

    for value in range(2, number + 1):
        result = result * value

    return result

# =========================================================
# THREAD WORKER FUNCTION
# =========================================================

def factorial_worker(
    number,
    result_dictionary
):
    """
    Each thread executes this function.
    The factorial result is stored in a dictionary.
    """

    result_dictionary[number] = (
        calculate_factorial(number)
    )

# =========================================================
# MULTITHREADED OPERATION
# =========================================================

def run_with_multithreading():
    results = {}

    threads = []

    # Create one thread for every factorial
    for number in FACTORIAL_NUMBERS:
        thread = threading.Thread(
            target=factorial_worker,
            args=(number, results),
            name=f"Factorial-{number}"
        )

        threads.append(thread)

    # t1: before the first thread starts
    start_time = perf_counter_ns()

    # Start all three threads
    for thread in threads:
        thread.start()

    # Wait until all threads have completed
    for thread in threads:
        thread.join()

    # t2: after the final thread finishes
    end_time = perf_counter_ns()

    time_elapsed = end_time - start_time

    return time_elapsed, results

# =========================================================
# OPERATION WITHOUT MULTITHREADING
# =========================================================

def run_without_multithreading():
    results = {}

    start_time = perf_counter_ns()

    for number in FACTORIAL_NUMBERS:
        results[number] = (
            calculate_factorial(number)
        )

    end_time = perf_counter_ns()

    time_elapsed = end_time - start_time

    return time_elapsed, results

# =========================================================
# SHORTEN LARGE FACTORIAL OUTPUT
# =========================================================

def shorten_number(
    number,
    number_of_digits=15
):
    number_as_text = str(number)

    if len(number_as_text) <= (
        number_of_digits * 2
    ):
        return number_as_text

    beginning = number_as_text[
        :number_of_digits
    ]

    ending = number_as_text[
        -number_of_digits:
    ]

    return (
        f"{beginning}...{ending}"
    )

# =========================================================
# VERIFY FACTORIAL RESULTS
# =========================================================

def display_factorial_results(results):
    print("\n" + "=" * 90)
    print("FACTORIAL CALCULATION RESULTS")
    print("=" * 90)

    for number in FACTORIAL_NUMBERS:
        factorial_value = results[number]

        print(
            f"{number}! = "
            f"{shorten_number(factorial_value)}"
        )

        print(
            f"Number of digits in {number}! = "
            f"{len(str(factorial_value))}"
        )

        print("-" * 90)

# =========================================================
# TEN-ROUND EXPERIMENT
# =========================================================

def run_experiment():
    multithreading_times = []

    non_multithreading_times = []

    final_results = {}

    # Warm-up operations are not included
    run_with_multithreading()
    run_without_multithreading()

    print("\nRunning multithreading experiment...")

    for round_number in range(
        1,
        NUMBER_OF_ROUNDS + 1
    ):
        elapsed_time, results = (
            run_with_multithreading()
        )

        multithreading_times.append(
            elapsed_time
        )

        final_results = results

    print(
        "Running experiment without "
        "multithreading..."
    )

    for round_number in range(
        1,
        NUMBER_OF_ROUNDS + 1
    ):
        elapsed_time, results = (
            run_without_multithreading()
        )

        non_multithreading_times.append(
            elapsed_time
        )

        # Confirm that both methods produce
        # exactly the same factorial results
        if results != final_results:
            raise AssertionError(
                "The factorial results are different."
            )

    return (
        multithreading_times,
        non_multithreading_times,
        final_results
    )

# =========================================================
# DISPLAY EXPERIMENT RESULTS
# =========================================================

def display_experiment_results(
    multithreading_times,
    non_multithreading_times
):
    print("\n" + "=" * 90)
    print(
        "FACTORIAL EXECUTION TIME EXPERIMENT "
        "(NANOSECONDS)"
    )

    print("=" * 90)

    print(
        f"{'Round':<10}"
        f"{'With Multithreading':>28}"
        f"{'Without Multithreading':>32}"
    )

    print("-" * 90)

    for index in range(
        NUMBER_OF_ROUNDS
    ):
        print(
            f"{index + 1:<10}"
            f"{multithreading_times[index]:>28,}"
            f"{non_multithreading_times[index]:>32,}"
        )

    total_multithreading = sum(
        multithreading_times
    )

    total_non_multithreading = sum(
        non_multithreading_times
    )

    average_multithreading = mean(
        multithreading_times
    )

    average_non_multithreading = mean(
        non_multithreading_times
    )

    print("-" * 90)

    print(
        f"{'TOTAL':<10}"
        f"{total_multithreading:>28,}"
        f"{total_non_multithreading:>32,}"
    )

    print(
        f"{'AVERAGE':<10}"
        f"{average_multithreading:>28,.2f}"
        f"{average_non_multithreading:>32,.2f}"
    )

    print("=" * 90)

    print("\nEXPERIMENT CONCLUSION")
    print("-" * 90)

    if (
        average_multithreading
        < average_non_multithreading
    ):
        improvement = (
            average_non_multithreading
            / average_multithreading
        )

        print(
            "Multithreading was faster during "
            "this experiment."
        )

        print(
            f"Measured improvement: "
            f"{improvement:.2f} times."
        )

    else:
        difference = (
            average_multithreading
            / average_non_multithreading
        )

        print(
            "Execution without multithreading "
            "was faster during this experiment."
        )

        print(
            f"Non-multithreaded execution was "
            f"{difference:.2f} times faster."
        )

        print(
            "This can happen because factorial "
            "calculation is a CPU-bound task and "
            "Python threads are affected by the "
            "Global Interpreter Lock."
        )

    print("-" * 90)

# =========================================================
# MAIN PROGRAM
# =========================================================

def main():
    print("=" * 90)
    print(
        "FACTORIAL MULTITHREADING EXPERIMENT"
    )

    print("=" * 90)

    multithreading_times, non_multithreading_times, results = (
        run_experiment()
    )

    display_factorial_results(
        results
    )

    display_experiment_results(
        multithreading_times,
        non_multithreading_times
    )

if __name__ == "__main__":
    main()