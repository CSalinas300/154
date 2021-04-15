import enum
import queue
import random
import numpy

from scipy import stats
from matplotlib import pyplot as plt


class Customer:
    """Customer model"""

    def __init__(self, name, work_unit):
        """Customer name/id"""
        self.id = name
        """Customer's work unit"""
        self.wu = work_unit

    def get_wu(self):
        return self.wu


class BoothState(enum.Enum):
    Busy = 1
    Idle = 0


class Bank:
    """Bank model"""

    def __init__(self, booth_id, customer, speed, state):
        self.id = booth_id
        self.customer = customer
        self.speed = speed
        self.state = state

    def booth_available(self):
        return self.state == BoothState.Idle

    def booth_busy(self):
        return self.state == BoothState.Busy

    def change_state(self, state):
        self.state = state

    def help_customer(self, customer):
        self.customer = customer
        self.change_state(BoothState.Busy)

    def get_wu(self):
        return self.speed


class CustomerListPQ:
    """Priority Queue"""

    def __init__(self):
        """List to print elements"""
        self.list = []
        """PriorityQueue initialization"""
        self.q = queue.PriorityQueue()

    def add_customer(self, customer):
        """Adding a customer to a PQ use the work unit and id for sorting"""
        self.q.put(customer.get_wu(), customer.id, customer)
        self.list.append(customer.get_wu())

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


class CustomerList:
    """Normal Queue"""

    def __init__(self):
        """List to print elements"""
        self.list = []
        """Queue initialization"""
        self.q = queue.Queue()

    def add_customer(self, customer):
        """Adding a customer to a queue using FIFO"""
        self.q.put(customer)
        self.list.append(customer)

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


def generate_priority_queue(n):
    """
    :rtype: CustomerList
    """
    pq = CustomerListPQ()
    _list = n
    for i in range(0, _list.size()):
        new_customer = _list.get_customer()
        new_customer.wu = generate_gaussian_wu(c_mean, c_std)
        # print("Adding customer", new_customer.id, "wu ->", new_customer.get_wu())
        pq.add_customer(new_customer)
    return pq


def generate_gaussian_wu(mean, std):
    # random.gauss(mean, std)
    dist = stats.norm(mean, std)  # create a normal/gaussian random variable
    # print("Probability of 5 wu: ", dist.pdf(5))  # probability density at 5 and 15
    # print("Probability of 15 wu: ", dist.pdf(15))
    return dist.rvs()  # get a random sample


def generate_queue(n):
    """
    :rtype: CustomerList
    """
    qq = CustomerList()
    for i in range(0, n):
        # Adding customer to a normal queue with a worker unit of 0 as "unknown"
        new_customer = Customer(i, 0)
        qq.add_customer(new_customer)
    return qq


def generate_booths(n, worker_unit):
    booth_instances = []
    for i in range(0, n):
        booth = Bank(booth_id=i, customer=-1, speed=worker_unit, state=BoothState.Idle)
        booth_instances.append(booth)
    return booth_instances


def average_wait_time(r):
    # Total average wait time in 8 hours
    total_average = 0

    while r.size() != 0:
        '''Wait time for each customer rush of 5-15'''
        wait_time = 0

        '''Process all of the customers in the PQ'''
        # wait time is returned from the function
        if r.size() > 10:
            wait_time += process_customers(size=10, booth_list=booth_instance, qq=r)
        else:
            wait_time += process_customers(size=r.size(), booth_list=booth_instance, qq=r)

        print("Average wait time for ", 10, "customers:", wait_time, "wu")
        total_average += wait_time
    print("\tTotal average wait time in 8 hours:", total_average / customers, "wu")
    wu_to_hours(total_average/customers)


def add_n_booths(size, queue):
    booth_list = []
    for i in range(0, size):
        '''Same worker unit for each bank is 10'''
        internal_wu = 10
        booth = Bank(booth_id=i, customer=queue.get_customer(), speed=internal_wu, state=BoothState.Busy)
        booth_list.append(booth)
    return booth_list


def get_normal_distribution(x, mean, sd):
    prob_density = (numpy.pi * sd) * numpy.exp(-0.5 * ((x - mean) / sd) ** 2)
    return prob_density


def get_dist_output():
    x = numpy.linspace(5, 15, 200)
    mean = 5
    sd = 0.5
    dist = get_normal_distribution(x, mean, sd)
    return dist


def process_customers(size, booth_list, qq):
    c_wu = 0
    b_wu = 0

    while size != 0:
        for i in range(0, size):
            if booth_list[i].booth_available():
                customer = qq.get_customer()
                booth_list[i].help_customer(customer)
                b_wu += booth_list[i].get_wu()
                c_wu += customer
                # print("Customer:", customer, "loop size:", size)
                size -= 1  # subtract 1 from size
            else:
                booth_list[i].change_state(BoothState.Idle)
    return b_wu + c_wu  # return the sum of booth wu + customer wu


def wu_to_hours(wu_input):
    hours = wu_input / 10
    print(wu_input, "wu is", hours,"hours")


if __name__ == '__main__':
    '''How many total customers to process in a given (8 hour) day'''
    customers = 160

    '''How many bank booths to use'''
    booths = 10

    '''Booth worker units'''
    wu = 10

    '''Customer work units'''
    c_mean = 5
    c_std = 0.5

    '''Create the booth instances'''
    booth_instance = generate_booths(booths, worker_unit=wu)

    '''Add all customers to a queue'''
    s = generate_queue(customers)

    '''Generate events for all customers'''
    r = generate_priority_queue(s)

    '''Average wait time 2 using states and a single bank instance'''
    average_wait_time(r)
