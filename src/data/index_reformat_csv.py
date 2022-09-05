import csv
import json

with open('src\\config\\config.json') as f:
    config = json.load(f)


def index_in_csv(path_file: str) -> None:
    """
    :param path_file: database directory.
    creates an id column if the file does not have an id column. If yes, ignore.
    """

    # Exception object to stop search engines when the goal is accomplished.
    class ExceptionPass(Exception):
        pass

    with open(path_file, 'rt') as csvfile:
        # Read csv file
        reader = list(csv.reader(csvfile, delimiter=config['delimiter']))

    # 'id' column search engine.
    # If not found, it will generate a column with the corresponding id.
    try:
        for element in reader[0]:
            if 'id'.lower() in element.lower():
                raise ExceptionPass
        with open(path_file, 'w') as new_file:
            writer = csv.writer(new_file, delimiter=config['delimiter'], lineterminator='\n')
            writer.writerow(['id'] + reader[0])
            for n, n_row in enumerate(reader[1:len(reader)]):
                writer.writerow([n] + n_row)
    except ExceptionPass:
        pass
