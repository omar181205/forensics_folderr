DISK_IMAGE_PATH = r"C:\Users\omara\Downloads\CW Disk Image\CWImage.dd"

# 2. Installed Applications (Extracted from SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall)
application_data = [
    {"Application": "Google Chrome", "Version": "127.0.6533.100", "Publisher": "Google LLC"},
    {"Application": "VLC Media Player", "Version": "3.0.18", "Publisher": "VideoLAN"},
    {"Application": "Malware Hunter Pro", "Version": "2.1.0", "Publisher": "Suspicious Devs Inc."},
    {"Application": "Python 3.11.4", "Version": "3.11.4150.0", "Publisher": "Python Software Foundation"},
]

# 3. User Accounts and Registry Info (Extracted from SAM and NTUSER.DAT hives)
user_account_data = [
    {"Username": "omara", "RID": "1001", "Last Login": "2025-11-25 09:30:00 UTC", "Admin Status": "Yes"},
    {"Username": "Guest", "RID": "501", "Last Login": "N/A", "Admin Status": "No"},
    {"Username": "Administrator", "RID": "500", "Last Login": "2025-06-15 10:00:00 UTC", "Admin Status": "Yes"},
]

# 4. USB History (Extracted from SYSTEM\CurrentControlSet\Enum\USBSTOR)
usb_history_data = [
    {"Device Type": "SanDisk USB 3.0", "Serial Number": "ABCD1234EF", "Vendor ID": "0781", "First Connect": "2025-10-01 14:22:00 UTC"},
    {"Device Type": "WD Elements External", "Serial Number": "FGHJ5678KL", "Vendor ID": "1058", "First Connect": "2025-11-20 08:45:00 UTC"},
]

# 5. Command History/Recent Activity (Extracted from Shellbags, LNK files, and UserAssist)
command_history_data = [
    {"Artifact": "UserAssist", "Program": "cmd.exe", "Run Count": 15, "Last Run": "2025-11-25 09:28:00 UTC"},
    {"Artifact": "Shellbag", "Path": "C:\\Users\\omara\\Documents\\Secret_Files", "Accessed": "2025-11-24 16:05:00 UTC"},
    {"Artifact": "LNK File", "Target": "C:\\Windows\\System32\\powercfg.exe", "Created": "2025-11-25 09:20:00 UTC"},
]

def print_section_header(title):
    """Prints a standardized header for each report section."""
    print("\n" + "=" * 60)
    print(f"--- {title} ---")
    print("=" * 60)

def print_application_report():
    """Prints the Installed Applications section."""
    print_section_header("1. Installed Applications")
    for i, app in enumerate(application_data, 1):
        print(f"  {i}. {app.get('Application', 'N/A')}")
        print(f"     Version: {app.get('Version', 'N/A')}")
        print(f"     Publisher: {app.get('Publisher', 'N/A')}\n")

def print_user_account_report():
    """Prints the User Accounts and Registry Info section."""
    print_section_header("2. User Accounts and Registry Info")
    for i, user in enumerate(user_account_data, 1):
        print(f"  {i}. Username: {user.get('Username', 'N/A')} (RID: {user.get('RID', 'N/A')})")
        print(f"     Admin Status: {user.get('Admin Status', 'N/A')}")
        print(f"     Last Login: {user.get('Last Login', 'N/A')}\n")

def print_usb_history_report():
    """Prints the USB History section."""
    print_section_header("3. USB Device History (Registry: USBSTOR)")
    for i, usb in enumerate(usb_history_data, 1):
        print(f"  {i}. Device: {usb.get('Device Type', 'N/A')}")
        print(f"     Serial: {usb.get('Serial Number', 'N/A')}")
        print(f"     First Connected: {usb.get('First Connect', 'N/A')}\n")

def print_command_history_report():
    """Prints the Command History and Recent Activity section."""
    print_section_header("4. Command History & Recent Activity")
    for i, cmd in enumerate(command_history_data, 1):
        print(f"  {i}. Artifact Type: {cmd.get('Artifact', 'N/A')}")
        print(f"     Details: {cmd.get('Program', cmd.get('Path', cmd.get('Target', 'N/A')))}")
        print(f"     Timestamp: {cmd.get('Last Run', cmd.get('Accessed', cmd.get('Created', 'N/A')))}\n")


def generate_forensic_report():
    """Main function to generate the complete forensic report."""
    
    print("====================================================================")
    print(f"  FORENSIC ARTIFACT REPORT GENERATOR")
    print(f"  Target Image: {DISK_IMAGE_PATH}")
    print("====================================================================")
    
    # Run all report sections
    print_application_report()
    print_user_account_report()
    print_usb_history_report()
    print_command_history_report()

    # --- Forensic Script Validation and Interpretation Guidance ---
    print_section_header("5. Validation and Interpretation Guidance")
    
    print("Validation (Manual Check against Tool Output):")
    print("---------------------------------------------")
    print("To validate this script's *placeholder* output:")
    print("1. Run Autopsy (or FTK Imager) on the CWImage.dd file.")
    print("2. Navigate to 'Artifacts' (for Applications, USB) and 'Operating System' (for Users).")
    print("3. Compare the list of Applications, Users, and USB devices found by the professional tool to the lists printed above.")
    print("   *Example:* Does Autopsy list 'Malware Hunter Pro'? (If so, validation successful.)")

    print("\nInterpretation (Using an LLM/ChatGPT):")
    print("----------------------------------------")
    print("Use the following template to ask an LLM about your findings:")
    print('  "I found the following evidence on a forensic image: 1. Installed Application: Malware Hunter Pro, 2. USB Device: SanDisk USB 3.0, 3. User Command: ran cmd.exe 15 times. What is the potential significance of these findings in a digital crime investigation?"')
    print("\n====================================================================")


# Run the function when the script starts
if __name__ == "__main__":
    generate_forensic_report()