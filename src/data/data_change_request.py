import csv
from src.data.index_reformat_csv import index_in_csv
import json

with open('src\\config\\config.json', 'r') as f:
    config = json.load(f)


# Method of searching indexes in a list referring to the searched string.
def find_element(element: str, data: list) -> int:
    for index, i in enumerate(data):
        if element in i.lower():
            return index


class RequestCSV(object):
    def __init__(self) -> None:
        """
        Database directory and system startup.
        """
        self.filename = config['database']

    def csv_post(self, year: int, title: str, studios: str, producers: str, winner: str) -> None:
        """
        Method of adding new data to the database (POST)
        """
        with open(self.filename, 'rt') as f_id:
            # Reading the database and adding it to memory.
            reader_id = list(csv.reader(f_id, delimiter=config['delimiter']))
            # Calculation of the id of the new data to be included.
            new_id = int(reader_id[len(reader_id) - 1][find_element('id', reader_id[0])]) + 1

        with open(self.filename, 'a', newline='') as f:
            # Defining the 'writer' object and adding a new line with the corresponding id.
            writer = csv.writer(f, delimiter=config['delimiter'])
            header_input = [new_id, year, title, studios, producers, winner]
            header_names = ['id', 'year', 'title', 'studios', 'producers', 'winner']
            # empty list with generated to fetch the corresponding indices of each column in the csv database.
            # This method allows that, if new databases are included in the API, the algorithm will recognize where
            # each data entry will be made.
            df = ['' for i in range(6)]
            for n, element in enumerate(header_names):
                df[find_element(element, reader_id[0])] = header_input[n]

            writer.writerow(df)
            f.close()

    def csv_2_list(self) -> list:
        """
        Read from the database (GET)
        """
        with open(self.filename, 'rt', newline='') as f:
            reader = list(csv.reader(f, delimiter=config['delimiter']))
            f.close()
        return reader

    def csv_put(self, id_c: int, year, title: str, studios: str, producers: str, winner: str) -> None:
        """
        Method of updating existing data in the database (PUT)
        """
        with open(self.filename, 'rt') as f:
            # Reading the database and adding it to memory.
            reader = list(csv.reader(f, delimiter=config['delimiter']))
        with open(self.filename, 'w') as file:
            # Defining the 'writer' object and rewriting the header.
            writer = csv.writer(file, delimiter=config['delimiter'], lineterminator='\n')
            writer.writerow(reader[0])

            # Below method is intended to replace parameters in database data. When the input is 'NONE', the data
            # will be preserved.
            # The method used aims to manage the processing resources used to carry out such an operation.
            id_index = find_element('id', reader[0])
            for line in reader[1:len(reader)]:
                if id_c == int(line[id_index]):
                    new_line = ['' for i in range(6)]
                    new_line[find_element('id', reader[0])] = line[id_index]

                    header_input = [year, title, studios, producers, winner]
                    header_names = ['year', 'title', 'studios', 'producers', 'winner']

                    for n, element in enumerate(header_input):
                        new_line[find_element(header_names[n], reader[0])] = \
                            line[find_element(header_names[n], reader[0])] if element == 'NONE' else element

                    writer.writerow(new_line)
                else:
                    writer.writerow(line)

    def csv_delete(self, id_dt: int) -> None:
        """
        Delete data from the database (DELETE)
        """
        with open(self.filename, 'rt') as f:
            # Reading the database and adding it to memory.
            reader = list(csv.reader(f, delimiter=config['delimiter']))
        with open(self.filename, 'w') as file:
            # Defining the 'writer' object and rewriting the header.
            writer = csv.writer(file, delimiter=config['delimiter'], lineterminator='\n')

            header_name = ['id', 'year', 'title', 'studios', 'producers', 'winner']
            id_index = find_element('id', reader[0])

            # The code below rewrites the data that is not the given id, generating a new database without the file
            # that was requested to be deleted.
            writer.writerow(header_name)
            for line in reader[1::]:
                if int(line[id_index]) != id_dt:
                    new_line = ['' for _ in range(6)]
                    for names in header_name:
                        new_line[find_element(names, reader[0])] = line[find_element(names, reader[0])]
                    writer.writerow(new_line)

        # As the file was only rewritten, the ids were not rewritten. The code below deletes the id column and
        # then rewrites it again.
        with open(self.filename, 'rt') as source:
            reader = list(csv.reader(source, delimiter=config['delimiter']))
            id_index = find_element('id', reader[0])
            with open(self.filename, 'w') as result:
                writer = csv.writer(result, delimiter=config['delimiter'], lineterminator='\n')
                for r in reader:
                    del r[id_index]
                    writer.writerow(r)

        # Rewrite the id.
        index_in_csv(self.filename)
