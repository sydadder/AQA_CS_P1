class QNode:
    def __init__(self):
        self.buyer_id = "   "
        self.waiting_time = 0
        self.items_in_basket = 0


class FinalStats:
    def __init__(self):
        self.MAX_Q_LENGTH = 0
        self.MAX_WAIT = 0
        self.TOTAL_WAIT = 0
        self.TOTAL_Q = 0
        self.TOTAL_Q_OCCURRENCE = 0
        self.TOTAL_NO_WAIT = 0

    def output_stats(self, buyer_number, simulation_time):
        print("The simulation statistics are:")
        print("==============================")
        print(f"The maximum queue length was: {self.MAX_Q_LENGTH} buyers")
        print(f"The maximum waiting time was: {self.MAX_WAIT} time units")
        print(f"{buyer_number} buyers arrived during {simulation_time} time units")
        avg_waiting_time = round(self.TOTAL_WAIT / buyer_number, 1)
        print(f"The average waiting time was: {avg_waiting_time} time units")
        if self.TOTAL_Q_OCCURRENCE > 0:
            avg_queue_length = round(self.TOTAL_Q / self.TOTAL_Q_OCCURRENCE, 2)
            print(f"The average queue length was: {avg_queue_length} buyers")
        print(f"{self.TOTAL_NO_WAIT} buyers did not need to queue")


class Simulation:
    BLANK = "   "
    MAX_Q_SIZE = 30
    MAX_TILLS = 5
    MAX_TIME = 50
    TILL_SPEED = 3

    TIME_IDLE = 0
    TIME_BUSY = 1
    TIME_SERVING = 2

    ARRIVAL_TIME = 0
    ITEMS = 1

    TOTAL_WAIT = 2
    TOTAL_Q = 3
    TOTAL_Q_OCCURRENCE = 4

    def __init__(self):
        self.tills = [[0, 0, 0] for _ in range(self.MAX_TILLS + 1)]
        self.buyer_queue = [QNode() for _ in range(self.MAX_Q_SIZE)]
        self.simulation_time = 10
        self.no_of_tills = 2
        self.data = [[0, 0] for _ in range(self.MAX_TIME + 1)]
        self.queue_length = 0
        self.buyer_number = 0
        self.stats = FinalStats()

        # Change settings
        self.change_settings()
        # Obtain data
        self.read_in_simulation_data()
        # Output Heading
        self.output_heading()

    def change_settings(self):
        print("Settings set for this simulation:")
        print("=================================")
        print(f"Simulation time: {self.simulation_time}")
        print(f"Tills operating: {self.no_of_tills}")
        print("=================================")
        print()

    def read_in_simulation_data(self):
        with open("SimulationData.txt", "r") as file_in:
            for count, data_string in enumerate(file_in, start=1):
                if count > self.MAX_TIME:
                    break
                sanitized_data = data_string.split(":")
                self.data[count][self.ARRIVAL_TIME] = int(sanitized_data[0])
                self.data[count][self.ITEMS] = int(sanitized_data[1])

    def buyer_arrives(self):
        print(f"  B{self.buyer_number}({self.data[self.buyer_number][self.ITEMS]})")
        self.buyer_joins_queue(self.buyer_number)

    def buyer_joins_queue(self, buyer_number):
        self.buyer_queue[self.queue_length].buyer_id = f"B{buyer_number}"
        self.buyer_queue[self.queue_length].items_in_basket = self.data[buyer_number][self.ITEMS]
        self.queue_length += 1

    def calculate_serving_time(self, this_till, no_of_items):
        serving_time = (no_of_items // self.TILL_SPEED) + 1
        self.tills[this_till][self.TIME_SERVING] = serving_time
        print(f"{this_till:>6d}{serving_time:>6d}")

    def serving(self):
        till_free = self.find_free_till()
        while till_free != -1 and self.queue_length > 0:
            items_in_basket = self.serve_buyer()
            self.update_stats()
            self.calculate_serving_time(till_free, items_in_basket)
            till_free = self.find_free_till()
        self.buyer_queue = self.increment_time_waiting()
        self.update_tills()
        if self.queue_length > 0:
            self.stats.TOTAL_Q_OCCURRENCE += 1
            self.stats.TOTAL_Q += self.queue_length
        if self.queue_length > self.stats.MAX_Q_LENGTH:
            self.stats.MAX_Q_LENGTH = self.queue_length
        self.output_till_and_queue_states()

    def serve_buyer(self):
        this_buyer_id = self.buyer_queue[0].buyer_id
        self.buyer_queue[0].waiting_time
        this_buyer_items = self.buyer_queue[0].items_in_basket
        for count in range(self.queue_length):
            self.buyer_queue[count].buyer_id = self.buyer_queue[count + 1].buyer_id
            self.buyer_queue[count].waiting_time = self.buyer_queue[count + 1].waiting_time
            self.buyer_queue[count].items_in_basket = self.buyer_queue[count + 1].items_in_basket
        self.buyer_queue[self.queue_length].buyer_id = self.BLANK
        self.buyer_queue[self.queue_length].waiting_time = 0
        self.buyer_queue[self.queue_length].items_in_basket = 0
        self.queue_length -= 1
        print(f"{this_buyer_id:>17s}", end="")
        return this_buyer_items

    def increment_time_waiting(self):
        for count in range(self.queue_length):
            self.buyer_queue[count].waiting_time += 1
        return self.buyer_queue

    def find_free_till(self):
        for till_number in range(1, self.no_of_tills + 1):
            if self.tills[till_number][self.TIME_SERVING] == 0:
                return till_number
        return -1

    def update_tills(self):
        for till_number in range(self.no_of_tills + 1):
            if self.tills[till_number][self.TIME_SERVING] == 0:
                self.tills[till_number][self.TIME_IDLE] += 1
            else:
                self.tills[till_number][self.TIME_BUSY] += 1
                self.tills[till_number][self.TIME_SERVING] -= 1

    def tills_busy(self):
        return any(self.tills[till_number][self.TIME_SERVING] > 0 for till_number in range(self.no_of_tills + 1))

    def update_stats(self):
        waiting_time = self.buyer_queue[0].waiting_time
        self.stats.TOTAL_WAIT += waiting_time
        if waiting_time > self.stats.MAX_WAIT:
            self.stats.MAX_WAIT = waiting_time + 1
        if waiting_time == 0:
            self.stats.TOTAL_NO_WAIT += 1

    def output_heading(self):
        print()
        print("Time Buyer  | Start Till Serve | Till Time Time Time |      Queue")
        print("     enters | serve      time  | num- idle busy ser- | Buyer Wait Items")
        print("     (items)| buyer            | ber            ving | ID    time in")
        print("            |                  |                     |            basket")

    def output_till_and_queue_states(self):
        for i in range(1, self.no_of_tills + 1):
            print(
                f"{i:>36d}{self.tills[i][self.TIME_IDLE]:>5d}{self.tills[i][self.TIME_BUSY]:>5d}{self.tills[i][self.TIME_SERVING]:>6d}"
            )
        print("                                                    ** Start of queue **")
        for i in range(self.queue_length):
            print(
                f"{self.buyer_queue[i].buyer_id:>57s}{self.buyer_queue[i].waiting_time:>7d}{self.buyer_queue[i].items_in_basket:>6d}"
            )
        print("                                                    *** End of queue ***")
        print("------------------------------------------------------------------------")

    def queue_simulator(self):
        time_to_next_arrival = self.data[self.buyer_number + 1][self.ARRIVAL_TIME]

        # Serve until closing time i.e. SimulationTime
        for time_unit in range(self.simulation_time):
            time_to_next_arrival -= 1
            print(f"{time_unit:>3d}", end="")
            if time_to_next_arrival == 0:
                self.buyer_number += 1
                self.buyer_arrives()
                time_to_next_arrival = self.data[self.buyer_number + 1][self.ARRIVAL_TIME]
            else:
                print()

            self.serving()

        # Serve remaining customers in the queue after closing hours.
        extra_time = 0
        while self.queue_length > 0:
            time_unit = self.simulation_time + extra_time
            print(f"{time_unit:>3d}")
            self.serving()
            extra_time += 1

        # Complete serving the ones on the till
        while self.tills_busy():
            time_unit = self.simulation_time + extra_time
            print(f"{time_unit:>3d}")
            self.update_tills()
            self.output_till_and_queue_states()
            extra_time += 1

        # Final Status Output of all collected stats
        self.stats.output_stats(self.buyer_number, self.simulation_time)


if __name__ == "__main__":
    simulation = Simulation()
    simulation.queue_simulator()
    # input("Press Enter to finish")
