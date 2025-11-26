import os
from Registry import Registry


NTUSER_ADMIN_PATH = "C:\\Users\\omara\\Downloads\\CW Disk Image\\NTUSERadmin.DAT"
NTUSER_INFO_PATH = "C:\\Users\\omara\\Downloads\\CW Disk Image\\NTUSERinfo.DAT"

def get_system_path(name: str) -> str:
    """Gets and validates the path for the SYSTEM hive."""
    while True:
        path = input(f"Enter path to '{name}' hive: ").strip('"')
        if os.path.exists(path) and os.path.isfile(path):
            return path
        else:
            print(f"Error: File not found at '{path}'. Try again.")

def analyze_usb(system_hive_path: str):
    print("\n--- USB DEVICE HISTORY (from SYSTEM Hive) ---")
    try:
        reg = Registry.Registry(system_hive_path)
        usb_root_path = r"ControlSet001\Enum\USBSTOR"
        usb_key = reg.open(usb_root_path)
        devices = []
        
        for vendor_key in usb_key.subkeys():
            for serial_key in vendor_key.subkeys():
                name = serial_key.value("FriendlyName").value() if "FriendlyName" in serial_key.values() else serial_key.name()
                full_reg_path = f"\\{usb_root_path}\\{vendor_key.name()}\\{serial_key.name()}"
                
                devices.append({'name': name, 'serial': serial_key.name(), 'path': full_reg_path})
        
        if not devices:
            print("No USB device history found.")
            return

        for device in sorted(devices, key=lambda d: d['name']):
            print(f"- Device: {device['name']}")
            print(f"  Serial: {device['serial']}")
            print(f"  Path:   {device['path']}")
            
    except Exception as e:
        print(f"[ERROR] SYSTEM analysis failed: {e}")

def analyze_command_history(ntuser_hive_path: str, username: str):
    print(f"\n--- COMMAND HISTORY / USER ACTIVITY (from {username}'s NTUSER Hive) ---")
    try:
        reg = Registry.Registry(ntuser_hive_path)
        user_assist_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist"
        user_activity = []
        root_key = reg.open(user_assist_path)
        
        for guid_key in root_key.subkeys():
            if r"Count" in guid_key.subkeys():
                count_key = guid_key.subkeys()[r"Count"]
                
                for value in count_key.values():
                    program_name_raw = value.name() 
                    execution_details = f"(Value Data Size: {len(value.value())} bytes)" 
                    full_reg_path = f"\\{user_assist_path}\\{guid_key.name()}\\Count"
                    
                    user_activity.append({
                        'program_raw': program_name_raw,
                        'details_raw': execution_details,
                        'path': full_reg_path
                    })
        
        if not user_activity:
            print(f"No UserAssist execution records found for {username}.")
            return

        print("--- NOTE: Program keys are ROT13 encoded and must be decoded externally ---")
        for activity in sorted(user_activity, key=lambda a: a['program_raw']):
            print(f"- Raw Program Key: {activity['program_raw']}")
            print(f"  Raw Details:     {activity['details_raw']}")
            print(f"  Path:            {activity['path']}")
            
    except Exception as e:
        print(f"[ERROR] User Activity analysis for {username} failed: {e}")

def main():
    print("--- COMPREHENSIVE FORENSIC ACTIVITY ANALYZER ---")
    system_hive_path = get_system_path("SYSTEM")
    analyze_usb(system_hive_path)
    
    print("\n--- START NTUSER HIVE ANALYSIS ---")
    print(f"Analyzing admin user hive at: {NTUSER_ADMIN_PATH}")
    analyze_command_history(NTUSER_ADMIN_PATH, "admin") 

    print(f"\nAnalyzing info user hive at: {NTUSER_INFO_PATH}")
    analyze_command_history(NTUSER_INFO_PATH, "info")

    print("\n--- ANALYSIS COMPLETE ---")

if __name__ == "__main__":
    main()