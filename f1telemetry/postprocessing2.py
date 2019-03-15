# postprocessing of data received from image recognition

from scipy.signal import savgol_filter


# #######################################
# Sub-functions
# The following functions are not called directly.
# They provide sub functionality to the main processing functions.

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


def sign(a):
    # return the sign of a number
    if a > 0:
        return 1
    elif a < 0:
        return -1
    else:
        return 0


def derive(xdata, ydata):
    # calculates the rate of change from a list of points
    # returns a list of the same length containing the derived values
    #
    # Example: If the data looks like (1), the following algorith assumes (2) [ combination shown in (3) ]
    #       |                /                 /|
    #       |               /                 / |
    # (1)   |        (2)   /          (3)    /  |
    #    ___|             /                 /___|
    #
    # This results in a smoother result and is necessary, as the data does not change with every frame of the video
    # As a consequence the derived values are always non-zero. It can not be determined whether the rate of change is
    # actually zero or the data is just inaccurate. As the regions with low rate of change are not interesting, this is
    # not an issue though.

    derivative = list()
    last_x = xdata[0]
    last_y = ydata[0]
    last_index = 0

    for i in range(1, len(xdata)):  # xdata and ydata have same length
        if ydata[i] != last_y:
            try:
                d = (ydata[i] - last_y) / (xdata[i] - last_x)
            except ZeroDivisionError:  # should only happen if there is something wrong with the data
                d = float('inf')

            for _ in range(last_index, i):  # write derivate for all preceding datapoints without change
                derivative.append(d)

            last_x = xdata[i]
            last_y = ydata[i]
            last_index = i

    # if there is no change at the end of the dataset, the last few points are missing from the derivative
    # no changes means derivate is zero --> fill up list with zeros
    for i in range(last_index, len(xdata)):
        derivative.append(0)

    return derivative


def find_spikes(data, pos_max=15, neg_max=-40):
    # check for changes in the derived data which are bigger than pos_max/neg_max
    # the segment which is considered a spike is the added to error_segs as [start, end] of spike
    error_segs = list()
    for i in range(len(data)):
        if data[i] > pos_max or data[i] < neg_max:
            i_start = i
            data_tmp = 0
            while data_tmp == 0:
                i += 1
                if i == len(data):
                    break  # we've reached the end
                data_tmp = data[i]
            i_end = i
            error_segs.append([i_start, i_end])

    return error_segs


def bridge_error_segments(data, error_segs):
    # bridges over the specified error segments in data linearly
    # this is good enough as error segments are short and data will be smoothed later on anyways
    # a copy of the provided list is returned, original data is not modified
    ndata = data.copy()
    for seg in error_segs:
        start_value = ndata[seg[0] - 1]
        try:
            end_value = ndata[seg[1] + 1]
        except IndexError:
            break
        seg_length = seg[1] - seg[0]
        delta = end_value - start_value
        gradient = delta / seg_length

        pos_in_seg = 0
        for i in range(seg[0], seg[1] + 1):
            ndata[i] = start_value + gradient * pos_in_seg
            pos_in_seg += 1

    return ndata


def get_points_of_change(data, min_neg_change=-1):
    # searches for points where the sign of data changes
    # min_neg_change can be set so that a simple switch from postive to negative is not enough
    #   but the value needs to be at least as small as min_neg_change (useful for filtering lift and coast)
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


def smooth_full(data):
    ydata_smooth = savgol_filter(data, 15, 2)
    return ydata_smooth


def smooth_segmented(xdata, ydata, min_neg_change):
    # calculate rate of change from data
    data_deriv = derive(xdata, ydata)
    # search for points of change
    # min_neg_change can be set, so that only negative changes greater than it are considered important
    speed_seg_points = get_points_of_change(data_deriv, min_neg_change=min_neg_change)
    # add the first and last point of data for sake of simplicity when iterating over points later on
    speed_seg_points.insert(0, 0)
    speed_seg_points.append(len(xdata))

    # smooth the values using a Savitzky-Golay filter
    # only smooth from one segmentation point to the next and not the whole data
    # this way all the max and min values are kept as they are
    ydata_smooth = list()
    # settings for filter
    window_length = 15
    polyorder = 2

    for n in range(1, len(speed_seg_points)):
        current_point = speed_seg_points[n]
        previous_point = speed_seg_points[n-1]
        if current_point - previous_point >= window_length:
            ydata_smooth.extend(savgol_filter(ydata[previous_point:current_point], window_length, polyorder))
        elif current_point - previous_point == 0:
            continue
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
                po = wl - 1
            else:
                po = polyorder
            # smooth current semgent with determined setting
            ydata_smooth.extend(savgol_filter(ydata[previous_point:current_point], wl, po))

    return ydata_smooth


def index_round_to_next(xdata, value):
    # rounds value to nearest larger value in xdata and returns the index
    # assumes the values in xdata to only be increasing; xdata intervals do not need to be constant though
    if value in xdata:
        return value  # value is in dataset

    avg_interval = (xdata[-1] - xdata[0]) / len(xdata)
    index = int(round(value / avg_interval, 0))  # start index is just a guess implying constant intervals

    try:
        while xdata[index] > value:
            index -= 1
        while xdata[index] < value:
            index += 1
        return index
    except IndexError:
        return None


def round_to_next(xdata, value):
    # returns value rounded to the nearest larger value in xdata
    i = index_round_to_next(xdata, value)
    if i:
        return xdata[i]
    return None


def round_to_previous(xdata, value):
    # returns value rounded to the nearest smaller value in xdata
    i = index_round_to_next(xdata, value)
    if i:
        return xdata[i - 1]
    return None


def round_to_closest(xdata, value):
    # returns value rounded to the closest value in xdata
    nextvalue = round_to_next(xdata, value)  # get next and previous value
    prevvalue = round_to_previous(xdata, value)

    if not nextvalue or not prevvalue:
        return None

    delta_next = abs(nextvalue - value)  # calculate absolute difference
    delta_prev = abs(prevvalue - value)

    if delta_next < delta_prev:  # return the value with the smaller absolute difference
        return nextvalue
    return prevvalue

# ########################################
# Main processing functions
# These functions are connected to treelements as their respective data processing functions
# !!! These functions may not change the data they are given but must create a copy !!!
# If data is not changed, creating a copy is not required


def spikes_by_change(xdata, ydata, pmax, nmax):
        data_deriv = derive(xdata, ydata)
        spikes = find_spikes(data_deriv, pmax, nmax)
        new_ydata = bridge_error_segments(ydata, spikes)

        return xdata, new_ydata


def spikes_manual(xdata, ydata, cutpaths):
    new_xdata = xdata.copy()
    new_ydata = ydata.copy()

    for cutpath in cutpaths:
        if cutpath[-1] < cutpath[0]:  # reverse cut if last x value smaller than first
            cutpaths[0] = reversed(cutpath[0])
            cutpaths[1] = reversed(cutpath[1])

        # cutpath has format (xvalues, yvalues)
        # first, get the x values in the dataset best corresponding to the values from the path
        corresponding_xvals = list()

        for x in cutpath[0]:
            v = round_to_closest(new_xdata, x)
            if not v:
                return xdata, ydata  # cut path is faulty, return unmodified data
            corresponding_xvals.append(v)

        # remove all duplicates
        filtered_xvals = list()
        filtered_yvals = list()
        for i in range(len(corresponding_xvals)):
            if corresponding_xvals[i] not in filtered_xvals:
                filtered_xvals.append(corresponding_xvals[i])
                filtered_yvals.append(cutpath[1][i])

        # create list of indexes corresponding to position in dataset xdata/ydata
        indexes = list()
        for xval in filtered_xvals:
            indexes.append(new_xdata.index(xval))

        # divide indexes into two groups, one where data is above cut and one where data is below
        # this is done by iterating from first index to last index thereby creating a continious list of indexes
        # the previously created index list may have gaps because of fast mouse movement, meaning spikes can be missed
        # the y value of the previous "real" index is used to determine above or below
        indexes_above = list()  # data is above cut path
        indexes_below = list()
        for i in range(indexes[0], indexes[-1]+1):
            if i in indexes:
                current_y = filtered_yvals[indexes.index(i)]  # "real" index, update the y value of the cut path
            if current_y < new_ydata[i]:
                indexes_above.append(i)
            else:
                indexes_below.append(i)

        # check whether more datapoints are above or below the cut
        # delete the side where there are less
        if len(indexes_above) < len(indexes_below):
            for index in indexes_above.__reversed__():  # pop from back so other indexes don't change
                new_xdata.pop(index)
                new_ydata.pop(index)
        else:
            for index in indexes_below.__reversed__():  # pop from back so other indexes don't change
                new_xdata.pop(index)
                new_ydata.pop(index)

    return new_xdata, new_ydata


def smoothing(xdata, ydata, segmented, min_neg_change):
        if segmented:
            new_ydata = smooth_segmented(xdata, ydata, min_neg_change)
        else:
            new_ydata = smooth_full(ydata)

        return xdata, new_ydata


def remove_datapoints_periodic(xdata, ydata, interval, index):
    new_xdata = xdata.copy()
    new_ydata = ydata.copy()
    while index < len(new_xdata):
        new_xdata.pop(index)
        new_ydata.pop(index)

        index += (interval - 1)
        # minus 1 is required as the list gets shorter by one when removing
    print(len(new_xdata))
    return new_xdata, new_ydata
