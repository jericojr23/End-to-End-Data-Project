# End-to-End-Data-Project
<!-- Hi Everyone!  -->
<!-- This is a project that uses python, sql, and power bi to create an end to end data project. -->

## Instructions

Clone this repository

Create a virtual environment using this command:

`python -m venv .venv`

Install the packages using this command:

`pip install -r requirements.txt`

## Discussion
It uses File transfer Protocol (FTP) to download, upload, and transfer files from one location to another on the internet. 
- The FTP server would be made using WSL with vsftpd. 

### Install Ubuntu via WSL
- Use the command: 
    - wsl --install -d Ubuntu

### Update the Ubuntu packages
- apt update && apt upgrade

### Install VSFTPD
- apt install vsftpd 


### Edit the Configuration file of vsftpd
- cp /etc/vsftpd.conf /etc/vsftpd.conf_original

sudo chown nobody:nogroup /home/ftpuser/ftp

sudo chmod a-w /home/ftpuser/ftp

echo "ftpuser" | sudo tee -a /etc/vsftpd.chroot_list

### Checking whether the files are uploaded to the ftp server
wsl -u ftpuser 
ls /home/ftpuser/ -l 

### Expected Output:
-rw------- 1 ftpuser ftpuser 1257848 Nov 27 14:49 OFAC_ADD.CSV
-rw------- 1 ftpuser ftpuser  879350 Nov 27 14:49 OFAC_ALT.CSV
-rw------- 1 ftpuser ftpuser 4022823 Nov 27 14:49 OFAC_SDN.CSV
dr-xr-xr-x 2 nobody  nogroup    4096 Nov 27 12:33 ftp