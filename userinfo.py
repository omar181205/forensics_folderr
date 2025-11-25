import os
from Registry import Registry

def get_path(name: str) -> str:
    """Gets and validates the path for a hive file."""
    while True:
        path = input(f"Enter path to '{name}' hive: ").strip('"')
        if os.path.exists(path) and os.path.isfile(path):
            return path
        else:
            print(f"Error: File not found at '{path}'. Try again.")

def analyze_users(sam_hive_path: str):
    """
    Extracts non-default user accounts and their corresponding Registry paths 
    from the SAM hive using the highly stable 'Names' key.
    """
    print("\n--- USER ACCOUNTS ---")
    try:
        reg = Registry.Registry(sam_hive_path)
        names_root_path = r"SAM\Domains\Account\Users\Names"
        
        # 1. Open the key that lists all usernames
        names_key = reg.open(names_root_path)
        
        users = []
        
        for name_subkey in names_key.subkeys():
            username = name_subkey.name()
            
            # Simple check to filter out known system keys (Administrator, Guest, DefaultUser, etc.)
            if "CMI-CreateHive" not in username and username.lower() not in ['administrator', 'guest', 'defaultuser0']:
                
                # Construct the full Registry path for the Name key
                full_reg_path = f"\\{names_root_path}\\{username}"
                
                users.append({
                    'name': username, 
                    'path': full_reg_path
                })
                    
        output_lines = []
        
        if not users:
            print("No non-default user accounts found.")
            return

        for user in sorted(users, key=lambda u: u['name']):
            output_lines.append(f"- User: {user['name']}")
            output_lines.append(f"  Name Path: {user['path']}")
        
        for line in output_lines:
            print(line)
            
    except Exception as e:
        print(f"[ERROR] SAM analysis failed: {e}")

def main():
    print("--- USER ACCOUNT ANALYZER ---")
    sam_hive_path = get_path("SAM")
    analyze_users(sam_hive_path)
    print("\n--- ANALYSIS COMPLETE ---")

if __name__ == "__main__":
    main()