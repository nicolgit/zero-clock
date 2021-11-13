Because it isn't possible to run Visual Studio Code or use remote-ssh extension on Raspberry Pi Zero W (https://forums.raspberrypi.com/viewtopic.php?t=296434), using the following instructions, you can work from a Windows 11 machine on a remote folder mounted locally. In this way you will work on Windows 11 machine and VS code as the project is local, but via ssh you can run on pizero (debugging not possible).

## Environment
* Windows 10 or Windows 11 with WSL2 installed and running
* Windows Terminal

## Instructions
Open WSL either by launching the Windows Terminal and creating a new WSL tab or by launching the Linux distro that you installed and type:


```bash
sudo mkdir /mnt/pizero
sudo sshfs -o allow_other,default_permissions pi@pizero:/home/pi/projects/ /mnt/pizero
```

where:
1. /mnt/pizero is the location where mount the remote pizero working folder
2. pi@pizero username and ip/hostname of your piZero machine
3.  /home/pi/projects/ is the folder you will mount in (1)

once mounted from your terminal, launch into Visual Studio Code using

```bash
code .
```

From Visual studio code you can git clone a repo in /mount/pizero folder and work locally on your piZero. Obviously in order to run your code on piZero you can't use VSCode debugger, but you need to use an ssh terminal.


## More information
* https://forums.raspberrypi.com/viewtopic.php?t=296434
* https://www.windowscentral.com/how-install-wsl2-windows-10 
* https://code.visualstudio.com/blogs/2019/09/03/wsl2

