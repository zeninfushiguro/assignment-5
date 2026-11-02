class Contact:
    '''
    Contact class to represent a contact with a name and number.
    Attributes:
        name (str): The name of the contact.
        number (str): The phone number of the contact.
    '''

    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return f"{self.name}: {self.number}"


class Node:
    '''
    Node class to represent a single entry in the hash table.
    Attributes:
        key (str): The key (name) of the contact.
        value (Contact): The value (Contact object) associated with the key.
        next (Node): Pointer to the next node in case of a collision.
    '''

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    '''
    HashTable class to represent a hash table for storing contacts.
    Attributes:
        size (int): The size of the hash table.
        data (list): The underlying array to store linked lists for collision handling.
    Methods:
        hash_function(key): Converts a string key into an array index.
        insert(key, value): Inserts a new contact into the hash table.
        search(key): Searches for a contact by name.
        print_table(): Prints the structure of the hash table.
    '''

    def __init__(self, size):
        self.size = size
        self.data = [None] * size

    def hash_function(self, key):
        total = 0
        for char in key:
            total += ord(char)
        return total % self.size

    def insert(self, key, value):
        # value is the phone number string
        index = self.hash_function(key)
        current = self.data[index]

        # Empty slot: start a new chain
        if current is None:
            self.data[index] = Node(key, Contact(key, value))
            return

        # Walk the chain; update if the key already exists
        while True:
            if current.key == key:
                current.value.number = value
                return
            if current.next is None:
                break
            current = current.next

        # Key not found: append to the end of the chain
        current.next = Node(key, Contact(key, value))

    def search(self, key):
        index = self.hash_function(key)
        current = self.data[index]
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def print_table(self):
        for i in range(self.size):
            current = self.data[i]
            if current is None:
                print(f"Index {i}: Empty")
            else:
                line = f"Index {i}:"
                while current is not None:
                    line += f" - {current.value}"
                    current = current.next
                print(line)


# Test your hash table implementation here.
if __name__ == "__main__":
    table = HashTable(10)
    table.print_table()

    table.insert("John", "909-876-1234")
    table.insert("Rebecca", "111-555-0002")
    print()
    table.print_table()

    print("\nSearch result:", table.search("John"))

    # Edge case 1: collisions
    table.insert("Amy", "111-222-3333")
    table.insert("May", "222-333-1111")
    print()
    table.print_table()

    # Edge case 2: duplicate key updates the number
    table.insert("Rebecca", "999-444-9999")
    print()
    table.print_table()

    # Edge case 3: missing key
    print(table.search("Chris"))  # None


# DESIGN MEMO

# A hash table is the right structure for fast lookups because it turns a key
# directly into an array index. Instead of scanning every contact until a name
# matches, the hash function computes where the contact should live and the
# program jumps straight to that slot. With a reasonably sized table and evenly
# spread keys, insert and search take O(1) time on average, no matter how many
# contacts are stored. A list needs O(n) scanning, and a balanced tree needs
# O(log n) comparisons.

# I handled collisions with separate chaining. Each array slot holds either None
# or the head of a linked list of Node objects. When two names hash to the same
# index, such as Amy and May, which have the same character-code sum, the new
# node is added to the end of that index's chain. Searching hashes the key, then
# walks only that one chain comparing keys, so the cost depends on chain length
# rather than total contacts. Inserting an existing name walks the chain, finds
# the matching key, and updates the number instead of adding a duplicate.

# The weakness is that my hash function sums character codes, so anagrams
# collide, and with a fixed size the chains grow as contacts are added. A
# production version would use a better hash and resize when the load factor
# got high.

 #An engineer would choose a hash table over a list or tree when the main
# operations are exact-key lookups, inserts, and updates, and ordering does not
# matter. Examples are caches, phone books, and symbol tables. A tree is the
# better choice when sorted order or range queries are required.