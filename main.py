
from utils import get_detection_folder, check_folders
import redirect as rd

from pathlib import Path
import streamlit as st
from PIL import Image
import subprocess
import os


check_folders()

if __name__ == '__main__':
    
    st.title('Приложение по детекции объектов для Алёны :)')

    source = ("Картинка", "Видео")
    source_index = st.sidebar.selectbox("Выбери для загрузки", range(
        len(source)), format_func=lambda x: source[x])
    
    
    
    if source_index == 0:
        uploaded_file = st.sidebar.file_uploader(
            "Загрузить файл", type=['png', 'jpeg', 'jpg'])
        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text='Загрузка...'):
                st.sidebar.image(uploaded_file)
                picture = Image.open(uploaded_file)
                picture = picture.save(f'data/images/{uploaded_file.name}')
                source = f'data/images/{uploaded_file.name}'
        else:
            is_valid = False
    else:
        uploaded_file = st.sidebar.file_uploader("Загрузка видео", type=['mp4'])
        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text='Загрузка...'):
                st.sidebar.video(uploaded_file)
                with open(os.path.join("data", "videos", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                source = f'data/videos/{uploaded_file.name}'
        else:
            is_valid = False

    if is_valid:
        print('valid')
        if st.button('Нажми для детекции объектов'):
            with rd.stderr(format='markdown', to=st.sidebar), st.spinner('Немножко подожди...'):
                print(subprocess.run(['yolo', 'task=detect', 'mode=predict', 'model=yolov8n.pt', 'conf=0.25', 'source={}'.format(source)],capture_output=True, universal_newlines=True).stderr)

                    
            if source_index == 0:
                with st.spinner(text='Подготовка картинки'):
                    for img in os.listdir(get_detection_folder()):
                        st.image(str(Path(f'{get_detection_folder()}') / img))

                    st.balloons()
            else:
                with st.spinner(text='Подготовка видео'):
                    for vid in os.listdir(get_detection_folder()):
                        st.video(str(Path(f'{get_detection_folder()}') / vid))

                    st.balloons()
