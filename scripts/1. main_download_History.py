"""
This file is meant to update the storage folder by downloading all available data
from MT5 and combine it with the previously downloaded.
For this purpose it uses TCP sockets to connect to the corresponding MT5 client.

This file creates a socket Server.
When the correspoding MQL5 file is connected to it then:
    - Python asks MT5 for the list of symbols.
    - Python asks MT5 for the list of open positions.
    - Python asks MT5 for the OCHLV data of every symbol in several periods.
        - MT5 saves them in csv files
        - Python then reads them and combines them with the previously downloaded.
"""

# Classical Libraries
import datetime as dt
import matplotlib.pyplot as plt

import sys
sys.path.append("..") # Adds higher directory to python modules path.
from traphing.data_classes import Portfolio, Symbol, Velas
import traphing.utils.sockets as sockets_lib
from traphing.utils import Timeframes
import traphing.utils as utils

plt.close("all") # Close all previous Windows

# Now we can proceed to creating a class responsible for socket manipulation:

"""
####################### OPTIONS ###########################
"""

dataSource =  "MQL5"  # Hanseatic  FxPro GCI Yahoo
[storage_folder, updates_folder] = utils.get_foldersData(source = dataSource, rrf = "../../../" )
#### Load the info about the available symbols #####
Symbol_info = Symbol.load_symbols_info_from_csv(storage_folder)

## 
mode = "Blocking"
port = 9093
serv = sockets_lib.socketserver('127.0.0.1',port)
print("TCP Server listening on port ", port, ", mode = ", mode)
serv.listen();

# Ask for the list of symbols! 
try:
    success = serv.request_csv_symbol_info();
    
    if (success):
        symbol_info = Symbol.load_symbols_info_from_csv(updates_folder)
        Symbol.save_symbols_info_to_csv(storage_folder, Symbol_info)
        print(symbol_info)
        
        ## Now we download data from the first 10 symbols and mix it with previous one.
        timeframes_list = [Timeframes.M15,Timeframes.M1,Timeframes.M5, Timeframes.D1] # [1, 5, 15, 1440]
        symbol_names_list = Symbol_info["Symbol"].tolist()
        N_symbols = len(symbol_names_list)
        
        ## Download the last week ofsome symbols
        start_date = dt.date.today() - dt.timedelta(days=7000)
        start_date = start_date.strftime("%d %m %Y")
        
        for i in range(N_symbols):
            print ("------ Downloading symbol %i/%i ----------"%(i+1,N_symbols) )
            for p in range(len(timeframes_list)):
                symbol_name = symbol_names_list[i]
                timeframe = timeframes_list[p]
                success = serv.request_csv_data_signal(symbol_name, timeframe,start_date);
                
                if (success):
                    ## Load the local and new data and save it !!
                    timeData = Velas(symbol_name,timeframe)
                    timeData.update_csv (storage_folder, updates_folder)
                    print ("Updated database")
                      
    serv.sock.close()
except:
    print ("Forced closing due to interruption")
    serv.sock.close()
#if(0):
#    # Listening to the data
#    while True:  
#        print ("Listening")
#        msg = serv.recvmsg()
