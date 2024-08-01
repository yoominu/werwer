import textwrap
import google.generativeai as genai
import streamlit as st
import toml
import pathlib

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# secrets.toml 파일에서 API 키 값 가져오기
api_key = secrets.get("api_key")

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# few-shot 프롬프트 구성 함수 수정
def try_generate_content(api_key, prompt):
    # API 키를 설정
    genai.configure(api_key=api_key)
   
    # 설정된 모델 변경
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config={
                                      "temperature": 0.9,
                                      "top_p": 1,
                                      "top_k": 1,
                                      "max_output_tokens": 2048,
                                  },
                                  safety_settings=[
                                      {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                  ])
    try:
        # 콘텐츠 생성 시도
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # 예외 발생시 None 반환
        print(f"API 호출 실패: {e}")
        return None

# Streamlit 앱 구성
st.title("물체의 운동 분석 앱 🚀")
st.write("물체의 운동을 설명하면 해당 물체에 작용하는 힘을 분석해드립니다.")

motion_description = st.text_input("물체의 운동을 설명하세요:")

if st.button("힘 분석하기"):
    if motion_description:
        prompt = f"물체의 운동을 다음과 같이 설명합니다: '{motion_description}'. 이 운동에 작용하는 힘을 분석해줘."
        content = try_generate_content(api_key, prompt)
        if content:
            st.markdown(to_markdown(content))
        else:
            st.error("정보를 가져오는 데 실패했습니다. 다시 시도해 주세요.")
    else:
        st.warning("물체의 운동을 설명하세요.")
