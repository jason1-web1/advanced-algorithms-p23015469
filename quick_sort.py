```python
def quick_sort(numbers):
    # Base case
    if len(numbers) <= 1:
        return numbers

    # Select the last value as the pivot
    pivot = numbers[-1]

    smaller_values = []
    equal_values = []
    larger_values = []

    # Separate values based on the pivot
    for number in numbers:
        if number < pivot:
            smaller_values.append(number)
        elif number == pivot:
            equal_values.append(number)
        else:
            larger_values.append(number)

    # Sort the smaller and larger lists recursively
    return (
        quick_sort(smaller_values)
        + equal_values
        + quick_sort(larger_values)
    )


def main():
    numbers = [214, 12, 46, 57, 31, 8]

    print("Original list:", numbers)

    sorted_numbers = quick_sort(numbers)

    print("Sorted list:", sorted_numbers)


if __name__ == "__main__":
    main()
```
