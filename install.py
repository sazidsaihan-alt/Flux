import os
import sys

def install():
    path = os.getcwd()
    print(f"Installing Flux from: {path}")
    
    # This command adds the current folder to the Windows User PATH
    os.system(f'setx PATH "%PATH%;{path}"')
    
    print("\nFlux has been added to your PATH!")
    print("Please restart your terminal and type 'flux' to begin.")

if __name__ == "__main__":
    install()