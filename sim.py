# Skeleton Program for the AQA AS Summer 2024 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA Programmer Team
# developed in a Python 3 environment

# Version number: 0.0.1


class Q_Node:
    def __init__(self):
        self.BuyerID = "   "
        self.WaitingTime = 0
        self.ItemsInBasket = 0

class FinalStats:
    def __init__(self):
        self.MAX_Q_LENGTH = 0
        self.MAX_WAIT = 0
        self.TOTAL_WAIT = 0
        self.TOTAL_Q = 0
        self.TOTAL_Q_OCCURRENCE = 0
        self.TOTAL_NO_WAIT = 0
        self.stats = [0 for _ in range(7)]

    def output_stats(self, buyer_number, simulation_time):
        print("The simulation statistics are:")
        print("==============================")
        print(f"The maximum queue length was: {self.MAX_Q_LENGTH} buyers")
        print(f"The maximum waiting time was: {self.MAX_WAIT} time units")
        print(f"{buyer_number} buyers arrived during {simulation_time} time units")
        AverageWaitingTime = round(self.TOTAL_WAIT / buyer_number, 1)
        print(f"The average waiting time was: {AverageWaitingTime} time units")
        if self.TOTAL_Q_OCCURRENCE > 0:
            self.queue_length = round(self.TOTAL_Q / self.TOTAL_Q_OCCURRENCE, 2)
            print(f"The average queue length was: {self.queue_length} buyers")
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
    MAX_WAIT = 1
    TOTAL_Q = 3
    TOTAL_Q_OCCURRENCE = 4
    TOTAL_NO_WAIT = 5
    MAX_Q_LENGTH = 0

    def __init__(self):

        self.tills = [[0, 0, 0] for _ in range(self.MAX_TILLS + 1)]
        self.buyer_queue = [Q_Node() for _ in range(self.MAX_Q_SIZE)]
        self.simulation_time = 10
        self.no_of_tills = 2
        self.data = [[0, 0] for _ in range(self.MAX_TIME + 1)]
        self.queue_length = 0
        self.buyer_number = 0

        # Change settings
        self.change_settings()
        # obtain data
        self.read_in_simulation_data()
        # Output Heading
        self.OutputHeading()
        # FinalStats
        self.stats = FinalStats()

    def change_settings(self):
        print("Settings set for this simulation:")
        print("=================================")
        print(f"Simulation time: {self.simulation_time}")
        print(f"Tills operating: {self.no_of_tills}")
        print("=================================")
        print()
        # answer = input("Do you wish to change the settings?  Y/N: ")
        # if answer == 'Y':
        #     print(f"Maximum simulation time is {self.MAX_TIME} time units")
        #     simulation_time = int(input("Simulation run time: "))
        #     while simulation_time > self.MAX_TIME or simulation_time < 1:
        #         print(f"Maximum simulation time is {self.MAX_TIME} time units")
        #         simulation_time = int(input("Simulation run time: "))
        #     print(f"Maximum number of tills is {self.MAX_TILLS}")
        #     no_of_tills = int(input("Number of tills in use: "))
        #     while no_of_tills > self.MAX_TILLS or no_of_tills < 1:
        #         print(f"Maximum number of tills is {self.MAX_TILLS}")
        #         no_of_tills = int(input("Number of tills in use: "))
        return self.simulation_time, self.no_of_tills

    def read_in_simulation_data(self):
        FileIn = open("SimulationData.txt", "r")
        DataString = FileIn.readline()
        Count = 0
        while DataString != "" and Count < self.MAX_TIME:
            Count += 1
            SanitizedData = DataString.split(":")
            self.data[Count][self.ARRIVAL_TIME] = int(SanitizedData[0])
            self.data[Count][self.ITEMS] = int(SanitizedData[1])
            DataString = FileIn.readline()
        FileIn.close()
        return self.data

    #####
    ##### THE BUYER #####
    #####

    def buyer_arrives(self):
        print(f"  B{self.buyer_number}({self.data[self.buyer_number][self.ITEMS]})")
        self.buyer_joins_queue(self.buyer_number)
        return

    def buyer_joins_queue(self, buyer_number):
        self.buyer_queue[self.queue_length].BuyerID         = f"B{buyer_number}"
        self.buyer_queue[self.queue_length].ItemsInBasket   = self.data[buyer_number][self.ITEMS]
        self.queue_length += 1
        return


    #####
    ##### SERVICE #####
    #####

    def CalculateServingTime(self,ThisTill, NoOfItems):
        ServingTime = (NoOfItems // self.TILL_SPEED) + 1
        self.tills[ThisTill][self.TIME_SERVING] = ServingTime
        print(f"{ThisTill:>6d}{ServingTime:>6d}")
        return

    def serving(self):
        TillFree = self.FindFreeTill()
        while TillFree != -1 and self.queue_length > 0:
            ItemsInBasket = self.serve_buyer()
            self.UpdateStats()
            self.CalculateServingTime(TillFree, ItemsInBasket)
            TillFree = self.FindFreeTill()
        self.buyer_queue = self.IncrementTimeWaiting()
        self.UpdateTills()
        if self.queue_length > 0:
            self.stats.TOTAL_Q_OCCURRENCE += 1
            self.stats.TOTAL_Q += self.queue_length
        if self.queue_length > self.stats.MAX_Q_LENGTH:
            self.stats.MAX_Q_LENGTH = self.queue_length
        self.OutputTillAndQueueStates()
        return

    def serve_buyer(self):
        ThisBuyerID = self.buyer_queue[0].BuyerID
        self.buyer_queue[0].WaitingTime
        ThisBuyerItems = self.buyer_queue[0].ItemsInBasket
        for Count in range(self.queue_length):
            self.buyer_queue[Count].BuyerID = self.buyer_queue[Count + 1].BuyerID
            self.buyer_queue[Count].WaitingTime = self.buyer_queue[Count + 1].WaitingTime
            self.buyer_queue[Count].ItemsInBasket = self.buyer_queue[Count + 1].ItemsInBasket
        self.buyer_queue[self.queue_length].BuyerID = self.BLANK
        self.buyer_queue[self.queue_length].WaitingTime = 0
        self.buyer_queue[self.queue_length].ItemsInBasket = 0
        self.queue_length -= 1
        print(f"{ThisBuyerID:>17s}", end="")
        return ThisBuyerItems

    def IncrementTimeWaiting(self):
        for Count in range(self.queue_length):
            self.buyer_queue[Count].WaitingTime += 1
        return self.buyer_queue

    def FindFreeTill(self):
        FoundFreeTill = False
        TillNumber = 0
        while not FoundFreeTill and TillNumber < self.no_of_tills:
            TillNumber += 1
            if self.tills[TillNumber][self.TIME_SERVING] == 0:
                FoundFreeTill = True
        if FoundFreeTill:
            return TillNumber
        else:
            return -1

    def UpdateTills(self):
        for TillNumber in range(self.no_of_tills + 1):
            if self.tills[TillNumber][self.TIME_SERVING] == 0:
                self.tills[TillNumber][self.TIME_IDLE] += 1
            else:
                self.tills[TillNumber][self.TIME_BUSY] += 1
                self.tills[TillNumber][self.TIME_SERVING] -= 1
        return self.tills

    def TillsBusy(self):
        IsBusy = False
        TillNumber = 0
        while not IsBusy and TillNumber <= self.no_of_tills:
            if self.tills[TillNumber][self.TIME_SERVING] > 0:
                IsBusy = True
            TillNumber += 1
        return IsBusy


    #####
    ##### THE STATS ####
    #####

    def UpdateStats(self):
        self.stats.TOTAL_WAIT += self.buyer_queue[0].WaitingTime
        if self.buyer_queue[0].WaitingTime > self.stats.MAX_WAIT:
            self.stats.MAX_WAIT = self.buyer_queue[0].WaitingTime
        if self.buyer_queue[0].WaitingTime == 0:
            self.stats.TOTAL_NO_WAIT += 1
        return self.stats

    #####
    ##### OUTPUTS #######
    #####

    def OutputHeading(self):
        print()
        print("Time Buyer  | Start Till Serve | Till Time Time Time |      Queue")
        print("     enters | serve      time  | num- idle busy ser- | Buyer Wait Items")
        print("     (items)| buyer            | ber            ving | ID    time in")
        print("            |                  |                     |            basket")

    def OutputTillAndQueueStates(self):
        for i in range(1, self.no_of_tills + 1):
            print(
                f"{i:>36d}{self.tills[i][self.TIME_IDLE]:>5d}{self.tills[i][self.TIME_BUSY]:>5d}{self.tills[i][self.TIME_SERVING]:>6d}"
            )
        print("                                                    ** Start of queue **")
        for i in range(self.queue_length):
            print(
                f"{self.buyer_queue[i].BuyerID:>57s}{self.buyer_queue[i].WaitingTime:>7d}{self.buyer_queue[i].ItemsInBasket:>6d}"
            )
        print("                                                    *** End of queue ***")
        print("------------------------------------------------------------------------")

    ####
    #### THE SIMULATOR ####
    ####

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
        ExtraTime = 0
        while self.queue_length > 0:
            time_unit = self.simulation_time + ExtraTime
            print(f"{time_unit:>3d}")
            self.serving()
            ExtraTime += 1

        # Complete serving the ones on the till
        while self.TillsBusy():
            time_unit = self.simulation_time + ExtraTime
            print(f"{time_unit:>3d}")
            self.UpdateTills()
            self.OutputTillAndQueueStates()
            ExtraTime += 1

        # Final Status Output of all collected stats
        self.stats.output_stats(self.buyer_number, self.simulation_time)


if __name__ == "__main__":
    simulation = Simulation()
    simulation.queue_simulator()
    #input("Press Enter to finish")
