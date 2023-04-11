if [ ! -d "venv" ]; then
    echo "No virtual environment found with name 'venv', checking system python version"
    python_installed=false
    # only set python_installed to true if precisely python3.10 is installed
    command -v python3.10 >/dev/null 2>&1 && python_installed=true
    if python_installed; then
        echo "Confirmed Python 3.10 installed in system"
        echo "Generating vitual environment"
        python3.10 -m venv venv
        echo "Activating environment"
        source venv/bin/activate
        echo "Installing requirements"
        pip install -m requirements.txt
        echo "Finished setup, deactivating and continuing normally"
    else
        echo "Python 3.10 not found in system, please install it to continue."
        exit
    fi
fi
echo "Activating virtual environment"
source venv/bin/activate
if { python3.10 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))'; echo "3.10"; } | sort --version-sort --check &> /dev/null; then
  echo "Virtual environment python version is less than 3.10. Please delete the venv directory and run this script again to create a new one."
  exit
fi
cd src
echo "Starting bot"
python main.py