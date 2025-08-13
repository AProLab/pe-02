import streamlit as st
from openai import OpenAI


class StyleTextGenerator:
    """프롬프트 스타일에 따라 텍스트를 생성하는 클래스"""
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def generate_text(self, prompt: str) -> str:
        """주어진 프롬프트로 텍스트 생성"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"오류 발생: {str(e)}"


class StyleTextApp:
    """Streamlit 스타일 변환 UI 클래스"""
    def __init__(self):
        self.api_key = None
        self.base_topic = "고양이에 대해 설명해줘."
        self.style_options = {
            "기본": self.base_topic,
            "초등학생 스타일": "초등학생이 이해할 수 있도록 고양이에 대해 설명해줘.",
            "시 스타일": "고양이에 대해 시형식으로 설명해줘.",
            "전문 수의사 스타일": "전문적인 수의사처럼 고양이를 설명해줘."
        }

    def run(self):
        """Streamlit 앱 실행"""
        st.header("프롬프트 엔지니어링 - 스타일 바꾸기")
        self.api_key = st.text_input("OPENAI API KEY를 입력하세요.", type="password")

        st.write("기본 주제:")
        st.info(self.base_topic)

        style = st.selectbox("스타일을 선택하세요.", options=list(self.style_options.keys()))

        if st.button("결과 보기"):
            if not self.api_key:
                st.warning("API 키를 입력해주세요.")
                return

            generator = StyleTextGenerator(self.api_key)
            prompt = self.style_options[style]

            with st.spinner("답변 생성 중..."):
                result = generator.generate_text(prompt)
                st.write(result)


if __name__ == "__main__":
    app = StyleTextApp()
    app.run()