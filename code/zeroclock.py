import time

print("Hello World, I am a clock!")

while True:
    t =  time.localtime()
    print ("its", time.strftime("%H:%M:%S", t))
    time.sleep(2)

