"""
Renames all files in a given folder (MY_PATH)
to the form "filename_XhXmXs"
so it includes the duration of the media file
(h = hours, m = minutes, s = seconds)
"""

import subprocess
from os import listdir
from os.path import isfile, join
import os
import datetime


def getLength(filename):
  result = subprocess.Popen(["ffprobe", filename],
    stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
  return [x for x in result.stdout.readlines() if "Duration" in x]

import subprocess32 as sp
import json


def probe(vid_file_path):
    ''' Give a json from ffprobe command line

    @vid_file_path : The absolute (full) path of the video file, string.
    '''
    if type(vid_file_path) != str:
        raise Exception('Give ffprobe a full file path of the video')
        return

    command = ["ffprobe",
            "-loglevel",  "quiet",
            "-print_format", "json",
             "-show_format",
             "-show_streams",
             vid_file_path
             ]

    pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
    out, err = pipe.communicate()
    return json.loads(out)


def duration(vid_file_path):
    ''' Video's duration in seconds, return a float number
    '''
    _json = probe(vid_file_path)

    if 'format' in _json:
        if 'duration' in _json['format']:
            return float(_json['format']['duration'])

    if 'streams' in _json:
        # commonly stream 0 is the video
        for s in _json['streams']:
            if 'duration' in s:
                return float(s['duration'])

    # if everything didn't happen,
    # we got here because no single 'return' in the above happen.
    raise Exception('I found no duration')
    #return None

def formatDuration(hour_mins_sec):
	hours = hour_mins_sec[0]
	mins = hour_mins_sec[1]
	secs = hour_mins_sec[2]

	if mins[0] == '0':
		mins = mins[1:]
	if secs[0] == '0':
		secs = secs[1:]

	if int(hours[len(hours)-1]) > 0:
		return hours + "h" + mins + "m" + secs + "s"

	elif int(mins[len(mins)-1]) > 0:
		return mins + "m" + secs + "s"

	else:
		return secs + "s"

MY_PATH = "/Users/framunno/Downloads/rename"
onlyfiles = [f for f in listdir(MY_PATH) if isfile(join(MY_PATH, f))]

for file in onlyfiles:
	file_name = join(MY_PATH, file)
	try:
		file_duration = duration(file_name)
		reformat_duration = str(datetime.timedelta(seconds=round(file_duration)))
		hour_mins_sec = reformat_duration.split(":")
		file_split = file_name.split(".")
		new_file_name = file_split[0] + "_" + formatDuration(hour_mins_sec) + "." + file_split[1]
		os.rename(file_name, new_file_name)
	except:
		print("Exception found on: ", file_name)




