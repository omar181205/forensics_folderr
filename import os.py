import os
from Registry import Registry

REQUIRED_HIVES = ["SOFTWARE", "SAM", "SYSTEM"]

def get_path(name: str) -> str:
    while True:
        path = input(f"Enter path to '{name}' hive: ")
        path = path.strip('"')
        if os.path.exists(path) and os.path.isfile(path):
            return path
        else:
            print(f"Error: File not found at '{path}'. Try again.")

def analyze_apps(path: str):
    print("\n--- INSTALLED APPLICATIONS (ALL ENTRIES) ---")
    try:
        reg = Registry.Registry(path)
        uninstall_paths = [
            r"Microsoft\Windows\CurrentVersion\Uninstall",
            r"Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        apps = []

        # Adopted user's loop structure for opening the key
        for key_path in uninstall_paths:
            try:
                key = reg.open(key_path)
            except:
                continue

            for subkey in key.subkeys():
                # Extract details, falling back to key name or "N/A" if value is missing
                
                # Get DisplayName, falling back to key name (GUID) if missing
                name = subkey.value("DisplayName").value() if "DisplayName" in subkey.values() and subkey.value("DisplayName").value() else subkey.name()
                
                # Get Version/Publisher, falling back to "N/A"
                version = subkey.value("DisplayVersion").value() if "DisplayVersion" in subkey.values() else "N/A"
                publisher = subkey.value("Publisher").value() if "Publisher" in subkey.values() else "N/A"
                
                # Only append if a name (either DisplayName or GUID) was found
                if name and name.strip():
                    apps.append(f"{name} (Version: {version}, Publisher: {publisher})")

        if not apps:
            print("No applications found.")
        
        # Use set to ensure unique entries, then sort and print
        for app in sorted(list(set(apps))):
            print(f"- {app}")
            
    except Exception as e:
        print(f"[ERROR] SOFTWARE analysis failed: {e}")

def analyze_system_info(path: str):
    print("\n--- OPERATING SYSTEM DETAILS ---")
    try:
        reg = Registry.Registry(path)
        os_key_path = r"Microsoft\Windows NT\CurrentVersion"
        os_key = reg.open(os_key_path)
        
        product_name = os_key.value("ProductName").value() if "ProductName" in os_key.values() else "N/A"
        current_version = os_key.value("CurrentVersion").value() if "CurrentVersion" in os_key.values() else "N/A"
        build_number = os_key.value("CurrentBuildNumber").value() if "CurrentBuildNumber" in os_key.values() else "N/A"
        service_pack = os_key.value("CSDVersion").value() if "CSDVersion" in os_key.values() else "None"

        print(f"- OS Name:      {product_name}")
        print(f"- Version:      {current_version}")
        print(f"- Build Number: {build_number}")
        print(f"- Service Pack: {service_pack}")
        print(f"- Registry Path: \\{os_key_path}")
            
    except Exception as e:
        print(f"[ERROR] OS details analysis failed: {e}")

def analyze_users(path: str):
    print("\n--- USER ACCOUNTS ---")
    try:
        reg = Registry.Registry(path)
        names_root_path = r"SAM\Domains\Account\Users\Names"
        names_key = reg.open(names_root_path)
        
        users = []
        
        for name_subkey in names_key.subkeys():
            username = name_subkey.name()
            
            if "CMI-CreateHive" not in username and username.lower() not in ['administrator', 'guest', 'defaultuser0']:
                full_reg_path = f"\\{names_root_path}\\{username}"
                
                users.append({'name': username, 'path': full_reg_path})
                    
        output_lines = []
        for user in sorted(users, key=lambda u: u['name']):
            output_lines.append(f"- User: {user['name']}")
            output_lines.append(f"  Name Path: {user['path']}")
        
        if not output_lines:
            print("No non-default user accounts found.")
            return

        for line in output_lines:
            print(line)
            
    except Exception as e:
        print(f"[ERROR] SAM analysis failed: {e}")

def analyze_usb(path: str):
    print("\n--- USB DEVICE HISTORY ---")
    try:
        reg = Registry.Registry(path)
        usb_root_path = r"ControlSet001\Enum\USBSTOR"
        usb_key = reg.open(usb_root_path)
        devices = []
        
        for vendor_key in usb_key.subkeys():
            for serial_key in vendor_key.subkeys():
                name = serial_key.value("FriendlyName").value() if "FriendlyName" in serial_key.values() else serial_key.name()
                
                full_reg_path = f"\\{usb_root_path}\\{vendor_key.name()}\\{serial_key.name()}"
                
                devices.append({'name': name, 'serial': serial_key.name(), 'path': full_reg_path})
        
        output_lines = []
        for device in sorted(devices, key=lambda d: d['name']):
            output_lines.append(f"- Device: {device['name']}")
            output_lines.append(f"  Serial: {device['serial']}")
            output_lines.append(f"  Path:   {device['path']}")
        
        if not output_lines:
            print("No USB device history found.")
            return
            
        for line in output_lines:
            print(line)
            
    except Exception as e:
        print(f"[ERROR] SYSTEM analysis failed: {e}")

def main():
    print("--- MINIMAL FORENSIC HIVE ANALYZER ---")
    
    hive_paths = {name: get_path(name) for name in REQUIRED_HIVES}
        
    analyze_system_info(hive_paths["SOFTWARE"])
    analyze_apps(hive_paths["SOFTWARE"])
    analyze_users(hive_paths["SAM"])
    analyze_usb(hive_paths["SYSTEM"])
    print("\n--- ANALYSIS COMPLETE ---")

if __name__ == "__main__":
    main()