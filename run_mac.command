#!/bin/zsh

script_dir="$(dirname "$(realpath "$0")")"

cd "$script_dir" || exit 1

if [ ! -d "venv" ]
then
    python3 -m venv venv
fi

source venv/bin/activate
pip3 install -r requirements.txt
python3 scraping.py
deactivate
rm -r output

osascript -e 'tell application "Terminal" to close first window' & exit