import streamlit as st
from PIL import Image
from streamlit_extras.stylable_container import stylable_container

import requests
from bs4 import BeautifulSoup
import emoji

import pyttsx3
import time

# Initialize sound output driver
engine = pyttsx3.init(driverName="sapi5")  # Use the Microsoft Speech Platform: sapi5
voices = engine.getProperty('voices')

for voice in voices:
	if 'ZH-HK' in voice.id.split('\\')[-1]:
		engine.setProperty('voice', voice.id)
		break

engine.setProperty('rate',150 )
engine.setProperty('volume',1)
# engine.say('你好，你好嗎?')
# engine.runAndWait()

def web_scrape_title(url):
	# Send a GET request to the webpage
	response = requests.get(url)

	result_dict = {}
	# Check if the request was successful
	if response.status_code == 200:
		# Parse the HTML content of the page
		soup = BeautifulSoup(response.content, "html.parser")
		title_elements = soup.find_all(class_="title")  # Find all elements with class "title"

		result_dict = {}  # Initialize an empty dictionary

		for title in title_elements:
			text = title.get_text()  # Get the text of the element
			href = title.get("href")  # Get the value of the href attribute
			result_dict[text] = href  # Add key-value pair to the dictionary

	else:
		print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
	
	return result_dict


def mod_display():
	with st.sidebar:
		with stylable_container(
			key='detail_sidebar_button',
			css_styles="""
				button {
					background-color: white;
					width: 300px;
					height: 120px;
				}

				.custom-emoji {
					font-size: 5em;
				}

				.emoji-button {
					font-size: 5em;
					padding: 0.2em;
				}				

				"""
		):
			# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
			# st.button(f'<span class="custom-emoji">{emoji.emojize(":black_right_pointing_triangle_with_double_vertical_bar:")}</span>', unsafe_allow_html=True)
			st.button(':black_right_pointing_triangle_with_double_vertical_bar:', use_container_width=True)
			st.button(':black_square_for_stop:', use_container_width=True)
			st.button(':fast_forward:', use_container_width=True)
			st.button(':rewind:', use_container_width=True)
			st.button(':heavy_plus_sign:', use_container_width=True)
			st.button(':heavy_minus_sign:', use_container_width=True)
			# st.write(f'<span class="custom-emoji">{emoji.emojize(":smile:")}</span>', unsafe_allow_html=True)
			st.toast('語音速度: 正常')

	l_col, r_col = st.columns(2)
	with l_col:
		with stylable_container(
			key='return_home_button',
			css_styles="""
				button {
					background-color: orange;
					color: white;
					border-radius: 10px;
					width: 400px;
					height: 100px;

					/* Center the button horizontally */
					display: block;
					margin: 0 auto; 
				}
				"""
		):
			if st.button(r'$\Huge\text{主頁}$'):
				st.switch_page("home.py")
	with r_col:
		with stylable_container(
			key='news_button',
			css_styles="""
				button {
					background-color: orange;
					color: white;
					border-radius: 10px;
					width: 400px;
					height: 100px;

					/* Center the button horizontally */
					display: block;
					margin: 0 auto; 
				}
				"""
		):
			if st.button(r'$\Huge\text{日報}$'):
				st.switch_page("pages/news_home.py")
	
	cur_url = st.session_state['dict_cat'][st.session_state['cur_page']]
	dict_title = web_scrape_title(cur_url)
	for title, title_url in dict_title.items():
		# st.write(f'<a href="{title_url}">{title}</a>')
		#print('title_url',title_url)
		# 
		st.info(title)
		engine.say(title)
		# st.page_link(page= title_url, label= title)
		# st.markdown(title_url)
		
		engine.runAndWait()
		time.sleep(2)

	engine.stop()
	engine.runAndWait()
	# engine.close()

def Main():
	# Page config.
	carryai_icon = Image.open('./asset/carryai_favicon.ico')
	st.set_page_config(layout = 'wide', page_title = 'LCKCL News app', page_icon = carryai_icon)
	
	mod_display()

if __name__ == '__main__':
	Main()