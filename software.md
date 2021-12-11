fix links from https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

----


In this page we'll assume you've already gotten your Raspberry Pi up and running and can log into the command line

Here's the quick-start for people with some experience:

* Download the latest Raspberry Pi OS or Raspberry Pi OS Lite to your computer
* Burn the OS image to your MicroSD card using your computer
* Re-plug the SD card into your computer (don't use your Pi yet!) and set up your wifi connection by editing supplicant.conf
* Activate SSH support
* Plug the SD card into the Pi
* If you have an HDMI monitor we recommend connecting it so you can see that the Pi is booting OK
* Plug in power to the Pi - you will see the green LED flicker a little. The Pi will reboot while it sets up so wait a good 10 minutes
* If you are running Windows on your computer, install Bonjour support so you can use .local names, you'll need to reboot Windows after installation
* You can then ssh into raspberrypi.local

I really really recommend the lastest Raspberry Pi OS only. If you have an older Raspberry Pi OS install, run "sudo apt-get update" and "sudo apt-get upgrade" to get the latest OS!

# Upgrade your python 
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip

and

sudo pip3 install --upgrade setuptools

sudo pip3 install adafruit-circuitpython-epd
sudo apt-get install ttf-dejavu
sudo apt-get install python3-pil




# forse questo non serve, riprovare setup dall'inizio...
# install BLINKA

cd ~
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py


# requirered for web server and QRCode generation

pip3 install Flask
pip3 install pyqrcode
pip3 install pypng
pip3 install requests

# test display

https://learn.adafruit.com/2-13-in-e-ink-bonnet/usage

# autorun clock on startup 
On your Pi, type 

```bash
crontab -e 
```

and add the following row:

```bash
@reboot /bin/sleep 30; /usr/bin/python3 /home/pi/projects/zero-clock/code/zeroclock.py
```

this means execute 30 seconds after the boot, the zeroclock app. The pause is needed to be sure that all services required by the app are properly started.