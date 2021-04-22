import enum
import queue

import numpy
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import bar
from scipy import stats


class Customer:
    """Customer model"""

    def __init__(self, name, work_unit):
        """Customer name/id"""
        self.id = name
        """Customer's work unit"""
        self.wu = work_unit

    """This is used to compare priority (order) inside the priority queue"""
    def __lt__(self, other):
        self_priority = (self.id, self.wu)
        other_priority = (other.id, other.wu)
        return self_priority < other_priority

    def get_wu(self):
        return self.wu


class EventModel:
    def __init__(self):
        self.id = None
        self.arrival = None
        self.exit = None
        self.work_time = None
        self.event_list = []

    def add(self, id_, arrival_, work_, exit_):
        self.id = id_
        self.arrival = arrival_
        self.work_time = work_
        self.exit = exit_
        self.event_list.append(self)

    def print_all(self):
        for i in self.event_list:
            print("Customer", i.id, "\b) Arrival:", round(i.arrival, 3),
                  "Booth Time:", round(i.work_time, 3),
                  "Leave", round(i.arrival + i.work_time, 3))

    def print_current(self):
        print("Customer", self.id, "\b) Arrival:", round(self.arrival, 3),
              "Booth Time:", round(self.work_time, 3),
              "Leave", round(self.arrival + self.work_time, 3))


class InOutEvent:
    def __init__(self, print_bool):
        self.finish = 0.0
        self.start = 0.0
        self.offset = 0.0
        self.customer = None
        self.average = 0.0
        self.print = print_bool
        self.event_model = EventModel()

    def add_event(self, customer, entry):
        self.customer = customer
        self.finish = customer.get_wu() + wu
        self.start = entry
        self.event_model.add(self.customer.id, self.start, self.next_event(), self.next_event() + self.start)
        if self.print:
            self.event_model.print_current()

    def next_event(self):
        return self.finish


class BoothState(enum.Enum):
    Busy = 1
    Idle = 0


class Bank:
    """Bank model"""

    def __init__(self, booth_id, customer, speed, timer, state):
        self.id = booth_id
        self.customer = customer
        self.speed = speed
        self.state = state
        self.start_customer = timer
        self.finish_customer = timer

    def booth_available(self):
        return self.state == BoothState.Idle

    def booth_busy(self):
        return self.state == BoothState.Busy

    def change_state(self, state):
        self.state = state

    def help_customer(self, customer):
        self.customer = customer
        self.finish_customer += customer.wu + wu
        self.change_state(BoothState.Busy)

    def update_booth(self):
        self.change_state(BoothState.Idle)

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
        """Adding a customer to a PQ"""
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
        for i1 in self.list:
            print(i1)

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
    """Question variables"""

    def __init__(self):
        self.customers_not_served_today = None
        self.days_to_finish_customer_160 = None
        self.average = None


def generate_priority_queue(n):
    """
    :rtype: CustomerList
    """
    pq = CustomerListPQ()
    _list = n
    for i in range(0, _list.size()):
        new_customer = _list.get_customer()
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
        # Adding customer to a normal queue with a known worker unit ~N(5, 0.5)
        c_wu = generate_gaussian_wu(c_mean, c_std)
        new_customer = Customer(i, c_wu)
        qq.add_customer(new_customer)
    return qq


def generate_booths(n, worker_unit):
    booth_instances = []
    for i in range(0, n):
        booth = Bank(booth_id=i, customer=-1, speed=worker_unit, timer=0, state=BoothState.Idle)
        booth_instances.append(booth)
    return booth_instances


def get_normal_distribution(x, mean, sd):
    prob_density = (numpy.pi * sd) * numpy.exp(-0.5 * ((x - mean) / sd) ** 2)
    return prob_density


def get_dist_output():
    x = numpy.linspace(5, 15, 200)
    mean = 5
    sd = 0.5
    dist = get_normal_distribution(x, mean, sd)
    return dist


def process_customer_queue(qq, booth_list, work_units, events):
    while qq.size() != 0:
        for i in range(0, len(booth_list)):
            if booth_list[i].booth_available() and qq.size() > 0:
                customer = qq.get_customer()
                booth_list[i].help_customer(customer)
                events.add_event(customer, booth_list[i].start_customer)
                booth_list[i].start_customer += events.next_event()
                if events.offset <= work_units * work_hours:
                    question.customers_not_served_today = qq.size()
            else:
                booth_list[i].update_booth()
                if events.offset <= work_units * work_hours:
                    question.customers_not_served_today = qq.size()
        if booth_list[0].booth_busy():
            events.offset += events.next_event()
            events.average += events.start
    question.days_to_finish_customer_160 = events.offset
    question.average = events.average
    print("\tTime to finish all events:", round(_wu_to_hours(events.offset, work_units), 3),
          "hours\n\tAverage customer wait time:",
          round(_wu_to_hours(events.average/customers, work_units), 3), "hours")
    print("\tCustomers not served today ("+work_hours.__str__()+" hour shift):", question.customers_not_served_today)


def _wu_to_hours(wu_input, wu_efficiency):
    hours = wu_input / wu_efficiency
    return hours


def normal_dist(x, mean, sd):
    prob_density = (np.pi * sd) * np.exp(-0.5 * ((x - mean) / sd) ** 2)
    return prob_density


def plot_dist_graph():
    # Creating a series of data of in range of [5-15].
    x = np.linspace(5, 15, 200)

    # Calculate mean and Standard deviation.
    # mean = np.mean(x)
    # sd = np.std(x)
    # using ~N(5,0.5)
    mean = 5
    sd = 0.5

    # Generate PDF
    pdf = normal_dist(x, mean, sd)

    # Plot
    plt.plot(x, pdf, color='red')
    plt.xlabel('~N(5, 0.5)')
    plt.ylabel('Probability Density')
    plt.show()


def plot_graph():
    # Create graph of increasing booths with a static 10wu
    bar(booth_count, time_taken, width=0.8, bottom=None)
    plt.axhline(np.mean(time_taken), color='k', linestyle='dashed', linewidth=1)
    plt.text(161, np.mean(time_taken), "{:.0f}".format(np.mean(time_taken)), color="red", ha="right", va="center")
    plt.xlabel('Booth Count')
    plt.ylabel('Time taken (hours)')
    plt.show()


def plot_wu_graph():
    # Create a graph of increasing booth wu with a static 10 booths
    bar(wu_val, time_taken, width=0.8, bottom=None)
    plt.axhline(np.mean(time_taken), color='k', linestyle='dashed', linewidth=1)
    plt.text(250, np.mean(time_taken), "{:.0f}".format(np.mean(time_taken)), color="red", ha="right", va="center")
    plt.xlabel('Booth Worker Unit Efficiency')
    plt.ylabel('Time taken (hours)')
    plt.show()


def simulate_bank(customers_, booths_, work_units_, print_message_, print_bool_):
    """Simulate a bank"""

    '''Create the booths'''
    booth_instance_ = generate_booths(booths_, worker_unit=work_units_)

    '''Handle customer entry and exit events'''
    events_ = InOutEvent(print_bool_)

    '''Add all customers to a queue'''
    fifo_queue = generate_queue(customers_)

    '''Handle events for all customers'''
    priority_queue = generate_priority_queue(fifo_queue)

    '''Print messages and process the queue'''
    print(print_message_)
    process_customer_queue(priority_queue, booth_instance_, work_units_, events_)


if __name__ == '__main__':
    '''Class container for question answers'''
    question = Questions()

    '''Graph data arrays'''
    time_taken = []
    booth_count = []
    wu_val = []

    '''How many hours are in a work day'''
    work_hours = 8

    '''How many total customers to process in a work day'''
    customers = 160

    '''How many bank booths to use'''
    booths = 10

    '''Booth worker units'''
    wu = 10

    '''Customer work units for the gaussian calculation'''
    c_mean = 5
    c_std = 0.5

    '''Using 10 booths'''
    simulate_bank(customers, booths, wu, "Using 10 booths", True)

    '''Using 11 booths'''
    simulate_bank(customers, booths+1, wu, "Using 11 booths", False)

    '''Using 9 booths'''
    simulate_bank(customers, booths - 1, wu, "Using 9 booths", False)

    '''Separate priority queue for light requests?'''
    # It's not worth it since the distribution of customer worker units is always between 4-6
    plot_dist_graph()

    '''How long would it take to serve 160 customers with 1 booth?'''
    simulate_bank(customers, 1, wu, "Using 1 booth with " + customers.__str__() + " customers", False)
    days = _wu_to_hours(question.days_to_finish_customer_160, wu) / work_hours
    print("\tIt would take", round(days, 3), "days ("+work_hours.__str__()+" hour days) to finish the queue")

    '''How long would it take to serve 160 customers with 160 booths?'''
    simulate_bank(customers, 160, wu, "Using 160 booths", False)

    '''Difference between increasing booths vs worker units?'''
    simulate_bank(customers, booths, wu + 40, "Using 10 booths and 50wu", False)
    simulate_bank(customers, booths + 40, wu, "Using 50 booths and 10wu", False)
    simulate_bank(customers, booths, wu, "Using 10 booths and 10wu", False)

    '''Generate Booth Graph Efficiency'''
    for j in range(10, 161):
        simulate_bank(customers, j, wu, "Using "+j.__str__()+" booths and 10wu", False)
        time_taken.append(_wu_to_hours(question.average, wu))
        booth_count.append(j)
        wu_val.append(wu)
    plot_graph()

    '''Generate Worker Unit Efficiency'''
    # Reset arrays
    time_taken = []
    booth_count = []
    wu_val = []
    for k in range(10, 250):
        simulate_bank(customers, booths, k, "Using 10 booths and " + k.__str__()+"wu", False)
        time_taken.append(_wu_to_hours(question.average, k))
        booth_count.append(booths)
        wu_val.append(k)
    plot_wu_graph()
