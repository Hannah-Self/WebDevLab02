import streamlit as st
import data
import json
import pandas as pd

with open("data.json") as infile: 
    yas = json.load(infile)

if "eras_data" not in st.session_state: 
    st.session_state.eras_data = yas[0]

if "proj_data" not in st.session_state:
    st.session_state.proj_data = yas[2]

#3 new streamlit functions with #NEW beside them
#2 user input/interaction that affects app behavior 
#3 uses of data visualization (1 static, 2 dynamic)
#outside modules must be listed
#Streamlit Session States
#data plotted from a json
#description of app must be included in portfolio's project

st.header(":violet-background[DATA ABOUT MY PREVIOUS WORKS!]")
st.subheader(":violet[Scroll through to see more :>]")
st.caption(":red[**HEY!** There are two sections, so keep scrolling!]") #NEW

#Might want to change up below for .json info

def travels_section(hislit_data, dimension_data): 
    st.header(":violet-background[Research and Field Travels]")
    tab1, tab2, tab3 = st.tabs(["Historical & Literary Research", "Dimensional Travels/Dungeons", "Projects & Inventions"])
    with tab1: 
        st.subheader(":violet-background[Historical/Literary]")
        st.caption(":violet[How much time I've spent in field research per human era:]") #NEW

        def changeNum(select_era, number): 
            eras_data = st.session_state.eras_data.copy()
            for things in range(len(eras_data["Era"])): 
                if select_era == eras_data["Era"][things]: 
                    index = things
                    eras_data["Time Spent (Human Years)"][index] += number
                    st.session_state.eras_data = eras_data

        with st.form(key = "thisF"): 
            select_era = st.selectbox("Which era do you wish to add these years to?:", ["None", "1. BCE", "2. Medieval", "3. Renaissance", "4. Industrial Revs", "5. 1900s", "6. Modern"], key = "daEra") #NEW
            number = st.slider("Add Years:",0,50, key="daSlide") #NEW
            done = st.form_submit_button("Update!") #NEW
            if done == True:
                changeNum(select_era, number)

        st.bar_chart(data=st.session_state.eras_data, x= "Era", y= "Time Spent (Human Years)", color="#5D3FD3")

        st.subheader(":violet-background[Descriptions of my stay in each era:]")
        for era, desc in hislit_data.items(): 
            expander = st.expander(f"{era}")
            for thing in desc: 
                expander.write(thing)

    with tab2:
        st.markdown(''':rainbow[Going through dimensions is like going into a rainbow...there's a spectrum!]''') #NEW
        infile = open("data.json")
        st.subheader(":violet-background[Dimensional Travels/Dungeons]")
        st.caption(":violet[Dimensions I've traveled to & number of yields:]") #NEW
        dim_data = json.load(infile)[1]

        st.line_chart(data=dim_data, x="Dimensional Dungeon", y="Yields", color="#5D3FD3") #NEW
        st.subheader(":violet-background[Best yields and what they do:]")
        for dimen, descri in dimension_data.items(): 
            expander = st.expander(f"{dimen}")
            for thing in descri: 
                expander.write(thing)
        infile.close()

    with tab3: 
        st.subheader(":violet-background[Projects & Inventions]")
        st.write(":violet[The following data is sorted using a line chart to indicate the correlation between the variables as the dimensions they belong in decrease.]")
        st.caption(":violet[My inventions sorted by how much energy and profit they produced:]") #NEW

        def changeSec(one): 
            proj_data = st.session_state.proj_data.copy()
            for thing in range(len(proj_data["Project/Invention"])): 
                if one == proj_data["Project/Invention"][thing]: 
                    del proj_data["Project/Invention"][thing]
                    del proj_data["Profit (USD, mil)"][thing]
                    del proj_data["Energy Produced (Earths)"][thing]
                    del proj_data["Dimension"][thing]
                    break
            st.session_state.proj_data = proj_data

        with st.form(key = "thisFT"): 
            one = st.radio("Delete a project to see correlations more clearly:", ["15D Plutonian Flower","GF5 - Wave 3", "Imaginary Dice","Ludus Maffiae"]) #NEW
            doneTwo = st.form_submit_button("Update!") #NEW
            if doneTwo:
                changeSec(one)
        
        def changeLast(select_pro, increase): 
            proj_data = st.session_state.proj_data.copy()
            for item in range(len(proj_data["Project/Invention"])): 
                if select_pro == proj_data["Project/Invention"][item]: 
                    proj_data["Profit (USD, mil)"][item] += increase
                
            st.session_state.proj_data = proj_data

        with st.form(key = "thisFTrice"): 
            select_pro = st.selectbox("Which loot to adjust inflation to (Profit)?:", ["None", "15D Plutonian Flower","GF5 - Wave 3", "Imaginary Dice","Ludus Maffiae"], key = "daProj") #NEW
            increase = st.slider("Add loot:",0,50, key="daSlideTwo") #NEW
            doneThree = st.form_submit_button("Update!") #NEW
            if doneThree == True:
                changeLast(select_pro, increase)

        st.line_chart(data=st.session_state.proj_data, x= "Project/Invention", y= ["Energy Produced (Earths)", "Profit (USD, mil)", "Dimension"], color=["#5D3FD3", "#8a2be2", "#660066"]) #NEW

        infile.close()
        st.write("Judging by the data provided, it seems that there is a nice correlation between the profit and dimension, indicating that inhabitants across the galaxy tend to see value by dimension. Further research is needed to discern fixed results.")
    
    st.write("---")
travels_section(data.hislit_data,data.dimension_data)