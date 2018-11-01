# postprocessing of data received from image recognition
# order in csv file: speed, rpm, gear, brake, throttle, frame

from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import os
import copy


def strip_spaces(data):
    # d: list
    # strip als space chars from data
    for i in range(len(data)):
        data[i] = data[i].replace(' ', '')
    return data


def to_float(data):
    # convert a list of strings to integers
    for i in range(len(data)):
        data[i] = float(data[i])
    return data


def to_string(data):
    # convert a list of values to strings
    for i in range(len(data)):
        data[i] = str(data[i])
    return data


def derive(data):
    # calculates the rate of change from a list of points
    # returns a list of same length containing the derived values
    derivative = [0, ]
    last_point = data[0]

    for i in range(1, len(data)):
        point = data[i]
        delta = point - last_point
        derivative.append(delta)
        last_point = point
    return derivative


def sign(a):
    # return the sign of a number
    if a > 0:
        return 1
    elif a < 0:
        return -1
    else:
        return 0


def find_spikes(data, pos_max=15, neg_max=-40):
    # check for changes in the derived data which are bigger than pos_max/neg_max
    error_seg = list()
    for i in range(len(data)):
        if data[i] > pos_max or data[i] < neg_max:
            i_start = i
            data_tmp = 0
            while data_tmp == 0:
                i += 1
                data_tmp = data[i]
            i_end = i
            error_seg.append([i_start, i_end])

    return error_seg


def get_points_of_change(data, min_neg_change=-1):
    # searches for points where the sign of data changes
    # min_decel can be set so that a simple switch from psotive to negative is not enough
    #   but the value needs to be at least as small as min_decel (useful for filtering lift and cost)
    previous_sign = 0
    points_of_change = list()

    for i in range(len(data)):
        current_sign = sign(data[i])
        if current_sign != previous_sign and current_sign != 0:
            if 0 > data[i] > min_neg_change:
                continue

            points_of_change.append(i)
            previous_sign = current_sign

    return points_of_change


class MatplotUserInput:
    # class for retrieving user input data from pyplot window
    # first/second/... are called as button callbacks; script later reads response value
    # plt.close() makes plot close on button click
    response = None

    def first(self, *args):
        self.response = 1
        plt.close()

    def second(self, *args):
        self.response = 2
        plt.close()

    def both(self, *args):
        self.response = 3
        plt.close()

    def none(self, *args):
        self.response = -1
        plt.close()


def userinput_filter_points_of_change(data, points_o_c, i):
    # calculate min and max value of the area to be viewed
    # area is +-100 around the problem region but limited to zero or max if necessary
    x_view_min = points_o_c[i] - 100 if points_o_c[i] - 100 > 0 else 0
    x_view_max = points_o_c[i + 2] + 100 if points_o_c[i + 2] + 100 < len(data) else len(data)
    # set the x and y data to be plotted from area size
    x = range(x_view_min, x_view_max)
    y = data[x_view_min:x_view_max]
    # calculate min and max y axis value from y data for purpose of scaling the plot
    y_view_min = min(k for k in y) * 0.9
    y_view_max = max(k for k in y) * 1.1

    # add some vertical red bars to clearly mark the region of error
    bar_1 = [[points_o_c[i] - 3, points_o_c[i] - 3], [y_view_min, y_view_max]]
    bar_2 = [[points_o_c[i + 1], points_o_c[i + 1]], [y_view_min, y_view_max]]
    bar_3 = [[points_o_c[i + 2] + 3, points_o_c[i + 2] + 3], [y_view_min, y_view_max]]
    # plot all the stuff
    # plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y)
    ax.plot(bar_1[0], bar_1[1], 'r')
    ax.plot(bar_2[0], bar_2[1], 'r')
    ax.plot(bar_3[0], bar_3[1], 'r')

    # initalize a response class; it's subfunctions are set as button callback
    response = MatplotUserInput()

    # define an axis per button, add button to axis, add callback functio
    first_button_ax = fig.add_axes([0.5, 0.01, 0.09, 0.04])
    first_button = plt.Button(first_button_ax, 'First', hovercolor='0.975')
    first_button.on_clicked(response.first)

    second_button_ax = fig.add_axes([0.6, 0.01, 0.09, 0.04])
    second_button = plt.Button(second_button_ax, 'Second', hovercolor='0.975')
    second_button.on_clicked(response.second)

    both_button_ax = fig.add_axes([0.7, 0.01, 0.09, 0.04])
    both_button = plt.Button(both_button_ax, 'Both', hovercolor='0.975')
    both_button.on_clicked(response.both)

    none_button_ax = fig.add_axes([0.8, 0.01, 0.09, 0.04])
    none_button = plt.Button(none_button_ax, 'None', hovercolor='0.975')
    none_button.on_clicked(response.none)

    # also add some text that tells the user what's the problem
    # is added to none_button_ax because it needs an axes... so I just used that one
    none_button_ax.text(-7.5, 0.01, 'Two spikes in short succession!\nWhich area needs to be removed?',
                        fontsize=9, color='red')
    # show plot, button clicks automatically close the window by calling plt.close() from response class
    plt.show()

    return response.response


def filter_points_of_change(points_o_c, data_speed, data_deriv, min_sector=5):
    # filters a list of points of change
    # if to points in this list are closer together than min_sector, those points are dismissed
    # function returns a list of relevant points and a list with pairs of error points
    relevant_points = list()
    error_segments = list()
    # exclude_next = False

    # for i in range(len(points_o_c) - 1):
    i = 0
    while i < len(points_o_c) - 1:
        # if exclude_next:
        #     exclude_next = False
        #     continue

        if points_o_c[i + 1] - points_o_c[i] > min_sector:
            relevant_points.append(points_o_c[i])
            i += 1
        else:
            # check wether another point of change still exist
            # then check whether the point and the one after that are further apart than min_sector
            if len(points_o_c) > i+2 and points_o_c[i + 2] - points_o_c[i + 1] < min_sector \
                    and not (abs(data_deriv[points_o_c[i]]) < 5 or abs(data_deriv[points_o_c[i+1]]) < 5):
                # we now have two sectors which are shorter than allowed following each other
                # this can be caused by two following errors OR one error being close to a correct point
                # these two cases are very difficult to distinguish an can't be hnadled in software currently
                # therefore the script plots the concerning region and ask for help

                response = userinput_filter_points_of_change(data_speed, points_o_c, i)

                if response == 1:
                    # delete first
                    error_segments.append((points_o_c[i], points_o_c[i+1]))
                    i += 3  # skip over both
                elif response == 2:
                    # delete second
                    relevant_points.append(points_o_c[i])
                    error_segments.append((points_o_c[i+2], points_o_c[i+3]))
                    i += 3  # skip over both
                elif response == 3:
                    # delete both; only first ist deleted actively, code takes care of second one
                    error_segments.append((points_o_c[i], points_o_c[i+1]))
                    i += 2  # only skip first issue, standard check takes care of second one
                elif response == -1:
                    i += 3
            else:
                error_segments.append((points_o_c[i], points_o_c[i + 1]))
                i += 2  # skip over next point

    return relevant_points, error_segments


def bridge_error_segments(data, error_segs):
    # bridges over the specified error segments in data linearly
    # this is good enough as error segments are short and data will be smoothed later on anyways
    for seg in error_segs:
        start_value = data[seg[0]-1]
        end_value = data[seg[1] + 1]
        seg_length = seg[1] - seg[0]
        delta = end_value - start_value
        gradient = delta / seg_length

        pos_in_seg = 0
        for i in range(seg[0], seg[1]+1):
            data[i] = start_value + gradient * pos_in_seg
            pos_in_seg += 1

    return data


def interactive_spikes_by_change(data, pmax, nmax):
    data_deriv = derive(data)
    spikes = find_spikes(data_deriv, pmax, nmax)
    bridge_error_segments(data, spikes)


def interactive_spikes_by_length(data, min_length):
    data_deriv = derive(data)
    # get all points where a change from acceleration to deceleration or back occurs
    points_of_change = get_points_of_change(data_deriv)
    # filter out those segements where the change is shorter than min_sector
    # this is very likely a spike due to readout errors
    rel, error_segments = filter_points_of_change(points_of_change, data, data_deriv, min_sector=min_length)
    # bridge over those error segemnts
    bridge_error_segments(data, error_segments)


def interactive_smooth_full(data):
    data_smooth = savgol_filter(data, 15, 2)
    return data_smooth


def interactive_smooth_segmented(data, min_neg_change):
    # calculate rate of change from data
    data_deriv = derive(data)
    # search for points of change
    # min_neg_change can be set, so that only negative changes greater than it are considered important
    speed_seg_points = get_points_of_change(data_deriv, min_neg_change=min_neg_change)
    # add the first and last point of data for sake of simplicity when iterating over points later on
    speed_seg_points.insert(0, 0)
    speed_seg_points.append(len(data))

    # smooth the values using a Savitzky-Golay filter
    # only smooth from one segmentation point to the next and not the whole data
    # this way all the max and min values are kept as they are
    data_smooth = list()
    # settings for filter
    window_length = 15
    polyorder = 2

    for n in range(1, len(speed_seg_points)):
        current_point = speed_seg_points[n]
        previous_point = speed_seg_points[n-1]
        if current_point - previous_point >= window_length:
            data_smooth.extend(savgol_filter(data[previous_point:current_point], window_length, polyorder))
        else:
            # the segment to be smoothed is shorter than the filter settings allow
            # therefore we need to adapt those settings (only for the current segment)
            # first: set window length to the largest odd number that is smaller than our segment length
            length = current_point - previous_point
            if length % 2 == 0:
                length -= 1
            wl = length
            # second: make sure polyorder is smaller than window length
            if wl < polyorder:
                pl = wl - 1
            else:
                pl = polyorder
            # smooth current semgent with determined setting
            data_smooth.extend(savgol_filter(data[previous_point:current_point], wl, pl))

    return data_smooth


def read_file(path):
    csv_in = open(path, 'r')

    data = [[], [], [], [], [], []]

    for line in csv_in.readlines():
        line = line.replace('\n', '')  # strip newline character
        values = line.split('; ')
        for i in range(len(data)):
            data[i].append(values[i])

    header = []
    # extract every first item from data as these are the headers
    for i in range(len(data)):
        header.append(data[i].pop(0))

    return data, header


def write_file(data, header, path):
    with open(path, 'w') as csvfile:
        csvfile.write('; '.join(header) + '\n')
        for n in range(len(data[0])):
            d = []
            for i in range(len(data)):
                d.append(data[i][n])
            csvfile.write('; '.join(to_string(d)) + '\n')
        csvfile.close()


def interactive_mode():
    # allows to interactively postprocess data
    # every time the data is modified the changes are immediately written to the file so they can be
    # visualized in an external software
    # a undo command is available so different ways of postprocessing can easily be tried out
    # the script creates a backup of the original file wich is named filename_original.csv
    # at some point this should be replaced with a gui interface

    # promt user for filepath
    path = ''
    while not os.path.isfile(path):
        print('\nEnter path to file: ')
        path = str(input())

    data, header = read_file(path)

    # create backup file; append _original to the filename
    index_file_type = path.rfind('.')
    path_file_copy = path[:index_file_type] + '_original' + path[index_file_type:]
    write_file(data, header, path_file_copy)

    # convert all data to float and strip out space characters if any
    for i in range(len(data)):
        data[i] = to_float(strip_spaces(data[i]))

    # start of the interactive part
    command = None
    selection = None
    previous = []

    info = """
    Interactive Tool for postprocessing data.
    After selecting an option changes are immediately written to file
    so they can be visualized in a different program.
    
    Available Commands:
    \tselect \t\t\t|\tSelect which data you want to manipulate
    \tundo \t\t\t|\tUndo latest changes
    \texit \t\t\t|\tExit program
    \n\t\t1 posmax negmax |\tRemove spikes based on rate of change: posmax and negmax are the maximum amounts of change 
    \t\t\t\t\t|\twhich are not considered a spike (negmax needs to be a negative number!)
    \n\t\t2 min_length \t|\tRemove spikes based on length: 
    \t\t\t\t\t|\tIf there are less datapoint than min_length between two points of 
    \t\t\t\t\t|\tchange, that section is considered a spike
    \n\t\t3 \t\t\t\t|\tSmooth data in one go: Runs a Savitzky-Golay filter over all of the data\n
    \n\t\t4 min_neg_change|\tSmooth data in segments: Data is devided into segments, every segments starts at a local 
    \t\t\t\t\t|\tmaximum or minimum and ends at the next maximum or minimum. This keeps the values of the maximum/minimum 
    \t\t\t\t\t|\tunchanged when smoothing the data. A Savitzky-Golay filter is run over each segment.
    """

    # show the info so one knows what to do
    print(info)

    while command != 'exit':
        if command == 'select' or selection is None:
            # select dataset from csv which is to be modified
            print('\n\n Select from data by index:')
            for i in range(len(data)):
                print('\t{} - {}'.format(i, header[i]))

            while selection not in range(len(data)):
                print('Enter Number: ')
                try:
                    selection = int(input())
                except ValueError:
                    continue

            previous = []

        elif command == 'undo':
            # undo last changes
            data[selection] = previous.pop(-1)

        elif command == 'info':
            print(info)

        elif command[0] == '1':
            print('\n Removing spikes: detection by rate of change')

            # backup a copy of the current dataset in a list of all changes
            previous.append(data[selection].copy())

            options = command.split(' ')
            if len(options) == 3:
                interactive_spikes_by_change(data[selection], float(options[1]), float(options[2]))
            else:
                print('\n! invalid, syntax is: "1 posmax negmax" !')

        elif command[0] == '2':
            print('\n Removing spikes: detection by length')
            previous.append(data[selection].copy())
            options = command.split(' ')
            if len(options) == 2:
                interactive_spikes_by_length(data[selection], float(options[1]))
            else:
                print('\n! invalid: syntax is "2 min_length" !')

        elif command == '3':
            print('\n Smoothing data in one go')
            previous.append(data[selection].copy())
            data[selection] = interactive_smooth_full(data[selection])

        elif command[0] == '4':
            print('\n Smoothing data in segments')
            previous.append(data[selection].copy())
            options = command.split(' ')
            if len(options) == 2:
                data[selection] = interactive_smooth_segmented(data[selection], float(options[1]))
            else:
                print('\n! invalid: syntax is "4 min_neg_change" !')

        else:
            print('\n!! Invalid selection: Enter "info" to get availlable commands')

        write_file(data, header, path)

        print('\n Select an option: ')
        command = str(input())

    # when exiting write file again with modified headers
    # this makes it easier to seperate the original and modified dataset in other software
    for i in range(len(data)):
        header[i] = header[i] + '_p'


interactive_mode()
