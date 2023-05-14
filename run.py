import streamlit as st

if __name__ == "__main__":
    st.header("Hi! I'm your Personal SRT Translator 😀")
    st.write("Choose any srt file for translating: ")
    with st.sidebar:
            add_lan = st.sidebar.selectbox(
            "Language example",
            (
                "Chinese",
                "Spanish",
                "Japanse",
                "Korean",
                "English",
            ), index=0)
            st.markdown('You can use the above languages or any other language for translation')
            st.text('Application by GGLS and San ☕')

    src_file = st.file_uploader("only support src file ✨")

    if src_file is None or src_file.name[-4:].lower() != '.srt':
        pass
    else:
        target_lan = st.text_input('Input the target language desired')
        if target_lan is None or len(target_lan) == 0:
            if add_lan is None or len(add_lan) == 0:
                target_lan = 'French'
            else:
                 target_lan = add_lan
            
        #TODO 读取文件内容并转换成模型接受的格式
        data = 'hehe'
        st.download_button(
            "Press to Download",
            data,
            f"{target_lan}_{src_file.name}")