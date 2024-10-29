from openai import OpenAI
import streamlit as st
import config
import helper_func

st.title("Hello World, ChatGPT")
client = OpenAI(api_key=config.OPEN_API_KEY)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = config.MODEL

if "messages" not in st.session_state:
    st.session_state.messages = []
if "figures" not in st.session_state:
    st.session_state.figures = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["message"])
        if "figure" in message and message["role"] == "assistant":
            st.altair_chart(message["figure"], use_container_width=True)

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "message": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["message"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        figure = helper_func.generate_figure()
        st.altair_chart(figure, use_container_width=True)
    st.session_state.messages.append({"role": "assistant", "message": response, "figure": figure})

#combined_chart = data_layer + annotation_layer
#st.altair_chart(combined_chart, use_container_width=True)