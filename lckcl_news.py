# pip install azure-cognitiveservices-vision-computervision
# pip install easyocr

import os, sys, io
import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageOps, ImageColor
import bbox_visualizer as bbv  # for annotation
import easyocr

# # Azure
# from azure.cognitiveservices.vision.computervision import ComputerVisionClient
# from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
# from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
# from msrest.authentication import CognitiveServicesCredentials

# from array import array
# import os
# from PIL import Image
# import sys
# import time

# Paths
cwdir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.join(cwdir, "../"))
from toolbox.st_utils import show_carryyai_logo, get_image

# # Azure
# subscription_key = '95c8fa294cdf4748afebe96b4caf8327'
# endpoint = 'https://fore-student.cognitiveservices.azure.com/'


def button1_response():
	st.write("You clicked Button 1!")

def button2_response():
	st.write("You clicked Button 2!")


def home_page():

	# Add the CSS styles to the head section of your app
	st.write(
		"""
		<style>
		.button-style1 {
		background-color: #007bff;
		color: white;
		font-size: 16px;
		border-radius: 5px;
		padding: 10px 20px;
		}

		.button-style2 {
		background-color: #28a745;
		color: white;
		font-size: 20px;
		border-radius: 10px;
		padding: 15px 30px;
		}
		</style>
		""",
		unsafe_allow_html=True,
	)

	# Create a button with style 1
	st.button("Button 1", key="button1", class_="button-style1")

	# Create a button with style 2
	st.button("Button 2", key="button2", class_="button-style2")

	# # CSS style
	# st.markdown(
	# 	"""
	# 	<style>
	# 	.stButton button {
	# 		width: 1200px; /* Set button width */
	# 		height: 400px; /* Set button height */
	# 		font-size: 200!important; /* Adjust font size */
	# 		display: block;
	# 		margin: 0 auto; /* Center the button horizontally */
	# 	}
	# 	</style>
	# 	""",
	# 	unsafe_allow_html=True,
	# )

	# flag_news = st.button(r'$\Huge\text{日報}$')
	# flag_scan = st.button(r'$\Huge\text{掃描}$')

	# if flag_news:
	# 	st.session_state['page'] = 'NEWS'
	# 	st.rerun()
	# if flag_scan:
	# 	st.session_state['page'] = 'OCR'
	# 	st.rerun()


def create_home_button():
	flag_home = st.button(r'$\Huge\text{RETURN HOME}$', use_container_width=True)
	if flag_home:
		st.session_state['page'] = 'HOME'
		st.rerun()

def news_page():
	create_home_button()
	# CSS style
	st.markdown(
		"""
		<style>
		.stButton button {
			width: 400px; /* Set button width */
			height: 100px; /* Set button height */
			font-size: 200!important; /* Adjust font size */
		}
		</style>
		""",
		unsafe_allow_html=True,
	)
	l_col, m_col, r_col = st.columns(3)
	flag_test = l_col.button(r'$\Huge\text{TESTING}$')
	flag_test_2 = m_col.button(r'$\Huge\text{TESTING 2}$')
	flag_test_3 = r_col.button(r'$\Huge\text{TESTING 3}$')


def ocr_page():
	create_home_button()
	st.warning('OCR UNDER DEVELOPMENT')


def go_to_page():
	dict_page_func = {
		'HOME': home_page,
		'NEWS': news_page,
		'OCR': ocr_page
	}

	# Visit the page
	dict_page_func[st.session_state['page']]()
	return

def mod_display():
	# Initialize session state
	if 'page' not in st.session_state:
		st.session_state['page'] = 'HOME'

	go_to_page()

	
def Main():
	# Page config.
	carryai_icon = Image.open('./asset/carryai_favicon.ico')
	st.set_page_config(layout = 'wide', page_title = 'LCKCL OCR', page_icon = carryai_icon)
	show_carryyai_logo()
	with st.sidebar:
		st.header('LCKCL OCR')
		with st.expander('Info', expanded=True):
			st.info('''
				This tool is a demo for LCKCL 2024 News/OCR project (星島[https://std.stheadline.com/daily/%E6%97%A5%E5%A0%B1])
			''')

	mod_display()

if __name__ == '__main__':
	Main()