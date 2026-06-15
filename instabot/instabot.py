import os
import time
import random
import pyotp
import pytz
from datetime import datetime
import schedule

from post_uploader import post_uploader
from read_write_file import save_config

# Configure standard local timezone and global state checkers
iran_tz = pytz.timezone('Asia/Tehran')
one_time_checker = True
upload_status = False
user_counter = {}

# ==============================================================================
# 1. Main Scheduler Task Execution Function
# ==============================================================================

def instabot():
    """
    Core scheduler task for handling Instagram automated uploads.
    Reads current times, matches against execution patterns, performs uploads
    when schedules coincide, and resets daily logs/patterns at Tehran midnight.
    """
    global one_time_checker

    # Locally import constants to keep scope isolated and prevent dynamic load issues
    from constants import (
        insta_cfg_file, 
        insta_pattern_cfg_file, 
        report_posted_file, 
        table_length, 
        start_posting_time, 
        loop_interrupt, 
        configs_folder, 
        posting_timing_table_file, 
        posting_timing_pattern_table_file
    )

    current_time = datetime.now(iran_tz)
    print(f"instabot check: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Load baseline configurations and user grid tables from JSON files
    all_users_data = save_config(insta_cfg_file, "", "r")
    all_users_data_pattern = save_config(insta_pattern_cfg_file, "", "r")
    timing_table = save_config(posting_timing_table_file, '', "r")
    pattern_timing_table = save_config(posting_timing_pattern_table_file, '', "r")

    # ------------------------------------------------------------------------------
    # Scenario A: Clean Config State - Proceed with Standard Schedule Checks
    # ------------------------------------------------------------------------------
    if (timing_table is not False and 
        pattern_timing_table is not False and 
        all_users_data is not False and 
        all_users_data_pattern is not False and 
        all_users_data == all_users_data_pattern):
            
        # Midnight configuration reset routine triggered once at hour 00:00 local time
        if current_time.hour == 0:
            if one_time_checker:
                # Reload master reference table to restore current active tracking patterns
                timing_table = save_config(posting_timing_table_file, '', "r")
                save_config(posting_timing_pattern_table_file, timing_table, "w")
                
                # Delete daily report cache to begin tracking stats for the new day
                report_file_path = os.path.join(configs_folder, report_posted_file)
                if os.path.exists(report_file_path):
                    os.remove(report_file_path)

                one_time_checker = False

        else:
            # Arm the checker so the reset can be performed on the next midnight cycle
            one_time_checker = True

            # Boundary safeguard for execution window calculation
            if start_posting_time > 11:
                start_posting_time = 8

            # Calculate current execution slot index based on offset from start window hour
            current_hour_idx = current_time.hour - start_posting_time

            # Check if calculated slot is within active scheduler dimensions
            if 0 <= current_hour_idx < table_length:
                for username, hours in timing_table.items():
                    # If current index matches 1 in both reference table and active daily pattern
                    if hours[current_hour_idx] == 1 and pattern_timing_table[username][current_hour_idx] == 1:

                        add_to_caption = all_users_data.get(username, {}).get("add_to_caption", '')
                        upload_status = post_uploader(username, add_to_caption)

                        # If upload is successfully handled, disable index in tracking to prevent repeat posting
                        if upload_status:
                            upload_status = False
                            pattern_timing_table[username][current_hour_idx] = 0
                            save_config(posting_timing_pattern_table_file, pattern_timing_table, "w")
                            
                            # Standard anti-bot sleep delay block to bypass Instagram detection
                            time.sleep(random.randint(loop_interrupt, loop_interrupt * loop_interrupt))

    # ------------------------------------------------------------------------------
    # Scenario B: Missing / Out-of-sync Configs - Regenerate and Realign Grids
    # ------------------------------------------------------------------------------
    else:
        print("Missing or modified configurations detected. Regenerating grids...")
        timing_table = {}

        save_config(insta_pattern_cfg_file, all_users_data, "w")

        # Gather target daily frequency for each user profile
        for key, value in all_users_data.items():
            user_counter[key] = int(value.get('post_in_day', 0))

        # Distribute active posting grids symmetrically across table columns
        for key, value in user_counter.items():
            if value != 0:
                row_timing_result = [0] * table_length
                
                # Case 1: Only 1 daily post -> Placed at the end of the scheduler window
                if value == 1:
                    row_timing_result[table_length - 1] = 1
                
                # Case 2: 2 daily posts -> Placed at the start and end of the schedule window
                elif value == 2:
                    row_timing_result[0] = 1
                    row_timing_result[table_length - 1] = 1
                
                # Case 3: 3 or more daily posts -> Evenly spaced across the duration
                elif value >= 3:
                    row_timing_result[0] = 1
                    row_timing_result[table_length - 1] = 1
                    remaining = value - 2
                    
                    # Calculate equal mathematically step-index coordinates
                    step = (table_length - 1) / (remaining + 1)

                    for i in range(1, remaining + 1):
                        pos = int(round(i * step))
                        row_timing_result[pos] = 1
                
                timing_table[key] = row_timing_result

        # Save freshly calculated tables back to JSON configuration files
        save_config(posting_timing_table_file, timing_table, "w")
        save_config(posting_timing_pattern_table_file, timing_table, "w")


# ==============================================================================
# 2. Continuous Process Execution Loop
# ==============================================================================

if __name__ == '__main__':
    from constants import refresh_time, loop_interrupt

    # Initialize task execution trigger rule
    schedule.every(refresh_time).minutes.do(instabot)

    # Active main thread execution polling block
    while True:
        schedule.run_pending()
        time.sleep(loop_interrupt)