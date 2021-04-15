import enum
import queue
import random
import numpy
import numpy as np

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


class Questions:
    """Question class"""

    def __init__(self):
        self.average_wait_time = None
        self.average_wait_time_extra = None
        self.average_wait_time_less = None
        self.customers_not_served_today = None
        self.days_to_finish_customer_160 = None
        self.wait_to_finish_booth_160 = None
        self.total_time = None


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


def average_wait_time(pq, b, _booth_instance):
    # Total average wait time in 8 hours
    total_average = 0
    time_multiplier = pq.size() / b  # use for multiplying time
    start_multipler = 1
    while pq.size() != 0:
        '''Wait time for each customer rush of 5-15'''
        wait_time = 0
        '''Process all of the customers in the PQ'''
        # wait time is returned from the function
        if pq.size() > b:
            wait_time += process_customers(size=b, booth_list=_booth_instance, qq=pq)
        else:
            wait_time += process_customers(size=pq.size(), booth_list=_booth_instance, qq=pq)
        # todo add waiting time to people in queue
        # print("Average wait time for ", b, "customers:", wait_time, "wu")
        # customers not served today
        if total_average / b <= 80:
            question.customers_not_served_today = pq.size()
        if time_multiplier > start_multipler:
            # todo fix this?
            if time_multiplier - start_multipler < 1:
                total_average += wait_time * start_multipler
            else:
                total_average += wait_time * start_multipler
            start_multipler += 1
    print("\tTotal average wait time:", total_average / customers, "wu")
    question.total_time = total_average
    return total_average / customers


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
    print("\t", wu_input, "wu is", hours, "hours")


def _wu_to_hours(wu_input):
    hours = wu_input / 10
    return hours


def normal_dist(x, mean, sd):
    prob_density = (np.pi * sd) * np.exp(-0.5 * ((x - mean) / sd) ** 2)
    return prob_density


def plot_graph():
    # Creating a series of data of in range of [5-15].
    x = np.linspace(5, 15, 200)

    # Calculate mean and Standard deviation.
    # mean = np.mean(x)
    # sd = np.std(x)
    # using ~N(5,0.5)
    mean = 5
    sd = 0.5

    # Apply function to data
    pdf = normal_dist(x, mean, sd)

    # Plot
    plt.plot(x, pdf, color='red')
    plt.xlabel('Data points')
    plt.ylabel('Probability Density')


if __name__ == '__main__':
    '''Class container for question answers'''
    question = Questions()

    '''How many total customers to process in a given (8 hour) day'''
    customers = 160

    '''How many bank booths to use'''
    booths = 10

    '''Booth worker units'''
    wu = 10

    '''Customer work units for the gaussian calculation'''
    c_mean = 5
    c_std = 0.5

    '''Create the booth instances'''
    booth_instance = generate_booths(booths, worker_unit=wu)

    '''Add all customers to a queue'''
    s = generate_queue(customers)

    '''Generate events for all customers'''
    r = generate_priority_queue(s)

    '''Average wait time with 10 booths'''
    print("Using 10 booths")
    question.average_wait_time = average_wait_time(r, booths, booth_instance)
    wu_to_hours(question.average_wait_time)
    #######################################
    '''Average wait time with 11 booths'''
    #######################################
    '''Create the booth instances'''
    booth_instance = generate_booths(booths+1, worker_unit=wu)

    '''Add all customers to a queue'''
    s = generate_queue(customers)

    '''Generate events for all customers'''
    r = generate_priority_queue(s)
    '''Average wait time with 11 booths'''
    print("Using 11 booths")
    question.average_wait_time_extra = average_wait_time(r, booths+1, booth_instance)
    wu_to_hours(question.average_wait_time_extra)

    #######################################
    '''Average wait time with 9 booths'''
    #######################################
    '''Create the booth instances'''
    booth_instance = generate_booths(booths-1, worker_unit=wu)

    '''Add all customers to a queue'''
    s = generate_queue(customers)

    '''Generate events for all customers'''
    r = generate_priority_queue(s)
    '''Average wait time with 9 booths'''
    print("Using 9 booths")
    question.average_wait_time_less = average_wait_time(r, booths-1, booth_instance)
    wu_to_hours(question.average_wait_time_less)

    #######################################
    '''Separate priority queue for light requests?'''
    #######################################
    # It's not worth it since the distribution of customer worker units is always between 4-6
    plot_graph()

    #######################################
    '''How many customers are not served at all within an operating day?'''
    #######################################
    '''Create the booth instances'''
    booth_instance = generate_booths(booths, worker_unit=wu)

    '''Add all customers to a queue'''
    s = generate_queue(customers)

    '''Generate events for all customers'''
    r = generate_priority_queue(s)
    '''Customers not served today'''
    print("Customers not served in 8 hours?")
    print("\t", question.customers_not_served_today)

    #######################################
    '''How long would it take to serve 160 customers with 1 booth?'''
    #######################################
    '''Create the booth instances'''
    booth_instance = generate_booths(1, worker_unit=wu)

    '''Add all customers to a queue'''
    s = generate_queue(customers)

    '''Generate events for all customers'''
    r = generate_priority_queue(s)
    '''Average wait time with 9 booths'''
    print("Using 1 booth with ", customers, "customers")
    question.days_to_finish_customer_160 = average_wait_time(r, 1, booth_instance)
    wu_to_hours(question.days_to_finish_customer_160)
    days = _wu_to_hours(question.days_to_finish_customer_160) / 8
    print("\tIt would take", days, "days to finish the queue")
    #######################################
    '''How long would it take to serve 160 customers with 160 booths?'''
    #######################################
    '''Create the booth instances'''
    booth_instance = generate_booths(160, worker_unit=wu)

    '''Add all customers to a queue'''
    s = generate_queue(customers)

    '''Generate events for all customers'''
    r = generate_priority_queue(s)
    '''Average wait time with 9 booths'''
    print("Using 160 booths")
    question.wait_to_finish_booth_160 = average_wait_time(r, 160, booth_instance)
    wu_to_hours(question.wait_to_finish_booth_160)
