# postprocessing of data received from image recognition

from PyQt5.QtCore import QThread, pyqtSignal
from scipy.signal import savgol_filter


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


class SpikesByChange(QThread):
    processingFinished = pyqtSignal()

    def __init__(self, treeelement, pmax, nmax):
        super().__init__()

        self.treeelement = treeelement
        self.pmax = pmax
        self.nmax = nmax

    def run(self):
        xdata, ydata = self.treeelement.getPreviousData()

        data_deriv = derive(xdata, ydata)
        spikes = find_spikes(data_deriv, self.pmax, self.nmax)
        new_ydata = bridge_error_segments(ydata, spikes)

        self.treeelement.xdata = xdata
        self.treeelement.ydata = new_ydata
        self.processingFinished.emit()
