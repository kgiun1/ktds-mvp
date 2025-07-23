from langchain_core.prompts import ChatPromptTemplate
import os
from openai_llm import ask_openai
import json

def load_prompt(prompt_name: str) -> str:
    """
    Loads a prompt from src/prompts/{prompt_name}.txt.
    """
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", f"{prompt_name}.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

"""
Node for simple subtitle translation.
This function performs basic translation before style adjustment.
"""

def translate_subtitle(subtitle: str, target_language: str, feedback: str) -> str:
    """
    Translates the given subtitle into the target language.
    """

    template = ChatPromptTemplate.from_template(load_prompt("translate"))
    formatted_prompt = template.format(subtitle=subtitle, target_language=target_language, feedback=feedback)
    
    translated_text = ask_openai(formatted_prompt)
    return translated_text


"""
Node for adjusting subtitle style based on broadcast type and character information.
Examples: formal/informal tone, word choice by age/gender, etc.
"""

def adjust_style(translated_text: str, target_language: str, programInfo: str, peopleInfo: str, feedback: str) -> str:
    """
    Adjusts subtitle style using context such as broadcast type and character info.
    """
    template = ChatPromptTemplate.from_template(load_prompt("adjustStyle"))
    formatted_prompt = template.format(translated_text=translated_text, target_language=target_language, programInfo=programInfo, peopleInfo=peopleInfo, feedback=feedback)
    
    adjusted_text = ask_openai(formatted_prompt)
    return adjusted_text


"""
Node for handling consistency of proper nouns, character names, brands, and technical terms.
Ensures certain terms are not translated and maintains consistency throughout subtitles.
"""

def ensure_consistency(input_text: str, programInfo: str, peopleInfo: str, feedback: str) -> str:
    """
    Maintains consistency for proper nouns and technical terms using a glossary.
    """
    template = ChatPromptTemplate.from_template(load_prompt("ensureConsistency"))
    formatted_prompt = template.format(input_text=input_text, programInfo=programInfo, peopleInfo=peopleInfo, feedback=feedback)
    
    subtitle = ask_openai(formatted_prompt)
    return subtitle


"""
Node for reviewing subtitle quality and providing feedback if standards are not met.
Requests re-translation if necessary.
"""

def review_quality(subtitle: str, target_language : str, styled : str) -> tuple: 
    """
    Reviews subtitle quality and returns (is_passed, feedback).
    """
    template = ChatPromptTemplate.from_template(load_prompt("reviewQuality"))
    formatted_prompt = template.format(subtitle=subtitle, target_language=target_language, styled=styled)    
    response = ask_openai(formatted_prompt)

    try:
        data = json.loads(response)
        is_passed = data.get("quality_passed", False)
        feedback = data.get("feedback", "")
        return is_passed, feedback
    except json.JSONDecodeError:
        # 응답이 JSON이 아닌 경우에 대한 예외 처리
        return False, "형식이 올바르지 않은 응답입니다."