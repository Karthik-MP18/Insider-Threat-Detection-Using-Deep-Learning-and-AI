# Load device.csv
device_df = pd.read_csv('device.csv', names=['id', 'date', 'user', 'pc', 'activity'], header=None)

# Load http.csv
http_df = pd.read_csv('http.csv', names=['id', 'date', 'user', 'pc', 'url'], header=None)

# Load logon.csv
logon_df = pd.read_csv('logon.csv', names=['id', 'date', 'user', 'pc', 'activity'], header=None)

# Preprocess dates
for df in [device_df, http_df, logon_df]:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Extract hour
device_df['hour'] = device_df['date'].dt.hour
device_df['after_hours'] = device_df['hour'].apply(lambda x: 1 if (x < 8 or x > 18) else 0)

# Filter only Connect/Disconnect activities
device_df_filtered = device_df[device_df['activity'].isin(['Connect', 'Disconnect'])]

# Count removable drive use
device_use = device_df_filtered.groupby('user')['activity'].value_counts().unstack().fillna(0)
device_use['removable_drive_use'] = device_use.get('Connect', 0) + device_use.get('Disconnect', 0)

# After-hours device use
after_hours_device_use = device_df_filtered.groupby('user')['after_hours'].sum()

# Frequent USB use flag
device_use['frequent_usb_activity'] = device_use['removable_drive_use'].apply(lambda x: 1 if x > 10 else 0)

# Logon features
logon_df['hour'] = logon_df['date'].dt.hour
logon_df['after_hours'] = logon_df['hour'].apply(lambda x: 1 if (x < 8 or x > 18) else 0)

# Logon/Logoff features
logon_behavior = logon_df.groupby('user').agg({
    'after_hours': 'sum',
    'activity': 'count'
}).rename(columns={'activity': 'total_logons'})

# Define site categories
common_job_sites = ['job', 'career', 'linkedin', 'indeed', 'glassdoor', 'monster', 'zippercutter', 'workday', 'hired', 'career',
    'simplyhired', 'naukri', 'rozee', 'bayt', 'dice', 'craigslist', 'snagajob', 'upwork', 'freelancer', 'flyerr']
common_storage_sites = ['dropbox', 'drive.google', 'mega.nz', 'box.com', 'icloud.com', 'onedrive']
common_social_sites = ['facebook', 'instagram', 'tiktok', 'twitter', 'reddit', 'pinterest', 'tumblr', 'snapchat']
common_filesharing_sites = ['wetransfer', 'sendspace', 'mediafire', 'zippyshare', 'gofile', 'fileserve', 'filesonic']

# Categorize URLs
def detect_category(url):
    url = str(url).lower()
    if any(word in url for word in common_job_sites):
        return 'job_site'
    elif any(word in url for word in common_storage_sites):
        return 'storage_site'
    elif any(word in url for word in common_social_sites):
        return 'social_media'
    elif any(word in url for word in common_filesharing_sites):
        return 'file_sharing'
    else:
        return 'other_unknown'

http_df['site_category'] = http_df['url'].apply(detect_category)
http_df['hour'] = http_df['date'].dt.hour
http_df['after_hours'] = http_df['hour'].apply(lambda x: 1 if (x < 8 or x > 18) else 0)

# Detect after-hours risky site visits
def detect_suspicious_visit(row):
    risky = ['job_site', 'storage_site', 'file_sharing']
    return 1 if row['site_category'] in risky and row['after_hours'] == 1 else 0

http_df['suspicious_visit'] = http_df.apply(detect_suspicious_visit, axis=1)

# Summarize per user
http_behavior = http_df.groupby('user').agg({
    'suspicious_visit': 'sum',
    'site_category': 'count'
}).rename(columns={'site_category': 'total_sites_visited'})

# Novelty detection: unknown site spike
http_behavior['novelty_flag'] = http_behavior['total_sites_visited'].apply(lambda x: 1 if x > 10 else 0)

# Create features DataFrame
features = pd.DataFrame(index=list(set(device_use.index) | set(logon_behavior.index) | set(http_behavior.index)))

# Merge device features
features = features.join(device_use[['removable_drive_use', 'frequent_usb_activity']], how='left')
features = features.join(after_hours_device_use.rename('after_hours_device_use'), how='left')

# Merge Logon features
features = features.join(logon_behavior[['after_hours', 'total_logons']], how='left')

# Merge HTTP features
features = features.join(http_behavior[['suspicious_visit', 'novelty_flag']], how='left')

# Fill NaN with 0
features.fillna(0, inplace=True)

# Assign labels
def assign_label(row):
    suspicious_flags = 0
    if row['after_hours'] > 3:
        suspicious_flags += 1
    if row['after_hours_device_use'] > 2:
        suspicious_flags += 1
    if row['suspicious_visit'] > 2:
        suspicious_flags += 1
    if row['frequent_usb_activity'] == 1:
        suspicious_flags += 1
    if row['novelty_flag'] == 1:
        suspicious_flags += 1
    return 1 if suspicious_flags >= 2 else 0

features['label'] = features.apply(assign_label, axis=1)
