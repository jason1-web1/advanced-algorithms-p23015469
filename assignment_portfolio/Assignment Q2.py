from dataclasses import dataclass
from datetime import datetime
from time import perf_counter_ns


# =========================================================
# DATE VALIDATION
# =========================================================

def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%d/%m/%Y")
        return True
    except ValueError:
        return False


# Global variables for performance information
merge_sort_recursive_calls = 0
merge_sort_comparisons = 0


# =========================================================
# TRANSACTION ENTITY CLASS
# =========================================================

@dataclass
class Transaction:
    transaction_id: int
    customer_name: str
    product_name: str
    amount: float
    transaction_date: str

    def __str__(self):
        return (
            f"{self.transaction_id:<12}"
            f"{self.customer_name:<22}"
            f"{self.product_name:<25}"
            f"RM {self.amount:<12.2f}"
            f"{self.transaction_date:<12}"
        )


# =========================================================
# MERGE SORT
# =========================================================

def merge_sort(transactions, sort_attribute="transaction_id"):
    """
    Divide and Conquer Merge Sort.

    Divide:
    The list is divided into two smaller lists.

    Conquer:
    Each smaller list is sorted recursively.

    Combine:
    The sorted smaller lists are merged together.
    """

    global merge_sort_recursive_calls

    merge_sort_recursive_calls += 1

    if len(transactions) <= 1:
        return transactions.copy()

    # Divide step
    middle = len(transactions) // 2

    left_half = transactions[:middle]
    right_half = transactions[middle:]

    # Conquer step
    sorted_left = merge_sort(
        left_half,
        sort_attribute
    )

    sorted_right = merge_sort(
        right_half,
        sort_attribute
    )

    # Combine step
    return merge(
        sorted_left,
        sorted_right,
        sort_attribute
    )


def merge(left, right, sort_attribute):
    global merge_sort_comparisons

    merged_list = []

    left_index = 0
    right_index = 0

    while (
            left_index < len(left)
            and right_index < len(right)
    ):
        merge_sort_comparisons += 1

        left_value = getattr(
            left[left_index],
            sort_attribute
        )

        right_value = getattr(
            right[right_index],
            sort_attribute
        )

        if left_value <= right_value:
            merged_list.append(
                left[left_index]
            )

            left_index += 1

        else:
            merged_list.append(
                right[right_index]
            )

            right_index += 1

    # Add remaining records
    merged_list.extend(
        left[left_index:]
    )

    merged_list.extend(
        right[right_index:]
    )

    return merged_list


# =========================================================
# BINARY SEARCH
# =========================================================

def binary_search(transactions, target_id):
    low = 0
    high = len(transactions) - 1
    comparisons = 0

    while low <= high:
        comparisons += 1

        middle = (low + high) // 2

        middle_id = (
            transactions[middle].transaction_id
        )

        if middle_id == target_id:
            return transactions[middle], comparisons

        if target_id < middle_id:
            high = middle - 1

        else:
            low = middle + 1

    return None, comparisons


# =========================================================
# LINEAR SEARCH
# =========================================================

def linear_search(transactions, target_id):
    comparisons = 0

    for transaction in transactions:
        comparisons += 1

        if transaction.transaction_id == target_id:
            return transaction, comparisons

    return None, comparisons


# =========================================================
# SAMPLE DATASET
# =========================================================

def create_sample_transactions():
    return [
        Transaction(
            1087,
            "Alicia Tan",
            "Wireless Mouse",
            79.90,
            "18/04/2026"
        ),
        Transaction(
            1021,
            "Brandon Lee",
            "Laptop Stand",
            129.00,
            "09/04/2026"
        ),
        Transaction(
            1114,
            "Carmen Lim",
            "Mechanical Keyboard",
            259.90,
            "02/05/2026"
        ),
        Transaction(
            1046,
            "Daniel Wong",
            "USB-C Cable",
            35.50,
            "12/04/2026"
        ),
        Transaction(
            1095,
            "Emily Chan",
            "Bluetooth Speaker",
            189.00,
            "21/04/2026"
        ),
        Transaction(
            1013,
            "Farah Ahmad",
            "Power Bank",
            99.90,
            "05/04/2026"
        ),
        Transaction(
            1122,
            "George Tan",
            "Gaming Headset",
            229.00,
            "05/05/2026"
        ),
        Transaction(
            1058,
            "Hannah Ong",
            "Web Camera",
            149.90,
            "15/04/2026"
        ),
        Transaction(
            1034,
            "Isaac Goh",
            "Phone Case",
            39.90,
            "10/04/2026"
        ),
        Transaction(
            1106,
            "Jenny Low",
            "Smart Watch",
            399.00,
            "29/04/2026"
        ),
        Transaction(
            1071,
            "Kevin Ng",
            "Tablet Cover",
            59.90,
            "17/04/2026"
        ),
        Transaction(
            1063,
            "Linda Chew",
            "Portable Fan",
            49.90,
            "16/04/2026"
        )
    ]


# =========================================================
# DISPLAY FUNCTIONS
# =========================================================

def display_transactions(
        transactions,
        title="CUSTOMER TRANSACTIONS"
):
    print("\n" + "=" * 105)
    print(title)
    print("=" * 105)

    print(
        f"{'Transaction':<12}"
        f"{'Customer':<22}"
        f"{'Product':<25}"
        f"{'Amount':<15}"
        f"{'Date':<12}"
    )

    print("-" * 105)

    for transaction in transactions:
        print(transaction)

    print("-" * 105)

    print(
        f"Total records: {len(transactions)}"
    )

    print("=" * 105)


def display_search_result(
        result,
        comparisons,
        search_method
):
    print(
        f"\n{search_method} result"
    )

    print("-" * 70)

    if result is None:
        print("Transaction was not found.")

    else:
        print("Transaction found:")
        print(result)

    print(
        f"Number of comparisons: {comparisons}"
    )

    print("-" * 70)


# =========================================================
# DYNAMIC TRANSACTION INSERTION
# =========================================================

def insert_transaction(transactions):
    transaction_id = int(
        input("Transaction ID: ")
    )

    for transaction in transactions:
        if (
                transaction.transaction_id
                == transaction_id
        ):
            print(
                "Transaction ID already exists."
            )

            return

    customer_name = input(
        "Customer name: "
    ).strip()

    product_name = input(
        "Product name: "
    ).strip()

    amount = float(
        input("Transaction amount (RM): ")
    )

    while True:
        transaction_date = input(
            "Transaction date (DD/MM/YYYY): "
        ).strip()

        if validate_date(transaction_date):
            break

        print(
            "Invalid date. Please use DD/MM/YYYY, "
            "for example 25/06/2026."
        )

    if amount < 0:
        raise ValueError(
            "Amount cannot be negative."
        )

    new_transaction = Transaction(
        transaction_id,
        customer_name,
        product_name,
        amount,
        transaction_date
    )

    transactions.append(new_transaction)

    print(
        "Transaction inserted successfully."
    )


# =========================================================
# TIME COMPLEXITY TABLE
# =========================================================

def display_complexity_table():
    print("\n" + "=" * 78)
    print("TIME COMPLEXITY ANALYSIS")
    print("=" * 78)

    print(
        f"{'Algorithm':<22}"
        f"{'Best Case':<18}"
        f"{'Average Case':<18}"
        f"{'Worst Case':<18}"
    )

    print("-" * 78)

    print(
        f"{'Merge Sort':<22}"
        f"{'O(n log n)':<18}"
        f"{'O(n log n)':<18}"
        f"{'O(n log n)':<18}"
    )

    print(
        f"{'Binary Search':<22}"
        f"{'O(1)':<18}"
        f"{'O(log n)':<18}"
        f"{'O(log n)':<18}"
    )

    print(
        f"{'Linear Search':<22}"
        f"{'O(1)':<18}"
        f"{'O(n)':<18}"
        f"{'O(n)':<18}"
    )

    print("=" * 78)


# =========================================================
# PERFORMANCE EXPERIMENT
# =========================================================

def run_performance_experiment(
        transactions
):
    search_repetitions = 30000
    sort_repetitions = 2000

    original_data = transactions.copy()

    sorted_data = merge_sort(
        original_data,
        "transaction_id"
    )

    target_id = max(
        transaction.transaction_id
        for transaction in original_data
    )

    # Warm-up
    merge_sort(
        original_data,
        "transaction_id"
    )

    binary_search(
        sorted_data,
        target_id
    )

    linear_search(
        original_data,
        target_id
    )

    # Measure Merge Sort
    sort_start = perf_counter_ns()

    for repeat in range(sort_repetitions):
        merge_sort(
            original_data,
            "transaction_id"
        )

    sort_end = perf_counter_ns()

    merge_sort_total = (
            sort_end - sort_start
    )

    # Measure Binary Search
    binary_start = perf_counter_ns()

    for repeat in range(search_repetitions):
        binary_search(
            sorted_data,
            target_id
        )

    binary_end = perf_counter_ns()

    binary_total = (
            binary_end - binary_start
    )

    # Measure Linear Search
    linear_start = perf_counter_ns()

    for repeat in range(search_repetitions):
        linear_search(
            original_data,
            target_id
        )

    linear_end = perf_counter_ns()

    linear_total = (
            linear_end - linear_start
    )

    print("\n" + "=" * 82)
    print("ALGORITHM PERFORMANCE EXPERIMENT")
    print("=" * 82)

    print(
        f"Dataset size                      : "
        f"{len(original_data)} records"
    )

    print(
        f"Merge Sort repetitions            : "
        f"{sort_repetitions:,}"
    )

    print(
        f"Search repetitions                : "
        f"{search_repetitions:,}"
    )

    print("-" * 82)

    print(
        f"Merge Sort total time             : "
        f"{merge_sort_total:,} ns"
    )

    print(
        f"Merge Sort average time           : "
        f"{merge_sort_total / sort_repetitions:,.2f} ns"
    )

    print(
        f"Binary Search total time          : "
        f"{binary_total:,} ns"
    )

    print(
        f"Binary Search average time        : "
        f"{binary_total / search_repetitions:,.2f} ns"
    )

    print(
        f"Linear Search total time          : "
        f"{linear_total:,} ns"
    )

    print(
        f"Linear Search average time        : "
        f"{linear_total / search_repetitions:,.2f} ns"
    )

    if binary_total > 0:
        print(
            f"Binary Search speed-up compared "
            f"with Linear Search: "
            f"{linear_total / binary_total:.2f} times"
        )

    print("=" * 82)


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():
    global merge_sort_recursive_calls
    global merge_sort_comparisons

    transactions = (
        create_sample_transactions()
    )

    sorted_by_id = False

    while True:
        print("\n" + "=" * 63)
        print("ONLINE SHOPPING TRANSACTION SYSTEM")
        print("=" * 63)

        print("1. Display all transactions")
        print("2. Sort using Merge Sort")
        print("3. Search using Binary Search")
        print("4. Search using Linear Search")
        print("5. Insert a new transaction")
        print("6. Sort by transaction amount")
        print("7. Display Merge Sort statistics")
        print("8. Display time complexity table")
        print("9. Run performance experiment")
        print("0. Exit")

        print("=" * 63)

        choice = input(
            "Enter your choice: "
        ).strip()

        try:
            if choice == "1":
                display_transactions(
                    transactions
                )

            elif choice == "2":
                display_transactions(
                    transactions,
                    "TRANSACTIONS BEFORE MERGE SORT"
                )

                merge_sort_recursive_calls = 0
                merge_sort_comparisons = 0

                transactions = merge_sort(
                    transactions,
                    "transaction_id"
                )

                sorted_by_id = True

                display_transactions(
                    transactions,
                    "TRANSACTIONS AFTER MERGE SORT"
                )

                print(
                    "Merge Sort completed successfully."
                )

                print(
                    f"Recursive calls: "
                    f"{merge_sort_recursive_calls}"
                )

                print(
                    f"Comparisons: "
                    f"{merge_sort_comparisons}"
                )

            elif choice == "3":
                if not sorted_by_id:
                    print(
                        "Transactions must be sorted "
                        "before Binary Search."
                    )

                    merge_sort_recursive_calls = 0
                    merge_sort_comparisons = 0

                    transactions = merge_sort(
                        transactions,
                        "transaction_id"
                    )

                    sorted_by_id = True

                    print(
                        "Transactions were automatically "
                        "sorted by transaction ID."
                    )

                target_id = int(
                    input(
                        "Enter transaction ID to search: "
                    )
                )

                result, comparisons = binary_search(
                    transactions,
                    target_id
                )

                display_search_result(
                    result,
                    comparisons,
                    "Binary Search"
                )

            elif choice == "4":
                target_id = int(
                    input(
                        "Enter transaction ID to search: "
                    )
                )

                result, comparisons = linear_search(
                    transactions,
                    target_id
                )

                display_search_result(
                    result,
                    comparisons,
                    "Linear Search"
                )

            elif choice == "5":
                insert_transaction(
                    transactions
                )

                sorted_by_id = False

            elif choice == "6":
                merge_sort_recursive_calls = 0
                merge_sort_comparisons = 0

                transactions = merge_sort(
                    transactions,
                    "amount"
                )

                sorted_by_id = False

                display_transactions(
                    transactions,
                    "TRANSACTIONS SORTED BY AMOUNT"
                )

                print(
                    f"Recursive calls: "
                    f"{merge_sort_recursive_calls}"
                )

                print(
                    f"Comparisons: "
                    f"{merge_sort_comparisons}"
                )

            elif choice == "7":
                print("\nMERGE SORT STATISTICS")
                print("-" * 45)

                print(
                    f"Recursive calls: "
                    f"{merge_sort_recursive_calls}"
                )

                print(
                    f"Comparisons: "
                    f"{merge_sort_comparisons}"
                )

            elif choice == "8":
                display_complexity_table()

            elif choice == "9":
                run_performance_experiment(
                    transactions
                )

            elif choice == "0":
                print(
                    "Transaction system ended."
                )

                break

            else:
                print(
                    "Invalid choice. Please try again."
                )

        except ValueError as error:
            print(f"Input error: {error}")


if __name__ == "__main__":
    main()

