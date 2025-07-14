import sys, os



sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../..", "src"))

from active_directory.config import Active_Directory
from fastapi import APIRouter, HTTPException,Depends
from utils import generate_response
from send_notify.service import generate_message

title="test"
field_values= {"ip":"1,2,3,4","host":"4.3.23.1","resson":"test"}
print(generate_message(title,field_values))