import csv


def read_csv_file(filepath):
    """Reads a csv file.
    read_csv_file(filepath)
    returns: InteractiveDataSet"""

    x = list()
    ysets = list()

    with open(filepath, 'r') as csv_in:
        reader = csv.reader(csv_in, delimiter=';')
        headers = reader.__next__()  # first line are column names
        num_datasets = len(headers) - 1  # minus one because first column is the "x axis"

        for _ in range(num_datasets):  # add the required number of sublists to ysets (one per dataset)
            ysets.append(list())

        for row in reader:
            x.append(float(row[0]))  # copy the x value into it's list

            for i in range(num_datasets):
                ysets[i].append(float(row[i + 1]))  # copy each y value into it's respective list

        csv_in.close()

    return headers, x, ysets


def write_csv_file(dataset, outfile):
    """Writes the newest data from active tree of a given InteractiveDataSet into a csv file.
    write_csv_file(dataset, filepath)"""

    # TODO: currently only writes the active tree
    with open(outfile, 'w') as csv_out:
        writer = csv.writer(csv_out, delimiter=';')
        writer.writerow([dataset.xname, dataset.active.name])  # row headers
        for x, y in zip(*dataset.active.getNewest().getData()):
            writer.writerow([x, y])
        csv_out.close()
