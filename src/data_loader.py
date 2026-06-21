import os
import pandas as pd
import requests

COLUMNS = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes',
    'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
    'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
    'su_attempted', 'num_root', 'num_file_creations', 'num_shells',
    'num_access_files', 'num_outbound_cmds', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate',
    'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
    'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count',
    'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
    'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
    'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
    'dst_host_srv_rerror_rate', 'attack_type', 'difficulty_level'
]

ATTACK_MAPPING = {
    'normal': 'Normal',
    'back': 'DoS', 'land': 'DoS', 'neptune': 'DoS', 'pod': 'DoS', 'smurf': 'DoS', 'teardrop': 'DoS', 'mailbomb': 'DoS', 'apache2': 'DoS', 'processtable': 'DoS', 'udpstorm': 'DoS',
    'ipsweep': 'Probe', 'nmap': 'Probe', 'portsweep': 'Probe', 'satan': 'Probe', 'mscan': 'Probe', 'saint': 'Probe',
    'ftp_write': 'R2L', 'guess_passwd': 'R2L', 'imap': 'R2L', 'multihop': 'R2L', 'phf': 'R2L', 'spy': 'R2L', 'warezclient': 'R2L', 'warezmaster': 'R2L', 'sendmail': 'R2L', 'named': 'R2L', 'snmpgetattack': 'R2L', 'snmpguess': 'R2L', 'xlock': 'R2L', 'xsnoop': 'R2L', 'httptunnel': 'R2L',
    'buffer_overflow': 'U2R', 'loadmodule': 'U2R', 'perl': 'U2R', 'rootkit': 'U2R', 'sqlattack': 'U2R', 'xterm': 'U2R', 'ps': 'U2R'
}

TARGET_ENCODING = {'Normal': 0, 'DoS': 1, 'Probe': 2, 'R2L': 3, 'U2R': 4}
REVERSE_TARGET_ENCODING = {v: k for k, v in TARGET_ENCODING.items()}

TRAIN_URL = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTrain%2B.txt"
TEST_URL = "https://raw.githubusercontent.com/defcom17/NSL_KDD/master/KDDTest%2B.txt"

def download_file(url, path):
    if not os.path.exists(path):
        print(f"Downloading {url} to {path}...")
        response = requests.get(url)
        response.raise_for_status()
        with open(path, 'wb') as f:
            f.write(response.content)
        print("Download complete.")

def load_data(data_dir="data"):
    os.makedirs(data_dir, exist_ok=True)
    train_path = os.path.join(data_dir, "KDDTrain+.csv")
    test_path = os.path.join(data_dir, "KDDTest+.csv")
    
    download_file(TRAIN_URL, train_path)
    download_file(TEST_URL, test_path)
    
    # Read the CSV files
    train_df = pd.read_csv(train_path, names=COLUMNS, index_col=False)
    test_df = pd.read_csv(test_path, names=COLUMNS, index_col=False)
    
    # Drop difficulty_level as it's not a feature
    train_df = train_df.drop('difficulty_level', axis=1, errors='ignore')
    test_df = test_df.drop('difficulty_level', axis=1, errors='ignore')
    
    # Map fine-grained attacks to 5 main categories
    train_df['attack_class'] = train_df['attack_type'].map(ATTACK_MAPPING)
    test_df['attack_class'] = test_df['attack_type'].map(ATTACK_MAPPING)
    
    # Drop records with unknown attack types
    train_df = train_df.dropna(subset=['attack_class'])
    test_df = test_df.dropna(subset=['attack_class'])
    
    # Drop original attack_type
    train_df = train_df.drop('attack_type', axis=1)
    test_df = test_df.drop('attack_type', axis=1)
    
    # Encode targets
    train_df['target'] = train_df['attack_class'].map(TARGET_ENCODING)
    test_df['target'] = test_df['attack_class'].map(TARGET_ENCODING)
    
    X_train = train_df.drop(['attack_class', 'target'], axis=1)
    y_train = train_df['target']
    X_test = test_df.drop(['attack_class', 'target'], axis=1)
    y_test = test_df['target']
    
    return X_train, y_train, X_test, y_test

if __name__ == "__main__":
    X_train, y_train, X_test, y_test = load_data()
    print("Train shape:", X_train.shape, y_train.shape)
    print("Test shape:", X_test.shape, y_test.shape)
    print("Class distribution (train):")
    print(y_train.value_counts().rename(index=REVERSE_TARGET_ENCODING))
