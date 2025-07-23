from langgraph.graph import StateGraph
from typing import TypedDict
from module import translate_subtitle, adjust_style, ensure_consistency, review_quality

# Define the state keys for the graph
class state_keys(TypedDict):
    input_text : str
    subtitle : str
    target_language : str
    program_info : str
    people_info : str
    translated : str
    styled : str
    quality_passed : bool
    feedback : str
    rewrite_attempts : int
    fullLog : str

# Define node functions for each step
def node_translate(state):
    translated = translate_subtitle(state.get("subtitle"), state.get("target_language"), state.get("feedback", "없음"))

    full_log = state.get("fullLog", "") + "2. node_translate 실행 결과 : " + translated + "\n\n"


    return {
        "translated" : translated,
        "fullLog": full_log}

def node_ensure_consistency(state):
    # glossary는 필요에 따라 추가
    subtitle = ensure_consistency(state.get("input_text"), state.get("program_info"), state.get("people_info"), state.get("feedback", "없음"))

    attempts = state.get("rewrite_attempts", 0) + 1

    full_log = state.get("fullLog", "") + str(attempts) + "번째 번역 Langaraph 실행\n"

    full_log += "1. node_ensure_consistency 실행 결과 : " + subtitle + "\n\n"


    return {
        "subtitle": subtitle,
        "rewrite_attempts": attempts,
        "fullLog": full_log
    } 

def node_adjust_style(state):
    styled = adjust_style(
        state.get("translated"),
        state.get("target_language"),
        state.get("program_info"),
        state.get("people_info"),
        state.get("feedback", "없음")
    )

    full_log = state.get("fullLog", "") + "3. node_adjust_style 실행 결과 : " + styled + "\n\n"

    return {
        "styled": styled,
        "fullLog": full_log
    }

def node_review_quality(state):
    is_passed, feedback = review_quality(state.get("input_text"), state.get("target_language"), state.get("styled"))

    full_log = state.get("fullLog", "") + "4. node_review_quality 실행 결과 : " + str(is_passed) +", " + feedback + "\n\n"

    return {
        "quality_passed": is_passed,  # Placeholder for actual quality check
        "feedback": feedback,  # Placeholder feedback
        "fullLog": full_log
    }

def end_node(state):
    return {}  # 종료 노드

# Create the graph
graph = StateGraph(state_keys)

graph.add_node("ensure_consistency", node_ensure_consistency)
graph.add_node("translate", node_translate)
graph.add_node("adjust_style", node_adjust_style)
graph.add_node("review_quality", node_review_quality)
graph.add_node("END", end_node)

graph.add_conditional_edges(
    "review_quality",
    lambda state: state.get("quality_passed") or state.get("rewrite_attempts", 0) >= 3,
    {
        True: "END",              # 품질 통과 또는 3회 초과 → 종료
        False: "ensure_consistency",    # 아니면 스타일 재조정 반복
    }
)

# Define the flow
graph.add_edge("ensure_consistency", "translate")
graph.add_edge("translate", "adjust_style")
graph.add_edge("adjust_style", "review_quality")
graph.add_edge("review_quality", "END")

# Set entry and exit points
graph.set_entry_point("ensure_consistency")

# Export the graph object for use
langgraph_flow = graph