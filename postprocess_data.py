# postprocessing of data received from image recognition
# order in csv file: speed, rpm, gear, brake, throttle, frame

from scipy.signal import savgol_filter
import numpy
import matplotlib.pyplot as plt


def strip_spaces(data):
    # d: list
    # strip als space chars from data
    for i in range(len(data)):
        data[i] = data[i].replace(' ', '')
    return data


def to_float(data):
    # d: list
    # convert a list of strings to integers
    for i in range(len(data)):
        data[i] = float(data[i])
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


def get_points_of_change(data, min_decel=-1):
    # searches for points where the sign of data changes
    # min_decel can be set so that a simple switch from psotive to negative is not enough
    #   but the value needs to be at least as small as min_decel (useful for filtering lift and cost)
    previous_sign = 0
    points_of_change = list()

    for i in range(len(data)):
        current_sign = sign(data[i])
        if current_sign != previous_sign and current_sign != 0:
            if 0 > data[i] > min_decel:
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


def filter_points_of_change(points_o_c, data, min_sector=5):
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
            if len(points_o_c) > i+2 and points_o_c[i + 2] - points_o_c[i + 1] < min_sector:
                # we now have two sectors which are shorter than allowed following each other
                # this can be caused by to following errors OR one error being close to a correct point
                # these two cases are very difficult to distinguish an can't be hnadled in software currently
                # therefore the script plots the concerning region and ask for help

                response = userinput_filter_points_of_change(data, points_o_c, i)

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


csv_in = open('results/out.csv', 'r')

speed_raw = list()
frames = list()

for line in csv_in.readlines():
    line = line.replace('\n', '')  # strip newline character
    values = line.split('; ')
    speed_raw.append(values[0])
    frames.append(values[5])


# process speed data
# first strip space characters that may result from OCR
speed_tmp = strip_spaces(speed_raw)
# convert strings to float
speed_tmp = to_float(speed_tmp)
# calculate the rate of change from speed data
speed_deriv = derive(speed_tmp)
# get all points where a change from acceleration to deceleration or back occurs
speed_points_of_change = get_points_of_change(speed_deriv)
# filter out those segements where the change is shorter than min_sector
# this is very likely a spike due to readout errors
rel, speed_error_segments = filter_points_of_change(speed_points_of_change, speed_tmp, min_sector=10)
# bridge over those error segemnts
bridge_error_segments(speed_tmp, speed_error_segments)

# again search for points of change; as error segments were removed this now only yields real points of change
# additionaly min_decel is set, this prevents lift and cost from being mistaken for the start of braking
speed_seg_points = get_points_of_change(speed_deriv, min_decel=-7)
# add the first and last point of data for sake of simplicity when iterating over points later on
speed_seg_points.insert(0, 0)
speed_seg_points.append(len(speed_tmp))


# smooth the speed values using a Savitzky-Golay filter
# only smooth from one segmentation point to the next and not the whole data
# this way all the max and min values are kept as they are
speed_smooth = list()
# settings for filter
window_length = 15
polyorder = 2

for n in range(1, len(speed_seg_points)):
    current_point = speed_seg_points[n]
    previous_point = speed_seg_points[n-1]
    if current_point - previous_point >= window_length:
        speed_smooth.extend(savgol_filter(speed_tmp[previous_point:current_point], window_length, polyorder))
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
        speed_smooth.extend(savgol_filter(speed_tmp[previous_point:current_point], wl, pl))


with open('results/smooth_speed.csv', 'w') as csvfile:
    for value in speed_smooth:
        csvfile.write(str(value) + '\n')
    csvfile.close()
