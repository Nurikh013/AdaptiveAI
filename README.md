
# AdaptiveAI

An AI-powered exam preparation assistant built with Python,
Streamlit, and Ollama.

## Overview

AdaptiveAI helps students identify their weakest programming
topics and receive personalized study recommendations.

The application analyzes quiz results, provides AI-generated
explanations for incorrect answers, and tracks learning progress.

## Features

- Interactive Python knowledge assessment
- Automatic quiz scoring
- Weakest-topic identification
- Personalized study recommendations
- AI-generated explanations of incorrect answers
- Experimental AI practice question generation
- Fallback questions when AI generation fails validation
- Local quiz history and progress visualization

## Technologies

- Python
- Streamlit - Web application interface
- Ollama - Local AI inference
- Qwen3 1.7B - Language model
- JSON - Local data storage

## Project Structure

- app.py - Streamlit application
- analysis.py - Quiz analysis and recommendations
- ai_engine.py - AI model integration
- history.py - Quiz history management
- requirements.txt - Python dependencies

## Installation

1. Clone or download this repository.
2. Install Python and Ollama.
3. Open a terminal in the project directory.

Install the required Python packages:

    python -m pip install -r requirements.txt

Download the AI model:

    ollama pull qwen3:1.7b

Start the application:

    python -m streamlit run app.py

Open http://localhost:8501 in your browser.

Ollama must be running locally for AI features to work.

## How It Works

1. Students answer Python quiz questions.
2. AdaptiveAI calculates performance by topic.
3. The application identifies topics needing improvement.
4. Students receive personalized study recommendations.
5. Qwen3 explains incorrect answers.
6. Quiz results are saved locally for progress tracking.

## Current Limitations

- AI-generated questions may contain factual errors.
- Generated practice questions are ungraded.
- The prototype focuses on Python programming.
- Quiz history is stored locally, without user accounts.
- The application requires a locally running Ollama model.

## Future Improvements

- More programming topics
- Improved AI question validation
- Individual student accounts
- More detailed learning analytics
- Public deployment with a hosted AI backend

## Project Status

Working local prototype under development.
