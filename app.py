import os,time,base64
import streamlit as st
from openai_template import translate,planMaker
import pandas as pd
from streamlit_chat import message
import azure.cognitiveservices.speech as speechsdk

st.set_page_config(page_title='Jarvis', page_icon="🤖",)
st.header('Hello My Master~')

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
:rocket:欢迎使用人工智能助手贾维斯！我是一个能够帮助您解决问题的 AI 助手，随时欢迎您的咨询！

:bulb:贾维斯有以下优势:

1. 可以处理多种自然语言问题。
2. 提供详细的技术实现细节.
3. 专业的 AI 领域知识和经验。
4. 完整的 API 测试和文档。

""")

# with col2:
#     # st.markdown(
#     #     """
#     #     <style>
#     #     img {
#     #         border-radius: 6%;
#     #     }
#     #     </style>
#     #     """,
#     #     unsafe_allow_html=True,
#     # )
#     #
#     # st.image(
#     #     image="/Users/jadeunicorn/Pictures/midjourney/my pic/out/赛博girl/shill_No_Prompt_8922bab7-48a1-4a14-829e-916589a14e04.png",
#     # )

#     df = pd.DataFrame({
#         '姓名': ['张三', '李四', '王五'],
#         '年龄': [22, 25, 28],
#         '性别': ['男', '男', '女']
#     })

#     # 在 Streamlit 中显示表格
#     st.write(df)

#     # 定义下载函数
#     def download_link(object_to_download, download_filename, download_link_text, icon='cloud-download-alt'):
#         if isinstance(object_to_download,pd.DataFrame):
#             object_to_download = object_to_download.to_csv(index=False)
#         # Some strings <-> bytes conversions necessary here
#         b64 = base64.b64encode(object_to_download.encode()).decode()
#         icon_html = f'<i class="fas fa-{icon}" style="padding-right: 5px;"></i>'
#         href = f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{icon_html}{download_link_text}</a>'
#         return href

#     # 添加下载按钮
#     st.markdown(download_link(df, 'data.csv', '下载 CSV 文件', 'download'), unsafe_allow_html=True)

#     # 添加 Font Awesome CSS 样式
#     st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" integrity="sha512-nWvIHYPKxstvZXctI5Sz4aHwq/U2tCVfQSQJ3cwR6y/QTSeSy2IWzsgCUpRIav4+AJ89P4KjLkarNp1gB5wUw==" crossorigin="anonymous" referrerpolicy="no-referrer" />', unsafe_allow_html=True)

st.markdown('-----')
########            sidebar         ############
temp = st.sidebar.selectbox('🦄Choose Template',('Translate','PlanMaker',"TTS"))
if temp == 'PlanMaker':
    st.title('PlanMaker')
    st.write('PlanMaker is a web application that allows you to create a plan based on a template.')
    usr_input = st.text_input(label='🔗 User Input', placeholder='Please input...', key='prompt')
    if usr_input:
        st.write('💡Plan here👇')
        resp = planMaker(usr_input)
        with st.spinner('Loading...'):
            st.code(resp, language='text')
elif temp == 'Translate':
    col1, col2 = st.columns(2)
    with col1:
        language=st.selectbox("Language Setting",('English','简体中文'))
#     with col2:
#         role=st.selectbox("Role Setting",('Jarvis','Default'))

    mod = st.sidebar.selectbox('输出样式',('chat','code-column'))
    if mod == 'chat':
        if 'generated' not in st.session_state:
            st.session_state['generated'] = []

        if 'past' not in st.session_state:
            st.session_state['past'] = []
        usr_input = st.text_input(label='🔗 User Input', placeholder='Please input...', key='prompt')
        if usr_input:
            # 在这里添加 spinner，表示正在计算
            # with st.spinner('Loading...'):
                # 模拟需要 5s 的计算时间
                # time.sleep(5)
            resp = translate(language,usr_input)
            st.session_state.past.append(usr_input)
            st.session_state.generated.append(resp)
            if st.session_state['generated']:
                for i in range(len(st.session_state['generated'])-1, -1, -1):
                    message(st.session_state["generated"][i], key=str(i))
                    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        #     st.write(f'🧑🏻‍💻: {usr_input}')
        #     with st.spinner('Loading...'):
        #         st.write('🤖: {}'.format(resp))
    elif mod == 'code-column':
        usr_input = st.text_input(label='🔗 User Input', placeholder='Please input...', key='prompt')
        st.markdown("**💡Translated👇**")
        if usr_input:
            resp = translate(language,usr_input)
            st.code(resp, language='text')
elif temp == 'TTS':
    st.title('TTS')
    tts_text = st.text_input(label='Text To Synthesize:',placeholder='Please input...', key='tts')

    speech_config = speechsdk.SpeechConfig(subscription=os.environ["SPEECH_API"], region=os.environ["SPEECH_REGION"])
    # 由于是远程服务器,无法设置默认扬声器,所以删除audio_config

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name='zh-CN-XiaochenNeural'  

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    if st.button('Submit'): 
        # Get text from the console and synthesize 
        text = tts_text 
        if text:
            speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
            if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                audio_data = speech_synthesis_result.audio_data  
                # Download the audio file         
                with open('speech.wav', 'wb') as f:
                    f.write(audio_data)

                # Display the audio file
                st.audio('speech.wav')
