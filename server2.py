#!/usr/bin/env python

# Run with sudo python ./server.py

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

from time import gmtime, strftime, sleep, localtime

from Adafruit_BME280 import *

# sudo apt-get install python-w1thermsensor
# https://github.com/timofurrer/w1thermsensor/blob/master/README.md
# Enable Kernel driver
#  sudo nano /boot/config.txt
#
#  Then at the end add the following
#  dtoverlay=w1-gpio
#  dtoverlay=w1-gpio,gpiopin=x <== use this to specify a different gpio pin
#  Save the file
#
# Finally, reboot
# sudo reboot

from w1thermsensor import W1ThermSensor

class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(s):
                s.send_response(200)
                s.send_header('Content-type','application/json')
                s.end_headers()

                message = getTempMessage()

                # Write content as utf-8 data
                s.wfile.write(bytes(message))

def getTempMessage():
        time_value = strftime("%a %b %-d    %-I:%M %p", localtime())

        try:
                sensor1 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "8000002708bd")
                temp1   = int(sensor1.get_temperature(W1ThermSensor.DEGREES_F))
                sleep(0)
                temp1   = int(sensor1.get_temperature(W1ThermSensor.DEGREES_F))

                sensor2 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "031645c790ff")
                temp2   = int(sensor2.get_temperature(W1ThermSensor.DEGREES_F))
                sleep(0)
                temp2   = int(sensor2.get_temperature(W1ThermSensor.DEGREES_F))
        except:
                temp1 = "999"
                temp2 = "999"

        sleep(0)
        sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

        temp3 = sensor.read_temperature()
        temp3 = (temp3 * 9)/5 +32
        temp3 = int(round(temp3))

        pressure = sensor.read_pressure() * .0002953
        sleep(0)
        pressure = sensor.read_pressure() * .0002953
        pressure = round(pressure, 3)

        message =  "{\n"
        message += "  \"data\": [\n"
        message += "    {\n"
        message += "      \"name\" : \"outsideTemp\",\n"
        message += "      \"time\" : \"" + str(time_value)   + "\",\n"
        message += "      \"temperature\" : \"" + str(temp1) + "\"\n"
        message += "    },\n"
        message += "    {\n"
        message += "      \"name\" : \"insideTemp\",\n"
        message += "      \"time\" : \"" + str(time_value) + "\",\n"
        message += "      \"temperature\" : \"" + str(temp2) + "\"\n"
        message += "    },\n"
        message += "    {\n"
        message += "      \"name\" : \"basementTemp\",\n"
        message += "      \"time\" : \"" + str(time_value) + "\",\n"
        message += "      \"temperature\" : \"" + str(temp3) + "\"\n"
        message += "    },\n"
        message += "    {\n"
        message += "      \"name\" : \"pressure\",\n"
        message += "      \"time\" : \"" + str(time_value) + "\",\n"
        message += "      \"pressure\" : \"" + str(pressure) + "\"\n"
        message += "    }\n"
        message += "  ]\n"
        message += "}\n"

        return message

def run():
        print('starting server...')

        # Server settings
        # Choose port 80, for port 80, which is normally used for a http server, you need root access
        server_address = ('', 80)
        httpd = HTTPServer(server_address, RequestHandler)

        print('running server...')
        httpd.serve_forever()


run()

