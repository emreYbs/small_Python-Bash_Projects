#!/usr/bin/env python3
#https://github.com/emreYbs
# -*- coding: utf-8 -*-

import os
import re
import shutil
from time import sleep
import threading

def display_banner():
    """
    Displays the banner for File_Organiser.py
    """
    banner = r"""
    ____ _ _    ____    ____ ____ ____ ____ _  _ _ ___  ____ ____ 
    |___ | |    |___    |  | |__/ | __ |__| |\ | |   /  |___ |__/ 
    |    | |___ |___    |__| |  \ |__] |  | | \| |  /__ |___ |  \ 
                                                                  
                                                        by emreYbs
    """

    banner = "\033[31m" + banner + "\033[0m"  # Add ANSI escape sequence for red color
    print(banner)

def clean_folder(file_types, directory):
    """
    Moves files with the given file types to separate folders based on their file types.
    """
    os.makedirs(directory, exist_ok=True)

    # Create regex for files with the given file types
    filename_regex = re.compile(r'(.+)\.(.+)')

    # Loop through files in the given directory
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            print("Organizing " + filename + "...")
            sleep(0.1)
            print("..........")
            mo = filename_regex.search(filename)

            try:
                if mo and mo.group(2) in file_types:
                    file_type = mo.group(2)
                    new_directory = os.path.join(directory, file_type.upper() + "s")
                    os.makedirs(new_directory, exist_ok=True)
                    shutil.move(os.path.join(dirpath, filename), os.path.join(new_directory, filename))
                    print("Done!")
            except AttributeError:
                print(f"Error: File {filename} does not match the expected format.")
            except shutil.Error:
                print(f"Error: Could not move file {filename}. It may already exist in the destination directory.")
            except PermissionError:
                print(f"Permission denied: You don't have the necessary permissions to move file {filename}.")
            except FileNotFoundError:
                print(f"Error: File {filename} not found.")
            except Exception as e:
                print(f"An unexpected error occurred: {str(e)}")

def get_file_types():
    size = int(input("Enter how many file types you want to be organized:\n"))
    sleep(0.2)
    if size == 0:
        print("You haven't chosen any file types to be organized. Exiting...")
        sleep(0.2)
        exit()
    elif size < 0:
        print("You have entered an invalid number. Exiting...")
        sleep(0.2)
        exit()
    elif size == 1:
        print(f"You have chosen {size} file type to be organized.\n")
        sleep(0.2)
    elif size > 1:
        print(f"You have chosen {size} file types to be organized.\n")
        sleep(0.5)
    print("..........")
    sleep(0.5)
    file_types = []
    print("\nEnter the file types like below: \n") 
    sleep(0.2)
    print("\tExample: \n")
    print("\t\tpdf\n")
    print("\t\ttxt\n")
    print("\t\tdocx\n")
    sleep(0.2)
    print("..........")
    sleep(0.3)
    for _ in range(size):
        file_type = input()
        file_types.append(file_type)
    print("Done. Thanks!")
    sleep(0.2)
    print("Organizing files...")
    print("This may take some time...")
    return file_types

def check_stop_execution():
    """
    Checks for user input to stop execution.
    """
    def stop_execution():
        """
        Stops the execution of the program.
        """
        print("Execution stopped by user.")
        exit()

    try:
        while True:
            user_input = input()
            if user_input.lower() == "q":
                stop_execution()
    except KeyboardInterrupt:
        stop_execution()

def main():
    print("\n\t\t\t _____File Organiser_____\n")
    display_banner()

    directory = input("\033[35mEnter the full directory path you would like to be organized: \n\033[0m")
    print(f"You have chosen {directory} as the directory to be organized.\n")
    print("\033[31mIt can take a while depending on the size of the folder. So please wait...\033[0m")
    print("..........")
    sleep(0.5)
    print("Organizing files may take some time...")
    sleep(0.2)

    file_types = get_file_types()
    clean_folder(file_types, directory)

    # Create a thread for checking stop execution
    stop_execution_thread = threading.Thread(target=check_stop_execution)
    stop_execution_thread.start()

    check_stop_execution()

    print("All files have been organized.\n")

if __name__ == "__main__":
    main()
