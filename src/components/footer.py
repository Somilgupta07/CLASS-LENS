import streamlit as st


def footer_home():
    logo_url = "https://i.ibb.co/0p9yD7dQ/Gemini-Generated-Image-tsm2a7tsm2a7tsm2-1.png"
    
    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center;align-items:center">
        <p style="font-weight:bold; color:white;"> Created with ❤️ by </p>  
        <img src='{logo_url}' style='max-height:50px' />
        </div>
                
                """, unsafe_allow_html=True)


def footer_dashboard():
    logo_url = "https://i.ibb.co/0p9yD7dQ/Gemini-Generated-Image-tsm2a7tsm2a7tsm2-1.png"
    
    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center;align-items:center">
        <p style="font-weight:bold; color:black;"> Created with ❤️ by </p>  
        <img src='{logo_url}' style='max-height:50px' />
        </div>
                
                """, unsafe_allow_html=True)