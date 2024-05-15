from openai import OpenAI

class ModelFactory:
    def __init__(self):
        pass

    def create_model(self,
                     llm_type: str,
                     api_key: str = "lm_studio",
                     base_url: str = "http://localhost:1234/v1"
                     ) -> OpenAI:
        assert llm_type in ["llama3", "openai"], "Invalid LLM type. Must be either 'llama3' or 'openai'"

        if llm_type == "llama3":
            return OpenAI(base_url=base_url,
                          api_key="lm_studio",
                          )
        elif llm_type == "openai":
            return OpenAI(api_key=api_key)
