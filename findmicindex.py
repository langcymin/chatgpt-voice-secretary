import pyaudio
# po = pyaudio.PyAudio()

# for index in range(po.get_device_count()): 
#     desc = po.get_device_info_by_index(index)
#     #if desc["name"] == "record":
#     print ("DEVICE: %s  INDEX:  %s  RATE:  %s " %  (desc["name"], index,  int(desc["defaultSampleRate"])))

po = pyaudio.PyAudio()

for index in range(po.get_device_count()): 
    desc = po.get_device_info_by_index(index)
    if desc["maxInputChannels"] > 0:
        if po.get_default_input_device_info()["name"] == desc["name"]:
            mic_index = index
            mic_rate = int(desc["defaultSampleRate"])
            print(mic_index)
            print(type(mic_index))
            print(type(mic_rate))
            break
