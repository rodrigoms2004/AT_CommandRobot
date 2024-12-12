import serial
import time
from datetime import datetime
from gpio_functions import restart


# Define modem port and baud rate
modem_port = "/dev/ttyACM2"  # Update with your modem's port
baud_rate = 115200  # Adjust as per your modem's specifications

# Function to send AT commands and get responses
def execute_at_commands(commands):
    try:
        # Connect to the modem
        with serial.Serial(modem_port, baud_rate, timeout=1) as modem:
            results = []
            for command in commands:
                # Send the command
                modem.write((command + '\r\n').encode())
                time.sleep(3)  # Wait for the modem to process the command
                # Read the response
                response = modem.read_all().decode().strip()
                results.append((command, response))
            return results
    except Exception as e:
        #restart(1)
        return [("Error", str(e))]


# Function to log the results
def log_results(results):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("modem_logs.txt", "a") as logfile:
        logfile.write(f"--- {timestamp} ---\n")
        for command, response in results:
            logfile.write(f"Command: {command}\nResponse: {response}\n")
        logfile.write("\n")

# Main execution function
def main():
    # Define the AT commands to send
    commands = ["AT", "AT+CSQ", "AT+CGMI", "AT+CIMI", "AT+QCCID"] 
    results = execute_at_commands(commands)
    log_results(results)

if __name__ == "__main__":
    main()

