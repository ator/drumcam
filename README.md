# drumcam
Tool(s) for recording multiple webcameras simultaneously for making drum videos.

Implemented features:
* One stop recording of all cameras at once [NOTE: not yet via Python UI]
* Direct recording of compressed video stream to disk [NOTE: not yet via Python UI]
* Creating new takes for each recording (named folder using date+time) [NOTE: not yet via Python UI]
* Marking last take as good or bad [NOTE:can mark any take]
* Automatic numbering of takes (easier to handle than date+time) [NOTE: both number and date+time implemented]
* Printing of repository content to console (mostly useful for debugging)

Wanted features:
* Naming of recording (ie song name)
* Marking take as final (good take that should be used for the final edit)
* Copying final take(s) to network storage (eg Dropbox or NAS)
* Removing non-final takes
* Adding notes to takes
* Playing takes (preferrably all cameras at once)
* Archiving old recordings (to NAS or similar, in order to save local space)
* Restarting failed recording unless manually stopped (save a good take by switching to another angle while the bad recording restarts)
