if [ ! -d "venv" ]; then
    echo "No virtual environment found with name 'venv', checking system python version"
    if command -v python3.10 >/dev/null 2>&1; then
        echo "Confirmed Python 3.10 installed in system"
        echo "Generating vitual environment"
        python3.10 -m venv venv
        echo "Activating environment"
        source venv/bin/activate
        echo "Updating pip"
        pip install --upgrade pip
        echo "Installing requirements"
        pip install -r requirements.txt
        echo "Finished setup, deactivating and continuing normally"
    else
        echo "Python 3.10 not found in system, please install it to continue."
        exit 1
    fi
fi
echo "Activating virtual environment"
source venv/bin/activate
if { python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))'; echo "3.10"; } | sort --version-sort --check &> /dev/null; then
  echo "Virtual environment python version is less than 3.10. Please delete the venv directory and run this script again to create a new one."
  exit 1
fi
cd src
echo "Starting bot"
python main.py