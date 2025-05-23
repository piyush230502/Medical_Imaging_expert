import os
from PIL import Image as PILImage
from agno.agent import Agent
from agno.models.google.gemini import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.media import Image as AgnoImage
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from backend.prompt import MEDICAL_ANALYSIS_QUERY
import uuid # For unique temporary filenames
import logging




def get_medical_agent():
    api_key = session.get("GOOGLE_API_KEY")
    logging.info("Getting medical agent")
    if api_key:
        try:
            return Agent(
                model=Gemini(
                    # model_name="gemini-1.5-flash-latest", # Or your preferred model
                    id="gemini-1.5-flash", # gemini-pro-vision is often used for image analysis
                    api_key=api_key
                ),
                tools=[DuckDuckGoTools()],
                markdown=True
            )
            logging.info("Medical agent initialized")
        except Exception as e:
            print(f"Error initializing agent: {e}") # Log error
            return None
    return None