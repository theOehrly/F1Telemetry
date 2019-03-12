#F1 Telemetry

This software is alpha grade Software!!! Don't confuse it or it may do unexpected stuff (probably just crash)!

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

Use the f1a language file from the trainingdata folder for tesseract.
It needs to be copied into the appropriate foler of your tesseract installation. 


Current Issues:
- 
- Videoplayer is slow(ish); dragging through the timeline may be a few frames off
- It is difficult to move the OCR Region selection precisely
- Not all postprocessing tools that have buttons are implemented
- Tree items are not correctly themed/have wrong size
- Saving from postprocessing environment only saves the currently active tree

and probably more  