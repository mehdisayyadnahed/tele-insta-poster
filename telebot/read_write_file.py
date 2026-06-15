import json
import os
import shutil
from constants import *
from except_exit_func import *

async def save_config(cfg_file, cfg_data, mode):
    """
    Synchronously manages the reading, writing, appending, deleting, and modifying
    of JSON configuration files for Instagram profiles within the bot environment.

    Args:
        cfg_file (str): The target configuration filename.
        cfg_data (dict/list/str): Payload used to write, delete, or modify settings.
        mode (str): Operations mode: 'r' (Read), 'w' (Write), 'a' (Append/Add), 'd' (Delete), 'm' (Modify).

    Returns:
        bool/dict: Depending on the mode, returns the configuration dictionary or operation success status.
    """
    global downloads_folder
    global configs_folder
    global sessions_folder

    accounts_config = {}

    # Safely construct the full path to the configuration file
    cfg_file_path = os.path.join(configs_folder, cfg_file)

    # Ensure the configs directory exists on disk
    if not os.path.isdir(configs_folder):
        os.makedirs(configs_folder)

    # ==============================================================================
    # 1. READ MODE ("r")
    # ==============================================================================
    if mode == "r":
        # If the file does not exist, create an empty file and return False
        if not os.path.isfile(cfg_file_path):
            try:
                with open(cfg_file_path, "w", encoding="utf-8") as file:
                    pass
                return False
            except Exception as e:
                print(f"An Error Occurred While Creating 'config' File: {e}")
                except_exit_func()

        # Parse and return JSON config content if it contains data
        if os.path.isfile(cfg_file_path):
            if os.path.getsize(cfg_file_path) > 0:
                try:
                    with open(cfg_file_path, "r", encoding="utf-8") as file:
                        accounts_config = json.load(file)
                    if not accounts_config:
                        return False
                    else:
                        return accounts_config
                except Exception as e:
                    print(f"An Error Occurred While Reading 'config' File: {e}")
                    except_exit_func()
            else:
                return False

    # ==============================================================================
    # 2. WRITE MODE ("w")
    # ==============================================================================
    elif mode == "w":
        try:
            with open(cfg_file_path, "w", encoding="utf-8") as file:
                json.dump(cfg_data, file, indent=4)
            return True
        except Exception as e:
            print(f"An Error Occurred While Writing 'config' File: {e}")
            return False

    # ==============================================================================
    # 3. APPEND / ADD MODE ("a")
    # ==============================================================================
    elif mode == "a":
        if os.path.isfile(cfg_file_path):
            if os.path.getsize(cfg_file_path) > 0:
                try:
                    with open(cfg_file_path, "r", encoding="utf-8") as file:
                        accounts_config = json.load(file)
                except Exception as e:
                    print(f"An Error Occurred While Reading 'config' File: {e}")
                    except_exit_func()

                # Update the existing profile configuration
                accounts_config.update(cfg_data)

                try:
                    with open(cfg_file_path, "w", encoding="utf-8") as file:
                        json.dump(accounts_config, file, indent=4)
                except Exception as e:
                    print(f"An Error Occurred While Updating 'config' File: {e}")
                    except_exit_func()
            
            elif os.path.getsize(cfg_file_path) == 0:
                try:
                    with open(cfg_file_path, "w", encoding="utf-8") as file:
                        json.dump(cfg_data, file, indent=4)
                except Exception as e:
                    print(f"An Error Occurred While Initializing empty 'config' File: {e}")
                    except_exit_func()

        # Create standard download queue directories for the newly added profile
        cfg_dir_name = list(cfg_data.keys())[0]
        user_download_dir = os.path.join(downloads_folder, cfg_dir_name)
        if not os.path.isdir(user_download_dir):
            os.makedirs(user_download_dir)

        if not os.path.isfile(cfg_file_path):
            try:
                with open(cfg_file_path, "w", encoding="utf-8") as file:
                    json.dump(cfg_data, file, indent=4)
            except Exception as e:
                print(f"An Error Occurred While Initializing 'config' File: {e}")
                except_exit_func()

    # ==============================================================================
    # 4. DELETE MODE ("d")
    # ==============================================================================
    elif mode == "d":
        if os.path.isfile(cfg_file_path):
            if os.path.getsize(cfg_file_path) > 0:
                try:
                    with open(cfg_file_path, "r", encoding="utf-8") as file:
                        accounts_config = json.load(file)
                except Exception as e:
                    print(f"An Error Occurred While Reading 'config' File: {e}")
                    except_exit_func()

                if accounts_config:
                    # Remove the specific account from the configuration mapping
                    if cfg_data in accounts_config:
                        del accounts_config[cfg_data]

                    # Save updated configurations back to the file
                    with open(cfg_file_path, "w", encoding="utf-8") as file:
                        json.dump(accounts_config, file, indent=4)

                    # Delete the corresponding credential session configuration file
                    session_file = os.path.join(sessions_folder, f"{cfg_data}.json")
                    if os.path.exists(session_file):
                        os.remove(session_file)

                        # Delete the local physical downloaded media queue directory on disk
                        user_download_dir = os.path.join(downloads_folder, cfg_data)
                        if os.path.isdir(user_download_dir):
                            shutil.rmtree(user_download_dir)
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    # ==============================================================================
    # 5. MODIFY MODE ("m")
    # ==============================================================================
    elif mode == "m":
        if os.path.isfile(cfg_file_path):
            if os.path.getsize(cfg_file_path) > 0:
                try:
                    with open(cfg_file_path, "r", encoding="utf-8") as file:
                        accounts_config = json.load(file)
                except Exception as e:
                    print(f"An Error Occurred While Reading 'config' File: {e}")
                    except_exit_func()

                # Modify daily posting frequency limit and default caption suffix settings
                accounts_config[cfg_data[0]]["post_in_day"] = cfg_data[1]
                accounts_config[cfg_data[0]]["add_to_caption"] = cfg_data[2]

                try:
                    with open(cfg_file_path, "w", encoding="utf-8") as file:
                        json.dump(accounts_config, file, indent=4)
                    return True
                except Exception as e:
                    print(f"An Error Occurred While Modifying 'config' File: {e}")
                    except_exit_func()
            else:
                return False
        else:
            return False
