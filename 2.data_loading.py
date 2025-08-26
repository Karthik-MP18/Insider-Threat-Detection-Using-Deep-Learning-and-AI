# Load device.csv
device_df = pd.read_csv('device.csv', names=['id', 'date', 'user', 'pc', 'activity'], header=None)

# Load http.csv
http_df = pd.read_csv('http.csv', names=['id', 'date', 'user', 'pc', 'url'], header=None)

# Load logon.csv
logon_df = pd.read_csv('logon.csv', names=['id', 'date', 'user', 'pc', 'activity'], header=None)
