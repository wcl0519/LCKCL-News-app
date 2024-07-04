# pip install azure-cognitiveservices-vision-computervision
# pip install easyocr

import os, sys, io
import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageOps, ImageColor
import bbox_visualizer as bbv  # for annotation
import easyocr

# Azure
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

# Paths
cwdir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(cwdir, "../"))
from toolbox.st_utils import show_carryyai_logo, get_image


subscription_key = '95c8fa294cdf4748afebe96b4caf8327'
endpoint = 'https://fore-student.cognitiveservices.azure.com/'


def delete_files_in_dir(dir):
	try:
		files = os.listdir(dir)
		for file in files:
			file_path = os.path.join(dir, file)
			if os.path.isfile(file_path):
				os.remove(file_path)
		st.sidebar.success("All files deleted successfully.")
	except OSError:
		st.sidebar.error("Error occurred while deleting files.")


def init_OCR():
	with st.sidebar:
		with st.expander('Camera input', expanded=True):
			img_file_buffer = st.camera_input('Take a picture')
			flag_save_img = st.button('Save image and show OCR result')

		with st.expander('Image storage', expanded=True):
			img_dir = st.text_input('Directory', value='./lcklc_2024_data/ocr/')
			flag_clear_storage = st.button('Clear image storage')

	if flag_clear_storage:
		del st.session_state['save_idx']
		delete_files_in_dir(img_dir)

	if 'save_idx' not in st.session_state:
		st.session_state['save_idx'] = 1
		
	if flag_save_img and img_file_buffer is not None:
		# Read and save image file buffer as a PIL Image
		img = Image.open(img_file_buffer)
		img.save(f'{img_dir}ocr{st.session_state["save_idx"]}.png')
		st.session_state['save_idx'] += 1
		
	return img_dir


def mod_EasyOCR():
	reader = easyocr.Reader(['ch_sim', 'en'])
	img_dir = init_OCR()
	files = os.listdir(img_dir)

	l_ocr_detected = []

	if len(files) > 0:
		# View images saved
		with st.expander('Image(s) review', expanded=True):
			tab_names = [file.split('.')[0] for file in files]
			tabs = st.tabs(tab_names)
			for tab, file in zip(tabs, files):
				with tab:
					l_col, r_col = st.columns([1, 3])
					with l_col:
						file_path = os.path.join(img_dir, file)
						img = Image.open(file_path)
						# Convert PIL Image to numpy array
						img_array = np.array(img)
						st.image(img_array, caption=str(img_array.shape))

					with r_col:
						st.markdown(reader.readtext(img_array, detail = 0))
	else:
		st.warning('Please take photo(s) and put into destinated dir')
		return


# TODO: write OCR function using Azure
def mod_Azure():
	computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
	img_dir = init_OCR()
	files = os.listdir(img_dir)

	l_ocr_detected = []

	if len(files) > 0:
		# View images saved
		with st.expander('Image(s) review', expanded=True):
			tab_names = [file.split('.')[0] for file in files]
			tabs = st.tabs(tab_names)
			for tab, file in zip(tabs, files):
				with tab:
					l_col, r_col = st.columns([1, 3])
					with l_col:
						file_path = os.path.join(img_dir, file)
						img = Image.open(file_path)
						# Convert PIL Image to numpy array
						img_array = np.array(img)
						st.image(img_array, caption=str(img_array.shape))

					with r_col:
						# with open(file_path, 'rb') as f:
						# 	img_data = f.read()
						img_data = open(file_path, 'rb')
						# Call API with URopen(file_path, 'rb')L and raw response (allows you to get the operation location)
						read_response = computervision_client.read_in_stream(img_data,  raw=True)

						# Get the operation location (URL with an ID at the end) from the response
						read_operation_location = read_response.headers["Operation-Location"]
						# Grab the ID from the URL
						operation_id = read_operation_location.split("/")[-1]

						# Call the "GET" API and wait for it to retrieve the results 
						while True:
							read_result = computervision_client.get_read_result(operation_id)
							if read_result.status not in ['notStarted', 'running']:
								break
							time.sleep(1)

						# Print the detected text, line by line
						if read_result.status == OperationStatusCodes.succeeded:
							for text_result in read_result.analyze_result.read_results:
								for line in text_result.lines:
									st.markdown(line.text)
	else:
		st.warning('Please take photo(s) and put into destinated dir')
		return

def Main():
	# Page config.
	carryai_icon = Image.open('./asset/carryai_favicon.ico')
	st.set_page_config(layout = 'wide', page_title = 'LCKCL OCR', page_icon = carryai_icon)
	show_carryyai_logo()
	with st.sidebar:
		st.header('LCKCL OCR')
		with st.expander('Info'):
			st.info('''
				This tool is a demo for LCKCL 2024 OCR project
			''')
		with st.expander('Service'):
			service_selected = st.selectbox('Select the service to use for OCR', options=['', 'EasyOCR', 'Azure'])
	
	if service_selected == '':
		st.warning(':point_left: Please select your service')
	elif service_selected == 'EasyOCR':
		mod_EasyOCR()
	elif service_selected == 'Azure':
		mod_Azure()

if __name__ == '__main__':
	Main()