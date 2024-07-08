import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import easyocr
from PIL import Image
import pyttsx3
import time
import cv2
from io import BytesIO
import numpy as np
import streamlit.components.v1 as components

st.session_state['cur_page'] = '掃描'

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

# Create a title and a file uploader
st.title("OCR Webpage")

# Check if the button has been clicked
# Create a video capture object
video_capture = st.camera_input("掃描")

if video_capture is not None:
    bytes_data = video_capture.getvalue()
    image = Image.open(BytesIO(bytes_data))
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    

        
    # Perform OCR on the captured frame
    reader = easyocr.Reader(['ch_sim'])
    result = reader.readtext(image_cv)
    
    



    # Initialize sound output driver
    # engine = pyttsx3.init(driverName="nsss")  # mac
    # engine = pyttsx3.init(driverName="sapi5")  # winows
    # engine = pyttsx3.init(driverName="espeak")  # linux version
    # voices = engine.getProperty('voices')

    # for voice in voices:
    #     if 'ZH-HK' in voice.id.split('\\')[-1]:
    #         engine.setProperty('voice', voice.id)
    #         break

    # engine.setProperty('rate',150 )
    # engine.setProperty('volume',1)
    
    # Display the extracted text
    for r in result:
        st.write(r[1])
        # engine.say(r[1])
            # st.page_link(page= title_url, label= title)
            # st.markdown(title_url)
        components.html(
			f"""
			<script>
			var msg = new SpeechSynthesisUtterance("{r[1]}");
			msg.rate = 0.75;
			msg.volume = 1;
			window.speechSynthesis.speak(msg);
			</script>
			"""
			, height=0, width=0
		)
        # engine.runAndWait()
        time.sleep(2)