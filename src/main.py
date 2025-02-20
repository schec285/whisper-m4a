import os
import subprocess
import whisper
import pandas as pd
import time
from datetime import datetime

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02}"

# start process
print(f"processing start:{datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}")

#dir path
# audioPath = "./original_m4a"
audioPath = "./original_m4a"
outputDir = "./output"
chunksDir = "./chunks"

# model load
model = whisper.load_model("medium")

# make chunks dir
if not os.path.exists(chunksDir):
    os.makedirs(chunksDir)

audioFileList = os.listdir(audioPath) # Directory in file list
# loop dir in file
for filename in audioFileList:
    print(*audioFileList)
    if filename.endswith(".m4a") and os.path.isfile(os.path.join(audioPath, filename)):
        audioFilePath = os.path.join(audioPath, filename)

        csvResult = [] # CSV array
        chunkLength = 60 # chunk size
        
        try:
            fileBaseName = filename.replace('.m4a', '')
            outputPattern = os.path.join(chunksDir, f"tmp_{fileBaseName}_%05d.wav")
            # write tmp
            subprocess.call(['ffmpeg', '-i', audioFilePath, '-f', 'segment', '-segment_time', str(chunkLength), '-c:a', 'pcm_s16le', '-ar', '44100', outputPattern])

            # processing division file
            chunkFiles = sorted([f for f in os.listdir(chunksDir) if f.startswith(f"tmp_{fileBaseName}_") and f.endswith('.wav')])
        
            for i, chunkFile in enumerate(chunkFiles):
                chunkFilePath = os.path.join(chunksDir, chunkFile)
                result = model.transcribe(chunkFilePath, language="ja")

                # write to csv
                for segment in result['segments']:
                    startTime = segment['start'] + (i * chunkLength)
                    endTime = segment['end'] + (i * chunkLength)
                    text = segment['text']
                    csvResult.append({
                        'start': format_time(startTime),
                        'end': format_time(endTime),
                        'text': text
                    })

            # pandas DataFrame encord for csv
            exportFile = os.path.join(outputDir, f"{fileBaseName}.csv")
            df = pd.DataFrame(csvResult)
            df.to_csv(exportFile, index=False, encoding='utf-8')

            print(f"save:{datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"Error processing {audioFilePath}: {str(e)}")
print (f"processing end:{datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}")
