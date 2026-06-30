# import streamlit as st
# from few_shot import FewShotPosts
# from post_generator import generate_post
#
#
# # Options for length and language
# length_options = ["Short", "Medium", "Long"]
# language_options = ["English", "Hinglish"]
#
#
# # Main app layout
# def main():
#     st.title("LinkedIn Post Generator")
#
#     # Create three columns for the dropdowns
#     col1, col2, col3 = st.columns(3)
#
#     fs = FewShotPosts()
#     # tags = fs.get_tags()
#     with col1:
#         # Dropdown for Topic (Tags)
#         selected_tag = st.selectbox("Title", options=fs.get_tags())
#
#     with col2:
#         # Dropdown for Length
#         selected_length = st.selectbox("Length", options=length_options)
#
#     with col3:
#         # Dropdown for Language
#         selected_language = st.selectbox("Language", options=language_options)
#
#
#
#     # Generate Button
#     if st.button("Generate"):
#         post = generate_post(selected_length, selected_language, selected_tag)
#         st.write(post)
#
#
# # Run the app
# if __name__ == "__main__":
#     main()


import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]


def main():
    st.set_page_config(page_title="LinkedIn Post Generator", layout="wide")
    st.title("LinkedIn Post Generator")

    # --- INJECTING CUSTOM EYE-SOOTHING BUTTON STYLES ---
    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #1E293B !important;
            color: #FFFFFF !important;
            border: 1px solid #475569 !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:first-child:hover {
            background-color: #334155 !important;
            color: #38BDF8 !important;
            border-color: #38BDF8 !important;
            box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    fs = FewShotPosts()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        influencer_list = fs.get_influencers()
        selected_influencer = st.selectbox("Select Influencer", options=influencer_list)

    with col2:
        selected_tag = st.selectbox("Topic", options=sorted(list(fs.get_tags())))

    with col3:
        selected_length = st.selectbox("Length", options=length_options)

    with col4:
        selected_language = st.selectbox("Language", options=language_options)

    if st.button("Generate Post", use_container_width=True):
        with st.spinner(f"Drafting post using {selected_influencer}'s style rules..."):
            post = generate_post(selected_length, selected_language, selected_tag, selected_influencer)
            st.markdown("###  Generated Copy:")
            st.text_area(label="Result Output", value=post, height=300)


if __name__ == "__main__":
    main()