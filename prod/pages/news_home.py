import streamlit as st
from PIL import Image
from streamlit_extras.stylable_container import stylable_container

import requests
from bs4 import BeautifulSoup

def web_scrape_cat(url):
	# Send a GET request to the webpage
	response = requests.get(url)

	result_dict = {}
	# Check if the request was successful
	if response.status_code == 200:
		# Parse the HTML content of the page
		soup = BeautifulSoup(response.content, "html.parser")

		main_nav = soup.find("div", id="mainNav")

		nav_items = main_nav.find_all("li", class_="nav-item")

		for item in nav_items:
			title = item.find("a")
			text = title.get_text().strip()  # Get the text of the element
			href = title.get("href")  # Get the value of the href attribute
			result_dict[text] = href  # Add key-value pair to the dictionary

	else:
		print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
	
	return result_dict

def mod_display():
	st.session_state['cur_page'] = '日報'
	# SingTao daily website
	st.session_state['dict_cat'] = web_scrape_cat(url = "https://std.stheadline.com/daily/%E6%97%A5%E5%A0%B1")

	with stylable_container(
		key='return_home_button',
		css_styles="""
			button {
				background-color: orange;
				color: white;
				border-radius: 10px;
				width: 1200px;
				height: 100px;

				/* Center the button horizontally */
				display: block;
				margin: 0 auto; 
			}
			"""
	):
		if st.button(r'$\Huge\text{主頁}$'):
			st.switch_page("home.py")

	l_col, r_col = st.columns(2)
	with l_col:
		with stylable_container(
			key='news_hk_button',
			css_styles="""
				button {
					background-color: #FFA07A;
					color: black;
					border-radius: 10px;
					width: 500px;
					height: 200px;

					/* Center the button horizontally */
					display: block;
					margin: 0 auto; 
				}
				"""
		):
			if st.button(r'$\Huge\text{港聞}$'):
				st.session_state['cur_page'] = '港聞'
				st.switch_page("pages/news_detail.py")

		with stylable_container(
			key='news_int_button',
			css_styles="""
				button {
					background-color: yellow;
					color: black;
					border-radius: 10px;
					width: 500px;
					height: 200px;

					/* Center the button horizontally */
					display: block;
					margin: 0 auto; 
				}
				"""
		):
			if st.button(r'$\Huge\text{國際}$'):
				st.session_state['cur_page'] = '國際'
				st.switch_page("pages/news_detail.py")
		with stylable_container(
			key='news_sport_button',
			css_styles="""
				button {
					background-color: #90EE90;
					color: black;
					border-radius: 10px;
					width: 500px;
					height: 200px;

					/* Center the button horizontally */
					display: block;
					margin: 0 auto; 
				}
				"""
		):
			if st.button(r'$\Huge\text{體育}$'):
				st.session_state['cur_page'] = '體育'
				st.switch_page("pages/news_detail.py")

	with r_col:
		with stylable_container(
			key='news_fin_button',
			css_styles="""
				button {
					background-color: #FFEBCD;
					color: black;
					border-radius: 10px;
					width: 500px;
					height: 200px;

					/* Center the button horizontally */
					display: block;
					margin: 0 auto; 
				}
				"""
		):
			if st.button(r'$\Huge\text{娛樂}$'):
				st.session_state['cur_page'] = '娛樂'
				st.switch_page("pages/news_detail.py")

		with stylable_container(
			key='news_editorial_button',
			css_styles="""
				button {
					background-color: #B0E0E6;
					color: black;
					border-radius: 10px;
					width: 500px;
					height: 200px;

					/* Center the button horizontally */
					display: block;
					margin: 0 auto; 
				}
				"""
		):
			if st.button(r'$\Huge\text{社論}$'):
				st.session_state['cur_page'] = '社論'
				st.switch_page("pages/news_detail.py")
		with stylable_container(
			key='news_finance_button',
			css_styles="""
				button {
					background-color: #EEE8AA;
					color: black;
					border-radius: 10px;
					width: 500px;
					height: 200px;

					/* Center the button horizontally */
					display: block;
					margin: 0 auto; 
				}
				"""
		):
			if st.button(r'$\Huge\text{財經}$'):
				st.session_state['cur_page'] = '財經'
				st.switch_page("pages/news_detail.py")

def Main():
	# Page config.
	carryai_icon = Image.open('./asset/carryai_favicon.ico')
	st.set_page_config(layout = 'wide', page_title = 'LCKCL News app', page_icon = carryai_icon)
	
	mod_display()

if __name__ == '__main__':
	Main()