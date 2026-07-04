import json
import ollama

from .prompts import SYSTEM_PROMPT


class MissionLLM:

    def parse(self, user_prompt):

        try:

            response = ollama.chat(
                model="llama3.2:latest",
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )

            content = response["message"]["content"]

            print("\n===== RAW LLM OUTPUT =====")
            print(content)

            return json.loads(content)

        except json.JSONDecodeError:

            print("\n[ERROR] Invalid JSON output from LLM")
            return None

        except Exception as e:

            print(f"\n[ERROR] Failed to communicate with Ollama: {e}")
            return None
