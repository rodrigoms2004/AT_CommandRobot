import serial
import time
from datetime import datetime
from gpio_functions import restart
import os

modem_data = {
    "port1": "/dev/ttyACM0",
    "port2": "/dev/ttyUSB0",
    "baud_rate": 115200,
    "model": "ST_script3_ACM0_USB0"
}

# Function to send AT commands and get responses
def execute_at_commands(commands, command_delay, modem_info):
    try:
        modem_port = ""
        if os.path.exists('/dev/ttyACM0') == True:
            modem_port = modem_info['port1']
        else:
            modem_port = modem_info['port2']

        baud_rate = modem_info['baud_rate']
        # Connect to the modem
        with serial.Serial(modem_port, baud_rate, timeout=1) as modem:
            results = []
            for command in commands:
                # Send the command
                modem.write((command + '\r\n').encode())
                time.sleep(command_delay)  # Wait for the modem to process the command
                # Read the response
                response = modem.read_all().decode().strip()
#                 print(command, response)
                results.append((command, response))
            return results
    except Exception as e:
        restart(1)
        return [("Error", str(e))]

# Function to log the results
def log_results(results, modem_name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(modem_name + "_logs.txt", "a") as logfile:
        logfile.write(f"--- {timestamp} ---\n")
        for command, response in results:
            logfile.write(f"Command: {command}\nResponse: {response}\n")
        logfile.write("\n")


# Main execution function
def main():
    # Define the AT commands to send and reponse delays in seconds
    general_commands = (["AT", "AT+CSQ", "AT+CGMI", "AT+CIMI", "AT+QCCID",
                        "AT+CREG?", "AT+CGREG", "AT+QNWINFO", 'AT+QENG="servingcell"'], 3)
    neighbor_cell = (['AT+QENG="neighbourcell"'], 5)
    cops_command = (["AT+COPS=?"], 120)
    
    command_list = [general_commands, neighbor_cell, cops_command]
    
    results = None
    for command_tuple in command_list:
        results = execute_at_commands(command_tuple[0], command_tuple[1], modem_data)
        log_results(results, modem_data['model'])


if __name__ == "__main__":
    main()
