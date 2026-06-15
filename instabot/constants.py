# ==============================================================================
# Instabot Global Constants and Configurations
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. Directories and File Configuration
# ------------------------------------------------------------------------------
downloads_folder = "downloads"
configs_folder = "configs"
sessions_folder = "sessions"

insta_cfg_file = "insta_configs.json"
insta_pattern_cfg_file = "insta_pattern_configs.json"
posting_timing_table_file = "posting_timing_table.json"
report_posted_file = 'report_posted.json'
posting_timing_pattern_table_file = "posting_timing_pattern_table.json"

# ------------------------------------------------------------------------------
# 2. Font Asset Paths (Persian & Arabic RTL compatible fonts)
# ------------------------------------------------------------------------------
video_font_path = "./fonts/vazir.ttf"
cover_font_path = "./fonts/lalezar.ttf"

# ------------------------------------------------------------------------------
# 3. Timing and Scheduler Configurations
# ------------------------------------------------------------------------------
table_length = 13               # Number of active schedule hours checked daily in the timing table
start_posting_time = 9          # Active window starts daily at 9:00 AM (local time)
refresh_time = 10               # Scheduler execution polling check rate (in minutes)
login_check_count = 3           # Max consecutive retry attempts for validating Instagram logins
loop_interrupt = 10             # Safety sleep cycle block (in seconds)

# ------------------------------------------------------------------------------
# 4. Username Categorizations
# ------------------------------------------------------------------------------
# Accounts requiring dynamic cover thumbnail images to be generated and added
covergraphi_usernames = [
    "toofunii", 
    "kharidpedia", 
    "grlsrls", 
    "rish_sefid_net", 
    "shopiko_ir", 
    "soofunii"
]

# Accounts requiring text watermarks overlaid on the top of published videos
textgraphi_usernames = [
    "toofunii", 
    "kharidpedia", 
    "grlsrls", 
    "shopiko_ir", 
    "soofunii"
]

# Accounts published exclusively in English (determines which language call-to-action is used)
english_pages = ["soofunii"]

# ------------------------------------------------------------------------------
# 5. Call to Action (CTA) Suffix Texts
# ------------------------------------------------------------------------------
call_to_action = "لایک و فالو کن، بفرست رفیقات"
english_call_to_action = "Like, follow, share friends"

# ------------------------------------------------------------------------------
# 6. Media Aspect Ratio Limitations
# ------------------------------------------------------------------------------
# Valid aspect ratio dimensions allowed by Instagram API (Width/Height)
# Normal vertical bounds range between 0.54716 (~9:16) and 1.92910 (~16:9 landscape)
min_aspect_ratio = 0.54716
max_aspect_ratio = 1.92910

# Dev Note on previous validation exception bounds:
# Invalid aspect ratio error was caught at:
# !0.5568749904632568 < 0.5471698113207547 < 1.9291000366210938