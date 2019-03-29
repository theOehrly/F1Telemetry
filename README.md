F1 Telemetry
-

This software is alpha grade Software!!! Don't confuse it or it may do unexpected stuff (probably just crash)!
Beware of the list of issues below.

This software can read speed data from F1 Telemetry animations in videos (2018 style).
Halo overlay is NOT supported.
The Software also has some Postprocessing capabilities to clean up data (OCR is not perfect) and smooth it to give a
more pleasant look for presentation.

Dependencies:
-
- PyQt5
- Opencv2 (cv2)
- pytesseract and Tesseract OCR
- scipy

The f1a and f1n file from the tessdata folder need to be copied into the appropriate foler 
of your tesseract installation. 


Basic Usage:
-
- Videorecognition Environment:

Open video file. Move the selection region by clicking and dragging. Change it's size by (Shift-)scrolling.
The selected area should contain all the THREE (!) digits of the displayed speed and no other elements. 
There should be a small gap around between the digits and the box.
Then selected a start point and end point for the recognition, as well as a zero point.
The zero point sets the zero time for the data. Everything before it is negative in time.
Fianlly click run, choose a output folder and set a unique id (UID). The UID is used as filename ('UID'.csv).
It is also used as a prefix for the column headers of the csv file.

- Postprocessing Environment:
Open a previously created CSV file. The data can be cleaned up by removing spikes (wrong OCR results),
remove frames periodically (bad frames in fixed intervals) and do some smoothing (nicer presentation).
To make sure nothing important changed, the original data can be overlayed (checkbox bottom right).
The history of applied tools is shown in the "Tree" tab. Values for previously applied tools can be
changed afterwards. The software will calculated all the following modifications again based on the new data.
When done, click save. You will be ask where you want to save the data.


Current Issues:
- 
- (CRITICAL): using the remove data periodically tool after smoothing may crash the application
- (CRITICAL): reopening a file that has be saved after postprocessing crashes the application
- added tools can not yet be removed (planned)
- also undo is not implemented (not planned)
- Videoplayer is slow(ish); dragging through the timeline may be a few (dozen) frames off
- Tree items are not correctly themed/have wrong size
- Saving from postprocessing environment only saves the currently active tree

and probably more  