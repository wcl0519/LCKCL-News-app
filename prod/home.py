import streamlit as st
from PIL import Image
from streamlit_extras.stylable_container import stylable_container

def show_carryyai_logo(use_column_width = False, width = 200, st_asset = st.sidebar):
	logo_path = './asset/carryai-simple-dark.png'
	st_asset.image(logo_path, use_column_width = use_column_width, channels = 'BGR', output_format = 'PNG', width = width)
	
def mod_display():
	st.session_state['cur_page'] = '主頁'
	with stylable_container(
		key='news_button',
		css_styles="""
			button {
				background-color: #025940;
				color: white;
				border-radius: 50px;
				width: 1200px;
				height: 400px;

				/* Center the button horizontally */
				display: block;
				margin: 0 auto; 
			}
			"""
	):
		if st.button(r'$\Huge\text{日報}$'):
			st.switch_page("pages/news_home.py")
		
	with stylable_container(
		key='ocr_button',
		css_styles="""
			button {
				background-color: green;
				color: white;
				border-radius: 50px;
				width: 1200px;
				height: 400px;

				/* Center the button horizontally */
				display: block;
				margin: 0 auto; 
			}
			"""
	):
		if st.button(r'$\Huge\text{掃描}$'):
			st.switch_page("pages/ocr_home.py")

def Main():
	# Page config.
	carryai_icon = Image.open('./asset/carryai_favicon.ico')
	st.set_page_config(layout = 'wide', page_title = 'LCKCL News app', page_icon = carryai_icon)
	# show_carryyai_logo()
	# with st.sidebar:
	# 	st.header('LCKCL News app')
	# 	with st.expander('Info', expanded=True):
	# 		st.info('''
	# 			This tool is a demo for LCKCL 2024 News/OCR project (星島[https://std.stheadline.com/daily/%E6%97%A5%E5%A0%B1])
	# 		''')

	mod_display()

if __name__ == '__main__':
	Main()