# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 10:17:21 2023

@author: sree
"""

import json
from json import JSONEncoder

import pandas as pd
import streamlit as st
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

def app():
        
    # Helper methods
    @st.cache(allow_output_mutation=True)
    def analyzer_engine():
        """Return AnalyzerEngine."""
        return AnalyzerEngine()
    
    
    @st.cache(allow_output_mutation=True)
    def anonymizer_engine():
        ##Return AnonymizerEngine.
        return AnonymizerEngine()
    
    def get_supported_entities():
        #Return supported entities from the Analyzer Engine.
        return analyzer_engine().get_supported_entities()
    
    
    def analyze(**kwargs):
        #Analyze input using Analyzer engine and input arguments (kwargs).
        if "entities" not in kwargs or "All" in kwargs["entities"]:
            kwargs["entities"] = None
        return analyzer_engine().analyze(**kwargs)
    
    
    def anonymize(text, analyze_results):
        #Anonymize identified input using Presidio Abonymizer.
    
        res = anonymizer_engine().anonymize(text, analyze_results)
        return res.text
    
    # st.title("Redaction Application")

    st.set_page_config(page_title="Redaction Demo", layout="wide")
    
    # Side bar
    st.sidebar.markdown(
        """
    Anonymize PII entities.
    """
    )
    
    st_entities = st.sidebar.multiselect(
        label="Select Entities",
        options=get_supported_entities()
    )
    
    st_threhsold = st.sidebar.slider(
        label="Acceptance Threshold", min_value=0.0, max_value=1.0, value=0.35
    )
    
   
    st.sidebar.info(
        "Solution for PII detection and anonymization. "
        "Demo Redaction Application"
    )

    # Main panel
    analyzer_load_state = st.info("Starting Analyzer...")
    engine = analyzer_engine()
    analyzer_load_state.empty()
    
    # Create two columns for before and after
    col1, col2 = st.columns(2)
    
    
    col1.subheader("Input string:")
    st_text = col1.text_area(
        label="Enter your text",
        value="Lionel Messi is the greatest player of all time. His phone number is 9991119119. He is born is Rosario and he is 35 years old",
        height=400,
    )

    
    col2.subheader("Output:")
    
    st_analyze_results = analyze(
        text=st_text,
        entities=st_entities,
        language="en",
        score_threshold=st_threhsold
    )
    st_anonymize_results = anonymize(st_text, st_analyze_results)
    col2.text_area(label="", value=st_anonymize_results, height=400)
    
    # table result
    st.subheader("Final Analysis")
    if st_analyze_results:
        df = pd.DataFrame.from_records([r.to_dict() for r in st_analyze_results])
        df = df[["entity_type", "start", "end", "score"]].rename(
            {
                "entity_type": "Entity type",
                "start": "Start",
                "end": "End",
                "score": "Confidence",
            },
            axis=1,
        )
    
        st.dataframe(df, width=1000)
    else:
        st.text("No analysis")  

if __name__ == "__main__":
    app()
