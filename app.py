import sys
import json
import time
import schedule
import pandas as pd
from os import environ, remove
from pathlib import Path
from ftplib import FTP_TLS

# First, connect to the vsftpd server 
def get_ftp() -> FTP_TLS:
    # Get the FTP details from the activation
    FTPHOST = environ["FTPHOST"]
    FTPUSER = environ["FTPUSER"]
    FTPPASS = environ["FTPPASS"]

    # print(f"test of FTPHOST: {FTPHOST}")

    # Return the authenticated FTP user
    ftp = FTP_TLS(FTPHOST, FTPUSER, FTPPASS)
    ftp.prot_p()
    return ftp 

# Next, read the csv

def read_csv(config: dict) -> pd.DataFrame:
    url = config["URL"]
    params = config["PARAMS"]
    return pd.read_csv(url, **params)


if __name__ =="__main__":
    # get_ftp()
    #  Load the source configuration(JSON file)
    # Read the binary in order to parse it into a dataframe 
    with open("config.json", "rb") as fp:
        config = json.load(fp)

    # print(config)
    """
    [{'OFAC_SDN': {'URL': 'https://www.treasury.gov/ofac/downloads/sdn.csv',
      'PARAMS': {'names': ['ent_num', 'sdn_Name', 'sdn_Type', 'program', 
      'title', 'call_sign', 'vess_type', 'tonnage', 'grt', 'vess_flag',
        'vess_owner', 'remarks'], 'na_values': '-0- ', 'skipfooter': 1,
          'engine': 'python'}}}, {'OFAC_ALT':
        {'URL': 'https://www.treasury.gov/ofac/downloads/alt.csv', 
        'PARAMS': {'names': ['ent_num', 'alt_num', 'alt_type', 'alt_name', 
        'alt_remarks'], 'na_values': '-0- ', 'skipfooter': 1, 'engine': 
        'python'}}}, 
        {'OFAC_ADD': {'URL': 'https://www.treasury.gov/ofac/downloads/add.csv',
          'PARAMS': {'names': ['ent_num', 'add_num', 'address', 'complete_address', 'country',
           'add_remarks'], 'na_values': '-0- ', 'skipfooter': 1, 'engine': 'python'}}}]
    """
    # Printing the first csv file as a DataFrame
    # print(read_csv(config[0]["OFAC_SDN"]).head())
    for source_config in config:
        # Looping all of the csv files and storing them as a DataFrame
        for source_name, source_params in source_config.items():
            file_name = source_name + ".CSV"
            df = read_csv(source_params)
            df.to_csv(file_name, index=False)
            # Confirm that the file has been saved
            print(f"Saved {file_name} as CSV.")


    