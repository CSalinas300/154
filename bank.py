import enum
from queue import PriorityQueue
import random

from scipy.stats import rv_discrete
from matplotlib import pyplot as plt


class Customer:
    """Customer model"""

    def __init__(self, name):
        self.id = name


class BankState(enum.Enum):
    Busy = 1
    Idle = 0

class Bank:
    """Bank model"""

    def __init__(self, booth_id, Customer, speed, state):
        self.id = booth_id
        self.customer = Customer
        self.speed = speed
        self.state = state

    def booth_available(self):
        return self.state == "IDLE"

    def booth_busy(self):
        return self.state == "BUSY"

    def change_state(self, BankState):
        self.state = BankState

    def get_wu(self):
        return self.speed


class CustomerList:
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

    def size(self):
        return len(self.list)


def generatePQ(n):
    """
    :rtype: CustomerList
    """
    queue = CustomerList()
    for i in range(0, n):
        new_customer = Customer(i)
        queue.add_customer(new_customer)
    return queue

def average_wait_time(q):
    while q.size() != 0:
        '''Wait time for each customer rush of 5-15'''
        wait_time = 0

        '''Total average wait time in 8 hours'''
        total_average = 0

        # 5 to 15 customers per run
        customer_rush = random.randint(5, 15)
        '''If we get more than 10 customers some have to wait longer for a slot to open up'''
        if customer_rush > 10:
            '''Initially add 10 customers to all the booths'''
            booth_list = add_n_booths(10, q)
            for n in range(0, booths):
                '''Add the wait time for each booth speed (10)'''
                wait_time += booth_list[n].speed
            '''The remaining customers are in line'''
            remaining_list = 10 - customer_rush
            '''Add the remaining customers to the booths'''
            booth_list = add_n_booths(remaining_list, q)
            for n in range(0, remaining_list):
                wait_time += booth_list[n].speed
        else:
            '''The rush of customers is less than our booth count so no problem'''
            booth_list = add_n_booths(customer_rush, q)
            for n in range(0, customer_rush):
                wait_time += booth_list[n].speed
        print("Average wait time: ", wait_time / booths, " minutes")
        total_average += wait_time
    print("Total average wait time in 8 hours: ", total_average/customers, " minutes")


def add_n_booths(size, queue):
    booth_list = []
    for i in range(0, size):
        '''Same worker unit for each bank is 10'''
        wu = 10
        booth = Bank(booth_id=i, Customer=queue.get_customer(), speed=wu, state=BankState.Busy)
        booth_list.append(booth)
    return booth_list

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
    '''How many total customers to process in a given (8 hour) day'''
    customers = 160

    '''How many bank booths to use'''
    booths = 10

    '''Add all customers to a queue'''
    q = generatePQ(customers)

    '''Average waiting time for customers'''
    average_wait_time(q)

