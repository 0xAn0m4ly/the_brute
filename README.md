# the_brute

This is a Pyhton script that performs brute-force attacks on internet protocols, now are available FTP, SSH, SMB and MySQL but
in the future version there will be new ones. The script is meant to be interactive and the user is guided along the 
configurations and the results.
The program is based on 3 modes:
1.  Same user and a list of passwords
2.  A list of users and the same password
3.  A list of users and passwords

**DISCLAIMER: this script is only for isolated environment and not meant to be used against private systems, remember that
 attacking private hosts is illegal. Please use this tool just for research uses; I assume no liability in the event of
 misuse or improper use.**

---

### Requirements

* **Python 3.x** installed on your system.
* **"paramiko", "impacket," "mysql-connector-python", "colorama" libraries**: you can easily download them by cloning or
    downloading the **"requirements.txt"** file and by typing in the cmd line:
  ```bash
   pip install -r requirements.txt
  ```


---

### Installation & Execution

There is no complex setup. Just download the script and run it directly from your terminal or editor.

1. **Download the script** (or clone the repository):
   ```bash
   git clone https://github.com/0xAn0m4ly/the_brute
   cd YOUR-REPO-NAME
   ```

2. **Run the program**:
   ```bash
   py BruteForce.py
   ```

---

### ⚙️ How It Works
This tool performs brute-force attacks by connecting to the protocol's port and sending multiple login request. The entire
process is guided but please pay attention to follow the instructions while entering the parameters. If the tool is unable to 
connect to the target, remember to check if the data provided are correct and in the required format.
**The users and passwords list are just text file you can easily create with the notepad or your text editor; there must be just
a username or password on each line.**
