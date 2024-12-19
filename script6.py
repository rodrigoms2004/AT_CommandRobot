import serial
import time
from datetime import datetime
from gpio_functions import restart
import os
import pandas as pd
import numpy as np
import re
from random import randrange

modem_data = {
    "port1": "/dev/ttyACM6",
    "port2": "/dev/ttyUSB6",
    "baud_rate": 115200,
    "filename": "ST_script6_ACM6_USB6.csv"
}

# Function to send AT commands and get responses
def execute_at_commands(commands, command_delay, modem_info):
    try:
        modem_port = ""
        if os.path.exists(modem_info['port1']) == True:
            modem_port = modem_info['port1']
        else:
            modem_port = modem_info['port2']

        baud_rate = modem_info['baud_rate']
        # Connect to the modem
        with serial.Serial(modem_port, baud_rate, timeout=1) as modem:
            results = []
            iccid = ""
            for command in commands:
                # Send the command
                modem.write((command + '\r\n').encode())
                time.sleep(command_delay)  # Wait for the modem to process the command
                # Read the response
                response = modem.read_all().decode().strip()
#                 print(command, response)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if command == "AT+QCCID":
                    match = re.search(r"\+QCCID: (\d+)", response)
                    iccid = match.group(1)

                results.append({
                    "iccid": iccid,
                    "command": command,
                    "response": response,
                    "timestamp": timestamp
                })
            return results
    except Exception as e:
        #restart(1)
        print(str(e))
        return [("Error", str(e))]

def log_results_csv(data, file_name):
    isFileExists = os.path.isfile(file_name)
    mode = 'a' if isFileExists else 'w'
    print("mode", mode)

    data.to_csv(file_name, mode=mode, index=False, sep=';', header= not isFileExists)


# Main execution function
def main():
    print(np.__version__)
    print(pd.__version__)

    # Define the AT commands to send and reponse delays in seconds
    general_commands = (["AT+QCCID", "AT", "AT+CSQ", "AT+CGMI", "AT+CIMI",
                        "AT+CREG?", "AT+CGREG", "AT+QNWINFO", 'AT+QENG="servingcell"'], 3)
    neighbor_cell = (["AT+QCCID", 'AT+QENG="neighbourcell"'], 5)
    cops_command = (["AT+QCCID", "AT+COPS=?"], 120)
    
    command_list = [general_commands, neighbor_cell, cops_command]
    

    df_results = None
    for command_tuple in command_list:
        time.sleep(randrange(1,4))  # wait a random time between 1 and 3 seconds
        results = execute_at_commands(command_tuple[0], command_tuple[1], modem_data)
        df_results = pd.DataFrame(results)
        print(df_results)
        log_results_csv(df_results, modem_data['filename'])
    
    


if __name__ == "__main__":
    main()
