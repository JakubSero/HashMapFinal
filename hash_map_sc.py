# Name: Jakub Kowalski
# OSU Email: kowaljak@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/9/2022
# Description: hash map implementation with chaining by linked lists


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        inserts a new node into the hash map.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        # check if the hashmap already has the value or not
        if self._buckets[index].contains(key):
            # key does exist, update value
            for node in self._buckets[index]:
                if node.key == key:
                    node.value = value
        else:
            # key does not exist, add new k,v
            self._buckets[index].insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        count empty buckets in the hash map
        """
        count = 0
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                count += 1
        return count

    def table_load(self) -> float:
        """
        number of elements divided by the capacity (number of buckets)
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        sets the self._bucket to a new array and fills them with LinkedLists()
        """
        self._buckets = DynamicArray()
        i = 0
        while i < self._capacity:
            self._buckets.append(LinkedList())
            i += 1
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        resizes the table and rehashes the values in it
        """
        old_capacity = self._capacity

        # copy values of current buckets
        temp = DynamicArray()
        for i in range(old_capacity):
            temp.append(self._buckets[i])

        if new_capacity < 1:
            return

        # prime check
        if self._is_prime(new_capacity):
            self._capacity = new_capacity
        else:
            self._capacity = self._next_prime(new_capacity)

        # make new array in buckets with new capacity
        self._buckets = DynamicArray()
        for i in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0

        # copy all the old elements and nodes and rehash them into the new self._buckets
        for i in range(old_capacity):
            for node in temp[i]:
                if node is not None:
                    current = node
                    while current is not None:
                        self.put(current.key, current.value)
                        current = current.next

    def get(self, key: str) -> object:
        """
        returns the value associated with the given key
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        # return None if key not in hash map
        if self._buckets[index] is None:
            return None

        for node in self._buckets[index]:
            if node.key == key:
                return node.value

    def contains_key(self, key: str) -> bool:
        """
        returns True if the key is in the hash map, otherwise False
        """
        if self._size == 0:
            return False

        hash = self._hash_function(key)
        index = hash % self._capacity

        if self._buckets[index] is None:
            return False

        for node in self._buckets[index]:
            if node.key == key:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        removes a node from the linked list and hash map
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        # checks for the node and then removes if it's there
        for node in self._buckets[index]:
            if node.key == key:
                self._buckets[index].remove(key)
                self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        returns all nodes in a tuple (k,v) in a new array
        """
        temp = DynamicArray()

        for i in range(self._capacity):
            if self._buckets[i] is not None:
                for node in self._buckets[i]:
                    temp.append((node.key, node.value))

        return temp

    def get_buckets(self) -> DynamicArray:
        """
        returns the buckets
        """
        return self._buckets

    def get_function(self):
        """
        returns the hash_function
        """
        return self._hash_function


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Finds the most occuring value(s) in the da.
    returns the array of most common value(s) and the frequency as a tuple
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    return_arr = DynamicArray()

    # loop through the da, find the hash/index, put them into map
    # and increase the value associated with it if that key
    # was already in the hash map, otherwise just put it in
    # with a 1 as its value
    max_frequency = 1
    for i in range(da.length()):
        hash = map.get_function()(da[i])
        index = hash % map.get_capacity()
        if map.contains_key(da[i]):
            # get the value and increase it if there was already another instance
            # of the key in the hash map
            value = map.get_buckets()[index].contains(da[i]).value
            if value is not None:
                count = value + 1
                if count >= max_frequency:
                    max_frequency = count
                map.put(da[i], count)
        else:
            map.put(da[i], 1)

    # now goes through that map and finds the keys with values
    # equal to the max_frequency variable from earlier.
    # if it is equal, add it to the return array and
    # return that array along with the frequency
    for i in range(map.get_capacity()):
        for node in map.get_buckets()[i]:
            if node.value == max_frequency:
                return_arr.append(node.key)
    return return_arr, max_frequency


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    # print(m)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m)
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(1)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
