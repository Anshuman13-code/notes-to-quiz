import streamlit as st
import re
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Explicitly load api.env
load_dotenv("api.env")

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))



# --- FUNCTION TO GENERATE QUIZ USING GEMINI API ---
def generate_quiz(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-1.5-pro"
    response = model.generate_content(prompt)

    # Safely extract text from response
    if hasattr(response, "text") and response.text:
        return response.text
    elif hasattr(response, "candidates") and response.candidates:
        return response.candidates[0].content.parts[0].text
    else:
        return ""

# --- REMOVE DUPLICATE QUESTIONS ---
def remove_duplicate_questions(question_blocks):
    seen_questions = set()
    unique_blocks = []
    for block in question_blocks:
        question_line = block.split('\n')[0]
        if question_line not in seen_questions:
            seen_questions.add(question_line)
            unique_blocks.append(block)
    return unique_blocks

# --- STREAMLIT UI CONFIG ---
st.set_page_config(page_title="Notes → Quiz", page_icon="📚", layout="centered")
st.title("📚 Notes → Quiz Generator")
st.markdown("Paste your summarized lecture notes below to generate 5 multiple-choice questions with answers.")

lecture_notes = st.text_area(
    "Paste your notes here (keep it concise for token efficiency):",
    height=250,
    placeholder="For example: Photosynthesis is a process used by plants, algae, and certain bacteria..."
)

if st.button("✨ Generate Quiz"):
    if not lecture_notes.strip():
        st.warning("📋 Please paste some notes first!")
    else:
        with st.spinner("🧠 Generating your quiz..."):
            # Optimized prompt to force answers immediately after each question
            prompt = (
                "Generate 5 unique multiple-choice questions from the text below. "
                "Each question must have 4 options (A-D) with only one correct answer. "
                "Provide the correct answer immediately after each question, starting with 'Answer:'. "
                "Format questions as Q1:, Q2:, etc., with each option on its own line.\n\n"
                f"Text:\n{lecture_notes}"
            )

            try:
                generated_text = generate_quiz(prompt)

                # Split questions by Q1:, Q2:, etc.
                quiz_blocks = re.split(r'(?=Q\s*\d+[:\-])', generated_text)
                quiz_blocks = [block.strip() for block in quiz_blocks if block.strip()]

                # Remove duplicates and keep only 5 questions
                unique_quiz_blocks = remove_duplicate_questions(quiz_blocks)
                final_quiz_blocks = unique_quiz_blocks[:5]

                if not final_quiz_blocks or len(final_quiz_blocks) < 5:
                    st.error("The model did not generate 5 unique questions. Try providing more detailed notes.")
                    with st.expander("Raw model output"):
                        st.code(generated_text)
                else:
                    st.subheader("📝 Here's Your Quiz!")
                    for block in final_quiz_blocks:
                        with st.container():
                            lines = block.strip().split('\n')
                            question_part = []
                            answer_part_styled = ""
                            for line in lines:
                                if line.lower().strip().startswith("answer:"):
                                    # Answer displayed in green bold
                                    answer_part_styled = f"<p style='color: #28a745; font-weight: bold;'>{line.strip()}</p>"
                                else:
                                    # Bold the option letters (A-D) and separate each option with a line break
                                    match = re.match(r'^([A-D]):\s*(.*)', line.strip())
                                    if match:
                                        option_letter = match.group(1)
                                        option_text = match.group(2)
                                        question_part.append(f"<b>{option_letter}:</b> {option_text}")
                                    else:
                                        question_part.append(line.strip())
                            question_text = "<br>".join(question_part)
                            st.markdown(question_text, unsafe_allow_html=True)
                            if answer_part_styled:
                                st.markdown(answer_part_styled, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred during quiz generation: {e}")
