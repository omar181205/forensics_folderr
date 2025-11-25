import os
from Registry import Registry

def get_path(name: str) -> str:
    while True:
        path = input(f"Enter path to '{name}' hive: ").strip('"')
        if os.path.exists(path) and os.path.isfile(path):
            return path
        else:
            print(f"Error: File not found at '{path}'. Try again.")

def list_installed_apps(path: str):
    print("\n--- INSTALLED APPLICATIONS ---")
    try:
        reg = Registry.Registry(path)
        paths = [r"Microsoft\Windows\CurrentVersion\Uninstall", r"Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"]
        apps = []
        
        for p in paths:
            try:
                key = reg.open(p)
            except: continue

            for sub in key.subkeys():
                name, publisher, version = None, None, None
                
                for v in sub.values():
                    if v.name() == "DisplayName": name = v.value()
                    elif v.name() == "Publisher": publisher = v.value()
                    elif v.name() == "DisplayVersion": version = v.value()

                if name:
                    apps.append({
                        "name": name, 
                        "publisher": publisher if publisher else "N/A", 
                        "version": version if version else "N/A"
                    })

        if not apps:
            print("No applications with DisplayName found.")
            return

        for app in sorted(apps, key=lambda x: x['name']):
            print(f"- {app['name']}")
            print(f"    Publisher: {app['publisher']}")
            print(f"    Version:   {app['version']}")
            print()
            
    except Exception as e:
        print(f"[ERROR] Application analysis failed: {e}")


def main():
    print("--- INSTALLED APPLICATIONS ANALYZER ---")
    software_hive_path = get_path("SOFTWARE")
    list_installed_apps(software_hive_path)
    print("\n--- ANALYSIS COMPLETE ---")

if __name__ == "__main__":
    main()