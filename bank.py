from queue import PriorityQueue
from scipy.stats import rv_discrete
from matplotlib import pyplot as plt


class Customer:
    """Customer model"""

    def __init__(self, name):
        self.id = name


class Bank:
    """Bank model"""

    def __init__(self, booth_id, Customer, speed, state):
        self.id = booth_id
        self.customer = Customer
        self.speed = speed
        self.state = state

    def booth_available(self):
        return self.state == "FREE"

    def help_customer(self):
        self.state = "WORKING"


class Wait:
    """Priority Queue"""

    def __init__(self):
        """List to print elements"""
        self.list = []
        """PriorityQueue initialization"""
        self.q = PriorityQueue()

    def add_customer(self, Customer):
        self.q.put(Customer.id, Customer)
        self.list.append(Customer.id)

    def get_customer(self):
        if not self.q.empty():
            c = self.q.get()
            self.list.remove(c)
            return c
        return -1

    def get_queue_instance(self):
        return self.q

    def print(self):
        for i in self.list:
            print(i)


def generate(n):
    """
    :rtype: Wait
    """
    queue = Wait()
    for i in range(0, n):
        new_customer = Customer(i)
        queue.add_customer(new_customer)
    return queue


def add_n_banks(n, queue):
    for i in range(0, n):
        bank = Bank(booth_id=n, Customer=queue.get_customer(), speed=10, state="FREE")


def array_input():
    num_array = list()
    num2_array = list()
    num = input("How many elements to add to array? ")
    print('Enter x values')
    for i in range(int(num)):
        n = input("num: ")
        num_array.append(int(n))

    for i in range(int(num)):
        n = input("variance val: ")
        num2_array.append(float(n))
    var = rv_discrete(values=(num_array, num2_array))
    print("Mean: ", var.mean())
    print("Variance: ", var.var())
    print("Standard Deviation: ", var.std())
    graph_it(num_array, num2_array)


def graph_it(x, y):
    plt.plot(x, y)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Data")
    plt.show()


def square_it():
    print("Enter a number to square: ")
    num1 = int(input())
    print("Square of num1: ", num1 * num1)


def print_bye(name):
    print(f"BYE, {name}")


if __name__ == '__main__':
    '''How many total customers to process'''
    customers = 160

    '''Add 160 customers to a queue'''
    q = generate(customers)

    '''Add 10 customers to a bank booth'''
    add_n_banks(10, q)

    '''Print the remaining customers in the queue'''
    q.print()

    val = "y"
    while val != 'N':
        add_n_banks(10, q)
        val = input("Continue? (Type N to stop): ")
        '''Print the remaining customers in the queue'''
        q.print()
