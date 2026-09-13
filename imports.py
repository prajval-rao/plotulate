from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import RedirectResponse
import io
import pandas as pd
import openpyxl
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import python_multipart