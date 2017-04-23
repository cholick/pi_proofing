

### pi setup
* https://raspberrypi.stackexchange.com/questions/26623/ds18b20-not-listed-in-sys-bus-w1-devices

```bash
sudo apt-get install rsync python-pip python-dev
sudo pip install virtualenv
```

### App Setup
```bash
virtualenv env
. env/bin/activate
pip install -r requirements.txt
```

### Development
```bash
python -m unittest discover -v -s proofing -p '*_test.py'
```

```bash
rsync -avzh --delete --exclude=env --exclude=.git --exclude=.idea . pi@192.168.2.19:~/app
```

### Todo
* Figure out how to test `heater_switch.py` (can't compile RPi.GPIO on dev machine)

### Reference
* [GPIO key](https://www.raspberrypi.org/documentation/usage/gpio-plus-and-raspi2/)
* https://github.com/kipe/python-onewire
* https://www.weekendbakery.com/posts/a-few-tips-on-dough-temperature/
