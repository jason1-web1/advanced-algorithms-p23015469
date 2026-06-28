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

# =========================================================
# PRODUCT ENTITY CLASS
# =========================================================

@dataclass
class Product:
    product_id: str
    product_name: str
    category: str
    price: float
    quantity: int
    expiry_date: str

    def __str__(self):
        return (
            f"{self.product_id:<10}"
            f"{self.product_name:<25}"
            f"{self.category:<15}"
            f"RM {self.price:<10.2f}"
            f"{self.quantity:<10}"
            f"{self.expiry_date:<12}"
        )

# Special marker used for deleted buckets
DELETED = object()

# =========================================================
# LINEAR PROBING HASH TABLE
# =========================================================

class LinearProbingHashTable:

    def __init__(self, size=29):
        self.size = size

        # The buckets are stored in a one-dimensional list.
        self.buckets = [None] * size

        self.number_of_products = 0

    def hash_function(self, product_id):
        """
        Convert the product ID into a bucket index.
        Example: MED101 becomes a numerical hash value.
        """
        hash_value = 0

        for character in product_id:
            hash_value = (
                hash_value * 31 + ord(character)
            ) % self.size

        return hash_value

    def insert(self, product):
        index = self.hash_function(product.product_id)

        for attempt in range(self.size):
            current_index = (index + attempt) % self.size
            bucket = self.buckets[current_index]

            # Empty or deleted bucket
            if bucket is None or bucket is DELETED:
                self.buckets[current_index] = product
                self.number_of_products += 1
                return True

            # Replace an existing product with the same ID
            if bucket.product_id == product.product_id:
                self.buckets[current_index] = product
                return True

        print("Hash table is full.")
        return False

    def search(self, product_id):
        index = self.hash_function(product_id)

        for attempt in range(self.size):
            current_index = (index + attempt) % self.size
            bucket = self.buckets[current_index]

            # A completely empty bucket means the product does not exist
            if bucket is None:
                return None

            if bucket is not DELETED:
                if bucket.product_id == product_id:
                    return bucket

        return None

    def edit(self, product_id):
        product = self.search(product_id)

        if product is None:
            print("Product not found.")
            return

        print("\nLeave the field empty to keep the current value.")

        new_name = input(
            f"New product name [{product.product_name}]: "
        ).strip()

        new_category = input(
            f"New category [{product.category}]: "
        ).strip()

        new_price = input(
            f"New price [{product.price:.2f}]: "
        ).strip()

        new_quantity = input(
            f"New quantity [{product.quantity}]: "
        ).strip()

        while True:
            new_expiry = input(
                f"New expiry date [{product.expiry_date}] "
                "(DD/MM/YYYY): "
            ).strip()

            if not new_expiry or validate_date(new_expiry):
                break

            print("Invalid date. Please use DD/MM/YYYY.")

        if new_name:
            product.product_name = new_name

        if new_category:
            product.category = new_category

        if new_price:
            product.price = float(new_price)

        if new_quantity:
            product.quantity = int(new_quantity)

        if new_expiry:
            product.expiry_date = new_expiry

        print("Product updated successfully.")

    def delete(self, product_id):
        index = self.hash_function(product_id)

        for attempt in range(self.size):
            current_index = (index + attempt) % self.size
            bucket = self.buckets[current_index]

            if bucket is None:
                return False

            if bucket is not DELETED:
                if bucket.product_id == product_id:
                    self.buckets[current_index] = DELETED
                    self.number_of_products -= 1
                    return True

        return False

    def display_all(self):
        print("\n" + "=" * 95)
        print("PHARMACY PRODUCT INVENTORY")
        print("=" * 95)

        print(
            f"{'ID':<10}"
            f"{'Product Name':<25}"
            f"{'Category':<15}"
            f"{'Price':<13}"
            f"{'Quantity':<10}"
            f"{'Expiry':<12}"
        )

        print("-" * 95)

        products_found = False

        for bucket in self.buckets:
            if bucket is not None and bucket is not DELETED:
                print(bucket)
                products_found = True

        if not products_found:
            print("No products are currently stored.")

        print("-" * 95)
        print(
            f"Number of products: {self.number_of_products}"
        )

        print(
            f"Hash table size: {self.size}"
        )

        print(
            f"Load factor: "
            f"{self.number_of_products / self.size:.2f}"
        )

        print("=" * 95)

    def display_bucket_structure(self):
        print("\nHASH TABLE BUCKET STRUCTURE")
        print("=" * 55)

        for index, bucket in enumerate(self.buckets):
            if bucket is None:
                value = "EMPTY"
            elif bucket is DELETED:
                value = "DELETED"
            else:
                value = (
                    f"{bucket.product_id} - "
                    f"{bucket.product_name}"
                )

            print(f"Bucket {index:02d}: {value}")

        print("=" * 55)

# =========================================================
# SAMPLE PHARMACY PRODUCTS
# =========================================================

def create_sample_products():
    return [
        Product(
            "MED101",
            "Paracetamol 500mg",
            "Tablet",
            6.50,
            120,
            "31/03/2028"
        ),
        Product(
            "MED204",
            "Cough Relief Syrup",
            "Syrup",
            12.90,
            45,
            "30/11/2027"
        ),
        Product(
            "MED317",
            "Vitamin C 1000mg",
            "Supplement",
            28.00,
            68,
            "15/07/2028"
        ),
        Product(
            "MED430",
            "Antacid Chewable",
            "Tablet",
            9.80,
            74,
            "20/09/2027"
        ),
        Product(
            "MED543",
            "Oral Rehydration Salt",
            "Sachet",
            4.20,
            150,
            "31/01/2029"
        ),
        Product(
            "MED656",
            "Allergy Relief",
            "Tablet",
            15.50,
            36,
            "10/04/2028"
        ),
        Product(
            "MED769",
            "Zinc Supplement",
            "Supplement",
            22.00,
            55,
            "25/10/2028"
        ),
        Product(
            "MED872",
            "Antiseptic Cream",
            "Cream",
            10.90,
            41,
            "31/12/2027"
        ),
        Product(
            "MED985",
            "Saline Nasal Spray",
            "Spray",
            18.50,
            33,
            "18/05/2028"
        ),
        Product(
            "MED198",
            "Ibuprofen 200mg",
            "Tablet",
            8.40,
            90,
            "12/08/2027"
        )
    ]

# =========================================================
# ONE-DIMENSIONAL LIST LINEAR SEARCH
# =========================================================

def linear_search(product_list, product_id):
    for product in product_list:
        if product.product_id == product_id:
            return product

    return None

# =========================================================
# SEARCH PERFORMANCE EXPERIMENT
# =========================================================

def search_performance_experiment():
    number_of_records = 5000
    repetitions = 500

    product_list = []

    experiment_table = LinearProbingHashTable(
        size=10007
    )

    # Insert the same records into both structures
    for number in range(number_of_records):
        product = Product(
            product_id=f"P{number:05d}",
            product_name=f"Product {number}",
            category="Medicine",
            price=10.00,
            quantity=100,
            expiry_date="31/12/2029"
        )

        product_list.append(product)
        experiment_table.insert(product)

    search_keys = [
        "P00000",   # Existing at beginning
        "P02500",   # Existing in middle
        "P04999",   # Existing at end
        "P09999",   # Non-existing
        "X00001"    # Non-existing
    ]

    # Warm-up
    for key in search_keys:
        experiment_table.search(key)
        linear_search(product_list, key)

    total_searches = (
        repetitions * len(search_keys)
    )

    # Measure hash table search
    hash_start = perf_counter_ns()

    for repeat in range(repetitions):
        for key in search_keys:
            experiment_table.search(key)

    hash_end = perf_counter_ns()
    hash_total_time = hash_end - hash_start

    # Measure one-dimensional list search
    list_start = perf_counter_ns()

    for repeat in range(repetitions):
        for key in search_keys:
            linear_search(product_list, key)

    list_end = perf_counter_ns()
    list_total_time = list_end - list_start

    hash_average = hash_total_time / total_searches
    list_average = list_total_time / total_searches

    print("\n" + "=" * 72)
    print("HASH TABLE VS ONE-DIMENSIONAL LIST")
    print("=" * 72)

    print(
        f"Number of records              : "
        f"{number_of_records:,}"
    )

    print(
        f"Total searches                 : "
        f"{total_searches:,}"
    )

    print("-" * 72)

    print(
        f"Hash Table total time          : "
        f"{hash_total_time:,} ns"
    )

    print(
        f"Hash Table average time        : "
        f"{hash_average:,.2f} ns/search"
    )

    print(
        f"One-dimensional list total     : "
        f"{list_total_time:,} ns"
    )

    print(
        f"One-dimensional list average   : "
        f"{list_average:,.2f} ns/search"
    )

    if hash_total_time > 0:
        speed_difference = (
            list_total_time / hash_total_time
        )

        print(
            f"Hash Table measured speed-up   : "
            f"{speed_difference:.2f} times"
        )

    print("=" * 72)

# =========================================================
# INPUT FUNCTIONS
# =========================================================

def input_product():
    print("\nENTER NEW PRODUCT INFORMATION")

    product_id = input(
        "Product ID: "
    ).strip().upper()

    product_name = input(
        "Product name: "
    ).strip()

    category = input(
        "Category: "
    ).strip()

    price = float(
        input("Price (RM): ")
    )

    quantity = int(
        input("Quantity: ")
    )

    while True:
        expiry_date = input(
            "Expiry date (DD/MM/YYYY): "
        ).strip()

        if validate_date(expiry_date):
            break

        print(
            "Invalid date. Please use DD/MM/YYYY, "
            "for example 25/06/2028."
        )

    if price < 0:
        raise ValueError(
            "Price cannot be negative."
        )

    if quantity < 0:
        raise ValueError(
            "Quantity cannot be negative."
        )

    return Product(
        product_id,
        product_name,
        category,
        price,
        quantity,
        expiry_date
    )

# =========================================================
# MAIN MENU
# =========================================================

def main():
    hash_table = LinearProbingHashTable(size=29)

    for product in create_sample_products():
        hash_table.insert(product)

    while True:
        print("\n" + "=" * 55)
        print("LOCAL PHARMACY INVENTORY SYSTEM")
        print("=" * 55)
        print("1. Display all products")
        print("2. Insert a product")
        print("3. Search for a product")
        print("4. Edit a product")
        print("5. Delete a product")
        print("6. Display bucket structure")
        print("7. Run search performance experiment")
        print("0. Exit")
        print("=" * 55)

        choice = input(
            "Enter your choice: "
        ).strip()

        try:
            if choice == "1":
                hash_table.display_all()

            elif choice == "2":
                new_product = input_product()

                if hash_table.insert(new_product):
                    print(
                        "Product inserted successfully."
                    )

            elif choice == "3":
                product_id = input(
                    "Enter product ID to search: "
                ).strip().upper()

                result = hash_table.search(
                    product_id
                )

                if result is None:
                    print("Product not found.")
                else:
                    print("\nProduct found:")
                    print("-" * 95)
                    print(result)

            elif choice == "4":
                product_id = input(
                    "Enter product ID to edit: "
                ).strip().upper()

                hash_table.edit(product_id)

            elif choice == "5":
                product_id = input(
                    "Enter product ID to delete: "
                ).strip().upper()

                if hash_table.delete(product_id):
                    print(
                        "Product deleted successfully."
                    )
                else:
                    print("Product not found.")

            elif choice == "6":
                hash_table.display_bucket_structure()

            elif choice == "7":
                search_performance_experiment()

            elif choice == "0":
                print(
                    "Pharmacy inventory system ended."
                )
                break

            else:
                print(
                    "Invalid choice. Please try again."
                )

        except ValueError as error:
            print(f"Input error: {error}")

        except OverflowError as error:
            print(f"Table error: {error}")

if __name__ == "__main__":
    main()

