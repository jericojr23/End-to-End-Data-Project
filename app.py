import sys
import json
import time
import schedule
import pandas as pd
from os import environ, pipe, remove
from pathlib import Path
from ftplib import FTP_TLS

# Connect to the vsftpd server 
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

# Upload to the FTP Server 
def ftp_upload(ftp: FTP_TLS, file_source: str):
    file_path = Path(file_source)
    file_name = file_path.name

    # Upload file
    with open(file_path, "rb") as fp:
        ftp.storbinary(f"STOR ftp/new/{file_name}", fp)

# Read csv and convert them into a dataframe

def read_csv(config: dict) -> pd.DataFrame:
    url = config["URL"]
    params = config["PARAMS"]
    return pd.read_csv(url, **params)
    pass

# Delete the local files 
def delete_file(file_source: str | Path):
    remove(file_source)
    pass

def pipeline():
    # get_ftp()
    #  Load the source configuration(JSON file)
    # Read the binary in order to parse it into a dataframe 
    with open("config.json", "rb") as fp:
        config = json.load(fp)

    # Getting the ftp user
    ftp = get_ftp()

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
    # Each source is called as a config and it is looped through 
    for source_config in config:
        # Looping all of the source name and get the source params/configuration
        for source_name, source_params in source_config.items():
            # Use a pathlib object 
            file_name = Path(source_name + ".CSV")
            df = read_csv(source_params)
            df.to_csv(file_name, index=False)
            # Confirm that the file has been saved
            print(f"Downloaded {file_name} as CSV.")

            ftp_upload(ftp, file_name)
            print(f"Uploaded {file_name} to FTP Server.")

            # delete the local files after uploading to FTP server

            delete_file(file_name)
            print(f"Deleted {file_name} in local files.")


if __name__ =="__main__":
    # Run the pipeline immediately 
    # pipeline()

    param = sys.argv[1]

    if param == "manual":
        pipeline()
    
    elif param == "schedule":
        # Run the pipeline based on schedule
        schedule.every().day.at("14:59").do(pipeline)

        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        print("Invalid parameter for app.py.")

    pass 