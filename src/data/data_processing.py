import csv
import json

with open('src\\config\\config.json', 'r') as f:
    config = json.load(f)


# Exception object to stop search systems when the objective is completed.
class ExceptionPass(Exception):
    pass


class DataProcessing(object):
    def __init__(self) -> None:
        """
        DataProcessing: Aims to treat the database to return a json file with the requested format.
        Database directory and variables
        """
        self.filename = config['database']
        self.sub_file: list[list] = []
        self.reader: list = []

    def csv_reader(self) -> None:
        """
        Reading csv file in mode: open for reading (r) and text mode (t). The aim is to store the data in memory to
        speed up processing time and facilitate treatment.
        """
        with open(self.filename, 'rt') as csvfile:
            self.reader = list(csv.reader(csvfile, delimiter=config['delimiter']))
            # Store the contents of the file in memory. list()

    @staticmethod
    def and_2_comma(producer: str) -> str:
        """
        In the 'producers' column we see that there are two ways of dividing producers in the text. Separated by
        commas, 'and' and 'and, '. With this function we can have an effective separation of all producers in a
        list, facilitating the processing of information.
        """
        return producer.replace(", and ", config['producer_replace']) \
            if ', and' in producer else producer.replace(" and ", config['producer_replace'])

    @staticmethod
    def find_element(element: str, data: list) -> int:
        """
        Finds the index of the searched string in a list. Used to save processing time, being faster than dictionary
        usage.
        :param element: String to search.
        :param data: List where the string will be searched.
        """
        for index, i in enumerate(data):
            if element in i.lower():
                return index

    def producers_treatment(self) -> list[list]:
        """
        Treatment and verification of award winners.
        """
        year_index = DataProcessing.find_element(config['find_columns']['year'], self.reader[0])
        producers_index = DataProcessing.find_element(config['find_columns']['producers'], self.reader[0])
        award_index = DataProcessing.find_element(config['find_columns']['winner'], self.reader[0])

        self.reader = self.reader[1:len(self.reader)]
        for n_row in self.reader:
            if config['find_columns']['winner_condition'] in n_row[award_index].lower():
                data_producer = DataProcessing.and_2_comma(n_row[producers_index]).split(sep=config['producer_replace'])
                self.sub_file.append([int(n_row[year_index]), data_producer])
        return self.sub_file


class Clustering(object):
    def __init__(self) -> None:
        """
        Data clustering method to search for winners with the shortest and longest intervals between consecutive awards.
        Detailed method in the code for easier understanding.
        """
        self.PDT = DataProcessing()
        self.PDT.csv_reader()
        self.df: list[list] = self.PDT.producers_treatment()
        self.cluster_df: dict[str, list[int]] = {}
        self.dist_year_producer: dict[str, list[dict[int, list]]] = {}
        self.MAX, self.MIN = [], []

    def CLUSTER(self) -> None:
        # -------------------------------------------------------------------------------------------------------------#
        # SECTION 1 |--------------------------------------------------------------------------------------------------#
        # -------------------------------------------------------------------------------------------------------------#
        # -> self.df : Returns a list of producers present in the films that won the award
        # -> self.df type: [[year, [producer, ... ,producer]], [year, [producer, ... ,producer]], ...,]
        ID_M = len(self.df)
        for id_m in range(ID_M):
            # ||| PRIMARY SEARCH ||| (searches for a producer to be the research item in the secondary search)
            # -> To see it better, run the line of code below: PRINT 0
            # print(self.df[id_m][1])
            # The 'for' function below will iterate through the list items to define your primary search
            # Example: [producer, producer, ... ,producer]

            for id_s in range(len(self.df[id_m][1])):
                # -> search_by_producer: Defines which producer should be searched in the database type: str
                # -> To see it better, run the line of code below: PRINT 1
                # print(f'{self.df[id_m][1][id_s].lower()} || {self.df[id_m][0]}')
                search_by_producer = self.df[id_m][1][id_s].lower()

                try:  # MEMORY RESOURCE MANAGEMENT
                    for search_auth in self.cluster_df:
                        if search_auth == search_by_producer:
                            # !!! if the search was already done by the producer, an exception will be thrown !!!
                            # The method is intended to save the memory used in processing
                            raise ExceptionPass

                    # ||| START SECONDARY SEARCH ||| Starts the search for the same producer in the database
                    self.cluster_df[search_by_producer] = [self.df[id_m][0]]
                    # -> self.cluster_df[search_by_producer]: defines the first item in the list (the year of the
                    #                                         first award) in the dictionary with the key (key is
                    #                                         the name of the producer)
                    for id_m_search in range(ID_M):
                        # Same method used in primary research
                        for id_s_search in range(len(self.df[id_m_search][1])):
                            if (id_m, id_s) != (id_m_search, id_s_search):  # Condition for not finding the item
                                #                                             that started the search
                                # -> current_producer: Producer to compare with 'search_by_producer'
                                current_producer = self.df[id_m_search][1][id_s_search].lower()

                                if current_producer == search_by_producer:  # Simple condition to verify the producer
                                    # -> To see it better, run the line of code below (PRINT 2)
                                    # Recommended to print PRINT2 (line 92) and PRINT1 (line 66) together
                                    # print(f'     |----> {self.df[id_m_search][1][id_s_search]} '
                                    #       f'|| : {self.df[id_m_search][0]}')
                                    # -> function below append the years referring to the search in the same list
                                    self.cluster_df[search_by_producer].append(self.df[id_m_search][0])
                except ExceptionPass:  # MEMORY RESOURCE MANAGEMENT
                    pass

        # -------------------------------------------------------------------------------------------------------------#
        # SECTION 2 |--------------------------------------------------------------------------------------------------#
        # -------------------------------------------------------------------------------------------------------------#
        # Section 2 is intended to calculate the distance between the awards' data.
        for prod, year in self.cluster_df.items():
            if len(year) > 1:  # will only run if the list gets more than one data
                year.sort()  # Leave data in ascending order
                # -> To see it better, run the line of code below (PRINT 3)
                # print(prod, year)
                self.dist_year_producer[prod] = []  # Setting producer key

                for i in range(len(year) - 1):
                    # -> To see it better, run the line of code below (PRINT 4)
                    # Recommended to print PRINT3 (line 107) and PRINT4 (line 112) together
                    # print(f'     |---> {prod} |---| {year[i + 1]} - {year[i]} = {year[i + 1] - year[i]}')
                    dc_year = {year[i + 1] - year[i]: [year[i], year[i + 1]]}
                    # -> dc_year: As the list is in ascending order, the calculation is done like this:
                    #             Having a list X = [a, b, c, d] And the index being i:
                    #             X[h + 1] - X[h] -> (b-a, c-b, d-c) such that h = i - 1
                    self.dist_year_producer[prod].append(dc_year)  # Append to referring producer key

        # -------------------------------------------------------------------------------------------------------------#
        # SECTION 3 |--------------------------------------------------------------------------------------------------#
        # -------------------------------------------------------------------------------------------------------------#
        # Section 3 is intended to add an ID for each consecutive award range
        id_dict, n, list_n = {}, 0, []
        for prod, year_sys in self.dist_year_producer.items():
            # -> To see it better, run the line of code below (PRINT 5)
            # print(f' prod: {prod} |----| year_sys: {year_sys}')
            for m, year_sys_item in enumerate(year_sys):
                # to create an index based on 'sub-iterable' objects, the method was used:
                # object producer_1 = (y_1, y_2,... ,y_x) ->
                # id_1 = producer_1 (y_1[g]), id_2 = producer_1 (y_1[g+cycle]), ...
                # where cycle and g is |general object| iteration and |sub object| iteration
                # -> To see it better, run the line of code below (PRINT 6)
                # print(f' id: {n+m} || {year_sys_item} || {prod}')

                list_n.append(n + m)  # interlinked system with max(list_n) + 1 (line 136) explained above
                id_dict[n + m] = {prod: year_sys_item}
            n = max(list_n) + 1  # integrated iteration process

        # -------------------------------------------------------------------------------------------------------------#
        # SECTION 4 |--------------------------------------------------------------------------------------------------#
        # -------------------------------------------------------------------------------------------------------------#
        # Has the objective of generating a list with the intervals necessary for the completion of the algorithm
        dist_list = []
        for id_x, sys in id_dict.items():
            for producer, data in sys.items():
                for dist in data:
                    dist_list.append(dist)

        # -------------------------------------------------------------------------------------------------------------#
        # SECTION 5 |--------------------------------------------------------------------------------------------------#
        # -------------------------------------------------------------------------------------------------------------#
        # Section 5 is intended to identify the maximum and minimum range of premiums and request data from the
        # responsible producers.
        max_dst, id_list_validation_max = max(dist_list), []
        for p, dst in enumerate(dist_list):
            id_list_validation_max.append(p) if dst == max_dst else None

        min_dst, id_list_validation_min = min(dist_list), []
        for q, dst in enumerate(dist_list):
            id_list_validation_min.append(q) if dst == min_dst else None

        # -------------------------------------------------------------------------------------------------------------#
        # FINALIZATION |-----------------------------------------------------------------------------------------------#
        # -------------------------------------------------------------------------------------------------------------#
        MIN, MAX = [], []
        for id_max in id_list_validation_max:
            self.MAX.append(id_dict[id_max])
        for id_min in id_list_validation_min:
            self.MIN.append(id_dict[id_min])
        # -------------------------------------------------------------------------------------------------------------#

    def list_2_json(self) -> dict:
        """
        Conversion of the result to json.
        """
        self.CLUSTER()
        master = {"min": [], "max": []}
        for dt_MIN in self.MIN:
            master["min"].append(
                {
                    "producer": [*dt_MIN][0],
                    "interval": [*dt_MIN[[*dt_MIN][0]]][0],
                    "previousWin": dt_MIN[[*dt_MIN][0]][[*dt_MIN[[*dt_MIN][0]]][0]][0],
                    "followingWin": dt_MIN[[*dt_MIN][0]][[*dt_MIN[[*dt_MIN][0]]][0]][1]
                }
            )
        for dt_MAX in self.MAX:
            master["max"].append(
                {
                    "producer": [*dt_MAX][0],
                    "interval": [*dt_MAX[[*dt_MAX][0]]][0],
                    "previousWin": dt_MAX[[*dt_MAX][0]][[*dt_MAX[[*dt_MAX][0]]][0]][0],
                    "followingWin": dt_MAX[[*dt_MAX][0]][[*dt_MAX[[*dt_MAX][0]]][0]][1]
                }
            )
        return master



