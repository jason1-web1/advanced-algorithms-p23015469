```python
def binary_search(numbers, target):
    low = 0
    high = len(numbers) - 1

    while low <= high:
        middle = (low + high) // 2

        if numbers[middle] == target:
            return middle

        elif target < numbers[middle]:
            high = middle - 1

        else:
            low = middle + 1

    return -1


def main():
    numbers = [8, 12, 31, 46, 57, 214]
    target = 31

    result = binary_search(numbers, target)

    if result != -1:
        print(f"{target} found at index {result}")
    else:
        print(f"{target} was not found")


if __name__ == "__main__":
    main()
```
