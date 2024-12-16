# Noise-Monitoring-IoT
This repository contains the project where I built an end-to-end IoT system to monitor noise levels.

Run Locally:
1. Ensure all physical components are present and functional:
   - Raspberry Pi with GrovePi sound sensor
   - Laptop/Desktop
   - Yeelight Smart LED Bulb
2. Setup components:
   - Download sense.py and requirements.txt on Raspberry Pi
   - Run 'pip install -r requirements.txt' on Raspberry Pi
   - Download process.py and requirements.txt on laptop/desktop
   - Run 'pip install -r requirements.txt' on laptop/desktop
   - Connect Yeelight Smart LED Bulb to laptop/desktop ([instructions here](https://user-cube.medium.com/control-xiaomi-yeelight-bulbs-with-python-f90fba962257))
3. Run 'python process.py' on laptop/desktop (before sense.py so MQTT broker isn't overloaded with information)
4. Run 'python sense.py' on Raspberry Pi
5. Test system:
   - Play audio/music near your GrovePi sound sensor and watch the LED adjust its brightness levels with different noise levels!
   - If audio exceeds a threshold defined in process.py, it will flash to alert the user of excessive noise
   - Threshold is determined based on current date and time using the World Time API (no API key required) to limit noise on weekdays and nights
