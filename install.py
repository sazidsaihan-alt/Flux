import os
import sys
import subprocess

def install_flux():
    print("--- Flux Language Installer (Windows) ---")
    
    # 1. Get the current directory where Flux is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        # 2. Add this folder to the User PATH via Windows Command Line
        # We use 'setx' to make it permanent
        print(f"Adding {current_dir} to your System Path...")
        
        # Get existing path to avoid duplicates
        output = subprocess.check_output(['reg', 'query', 'HKCU\\Environment', '/v', 'Path'], shell=True).decode()
        if current_dir.lower() in output.lower():
            print("(!) Flux is already in your Path.")
        else:
            os.system(f'setx PATH "%PATH%;{current_dir}"')
            print("✔ Success: Path updated.")

        print("\n--- Installation Complete! ---")
        print("1. Close this terminal.")
        print("2. Open a NEW terminal.")
        print("3. Type 'flux' to start coding!")
        
    except Exception as e:
        print(f"✘ Error: {e}")
        print("Please try running this script as an Administrator.")

if __name__ == "__main__":
    install_flux()