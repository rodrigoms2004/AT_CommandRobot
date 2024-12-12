import serial
import time
from datetime import datetime

# Define modem port and baud rate
modem_port = "/dev/ttyACM0"  # Update with your modem's port
baud_rate = 115200  # Default baud rate for most modems

def send_at_command(command):
    try:
        with serial.Serial(modem_port, baud_rate, timeout=1) as modem:
            modem.write((command + '\r\n').encode())
            time.sleep(0.5)  # Wait for a response
            response = modem.read_all().decode().strip()
            return response
    except Exception as e:
        return f"Error: {e}"

def log_response(command, response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("modem_logs.txt", "a") as logfile:
        logfile.write(f"{timestamp} - Command: {command}\nResponse: {response}\n\n")

def main():
    commands = ["AT", "AT+CSQ", "AT+CGMI"]  # Replace with your desired commands
    for command in commands:
        response = send_at_command(command)
        log_response(command, response)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(900)  # Wait 15 minutes (900 seconds)

