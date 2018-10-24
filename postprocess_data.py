# postprocessing of data received from image recognition
# order in csv file: speed, rpm, gear, brake, throttle, frame

from scipy.signal import savgol_filter
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


def filter_points_of_change(data, min_sector):
    # filters a list of points of change
    # if to points in this list are closer together than min_sector, those points are dismissed
    # TODO probable Issue when an error point and a correct point are too close together
    # function returns a list of relevant points and a list with pairs of error points
    relevant_points = list()
    error_segments = list()
    exclude_next = False

    for i in range(len(data)-1):
        if exclude_next:
            exclude_next = False
            continue

        if data[i+1] - data[i] > min_sector:
            relevant_points.append(data[i])
        else:
            error_segments.append((data[i], data[i+1]))
            exclude_next = True

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
rel, speed_error_segments = filter_points_of_change(speed_points_of_change, min_sector=10)
# bridge over those error segemnts
bridge_error_segments(speed_tmp, speed_error_segments)

# again search for points of change; as error segments were removed this now only yields real points of change
# additionaly min_decel is set, this prevents lift and cost from being mistaken for the start of braking
speed_seg_points = get_points_of_change(speed_deriv, min_decel=-7)
# add the very last point of data for sake of simplicity when iterating over points later on
speed_seg_points.append(len(speed_tmp))


# smooth the speed values using a Savitzky-Golay filter
# only smooth from one segmentation point to the next and not the whole data
# this way all the max and min values are kept as they are
speed_smooth = list()
# settings for filter
window_length = 15
polyorder = 2

for i in range(1, len(speed_seg_points)):
    current_point = speed_seg_points[i]
    previous_point = speed_seg_points[i-1]
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

