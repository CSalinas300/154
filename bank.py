import enum
import random
from queue import PriorityQueue


class Customer:
    """Customer model"""

    def __init__(self, name):
        self.id = name


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


class CustomerList:
    """Priority Queue"""

    def __init__(self):
        """List to print elements"""
        self.list = []
        """PriorityQueue initialization"""
        self.q = PriorityQueue()

    def add_customer(self, customer):
        self.q.put(customer.id, customer)
        self.list.append(customer.id)

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
    queue = CustomerList()
    for i in range(0, n):
        new_customer = Customer(i)
        queue.add_customer(new_customer)
    return queue


def generate_booths(n, worker_unit):
    booth_instances = []
    for i in range(0, n):
        booth = Bank(booth_id=i, customer=-1, speed=worker_unit, state=BoothState.Idle)
        booth_instances.append(booth)
    return booth_instances


def average_wait_time(q):
    # Total average wait time in 8 hours
    total_average = 0
    while q.size() != 0:
        '''Wait time for each customer rush of 5-15'''
        wait_time = 0

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
            remaining_list = customer_rush - 10
            '''Add the remaining customers to the booths'''
            booth_list = add_n_booths(remaining_list, q)
            for k in range(0, remaining_list):
                wait_time += booth_list[k].speed
        else:
            '''The rush of customers is less than our booth count so no problem'''
            booth_list = add_n_booths(customer_rush, q)
            for n in range(0, customer_rush):
                wait_time += booth_list[n].speed
        print("Average wait time for ", customer_rush, " customers: ",  wait_time / booths, " minutes")
        total_average += wait_time
    print("\tTotal average wait time in 8 hours: ", total_average/customers, " minutes")


def average_wait_time2(r):
    # Total average wait time in 8 hours
    total_average = 0

    while r.size() != 0:
        '''Wait time for each customer rush of 5-15'''
        wait_time = 0

        # 5 to 15 customers per run
        '''WU is time to finish not customer rush 10wu = 1hr'''
        customer_rush = random.randint(5, 15)
        '''If we get more than 10 customers some have to wait longer for a slot to open up'''
        if customer_rush > 10:
            '''Initially add 10 customers to all the booths'''
            process_customers(size=10, booth_list=booth_instance, queue=r)
            for n in range(0, len(booth_instance)):
                '''Add the wait time for each booth speed (10)'''
                wait_time += booth_instance[n].speed
            '''The remaining customers are in line'''
            remaining_list = customer_rush - 10
            '''Add the remaining customers to the booths'''
            process_customers(size=remaining_list, booth_list=booth_instance, queue=r)
            for n in range(0, remaining_list):
                wait_time += booth_instance[n].speed
        else:
            '''The rush of customers is less than our booth count so no problem'''
            process_customers(size=customer_rush, booth_list=booth_instance, queue=r)
            for n in range(0, customer_rush):
                wait_time += booth_instance[n].speed
        print("[2] Average wait time for ", customer_rush, " customers: ",  wait_time / booths, " minutes")
        total_average += wait_time
    print("\t[2] Total average wait time in 8 hours: ", total_average/customers, " minutes")


def add_n_booths(size, queue):
    booth_list = []
    for i in range(0, size):
        '''Same worker unit for each bank is 10'''
        internal_wu = 10
        booth = Bank(booth_id=i, customer=queue.get_customer(), speed=internal_wu, state=BoothState.Busy)
        booth_list.append(booth)
    return booth_list


def process_customers(size, booth_list, queue):
    for i in range(0, size):
        if booth_list[i].booth_available():
            customer = queue.get_customer()
            booth_list[i].help_customer(customer)
        else:
            booth_list[i].change_state(BoothState.Idle)
            customer = queue.get_customer()
            booth_list[i].help_customer(customer)


if __name__ == '__main__':
    '''How many total customers to process in a given (8 hour) day'''
    customers = 160

    '''How many bank booths to use'''
    booths = 10

    '''Static worker unit'''
    wu = 10

    '''Create the booth instances'''
    booth_instance = generate_booths(booths, worker_unit=wu)

    '''Add all customers to a not PQ'''
    q = generate_priority_queue(customers)

    '''One PQ for events'''
    '''TODO: fix PQ to reflect from a Gaussian model'''

    '''Another instance for another version'''
    r = generate_priority_queue(customers)

    '''Average waiting time for customers'''
    average_wait_time(q)

    '''Average wait time 2 using states and a single bank instance'''
    average_wait_time2(r)
