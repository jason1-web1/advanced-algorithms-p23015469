```python
def merge_sort(numbers):
    # Base case: a list with one or zero values is already sorted
    if len(numbers) <= 1:
        return numbers

    # Divide the list into two halves
    middle = len(numbers) // 2

    left_half = numbers[:middle]
    right_half = numbers[middle:]

    # Sort both halves recursively
    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    # Combine the two sorted halves
    return merge(left_half, right_half)


def merge(left, right):
    sorted_list = []

    left_index = 0
    right_index = 0

    # Compare values from both lists
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            sorted_list.append(left[left_index])
            left_index += 1
        else:
            sorted_list.append(right[right_index])
            right_index += 1

    # Add any remaining values
    sorted_list.extend(left[left_index:])
    sorted_list.extend(right[right_index:])

    return sorted_list


def main():
    numbers = [214, 12, 46, 57, 31, 8]

    print("Original list:", numbers)

    sorted_numbers = merge_sort(numbers)

    print("Sorted list:", sorted_numbers)


if __name__ == "__main__":
    main()
```
