# AT Command Getter

Get AT commands from Suntech USB Modems



## Installation and service

Necessary python 3

### Python 

In case of problems, run it

```
sudo apt update

sudo apt install python3 python3-pip
sudo apt install libopenblas-dev

sudo apt upgrade


pip3 uninstall numpy
pip3 install numpy --no-cache-dir
pip3 install pandas

pip3 install --upgrade numpy pandas
```


### Crontab


```
/var/spool/cron/crontabs/pi

crontab -e

# m h  dom mon dow   command

# Suntech ACM0 or USB0
*/10 * * * * python /home/pi/at_command/script3.py

# Suntech ACM2 or USB2
*/10 * * * * python /home/pi/at_command/script4.py

# Suntech ACM4 or USB4
*/10 * * * * python /home/pi/at_command/script5.py

# Suntech ACM6 or USB6
*/10 * * * * python /home/pi/at_command/script6.py
```

### dmesg

check voltage

```
dmesg -wH
```
