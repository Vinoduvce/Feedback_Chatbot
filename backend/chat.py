
from langchain.llms import Ollama

class Chatbot:
    def __init__(self):
        self.state = 'initial'  # Possible states: 'initial', 'awaiting_feedback', 'generating_feedback'
        self.file_path = "/Users/VI20463367/Documents/templete/data.txt"
        self.text = None

    def greet_user(self):
        return "Hi, I’ve completed analyzing your interview. Would you like to receive the feedback and sentiment analysis?"

#read .txt file
    def read_text(self):
        if not self.text:
            with open(self.file_path, 'r') as file:
                self.text = file.read()


# generate feedback based on text
    def generate_feedback(self, user_input):
        if not self.text:
            self.read_text()

        format="""Excellent! Here’s your feedback:
                Feedback:
                    Strengths:
                        👍 Technical Expertise: Your deep knowledge of Java frameworks and architecture patterns was impressive.
                        🔍 Problem-Solving Skills: Your approach to designing scalable and maintainable systems was spot-on.
                        🤝 Collaboration: You effectively communicated how you work with cross-functional teams and manage stakeholder expectations.
                    Areas for Improvement:
                        🗣️ Detail in Answers: Some responses could benefit from more specific examples of past projects or challenges.
                        📊 Metrics: Including concrete metrics or outcomes related to your architectural decisions could strengthen your points.
                    Sentiment Analysis:
                        Overall Sentiment: "what type of sentiment(positve or negative or neutral)"
                    Emotion Breakdown:
                        Confidence: High or moderate or low
                        Engagement: High or moderate or low
                        Nervousness: High or moderate or low
                    Over all short description:     """

        messages = [
            {"role": "system", "content": f"Give feedback to the candidate based on the following text:\n{self.text}, in the format of {format}"},
            {"role": "user", "content": user_input}
        ]
        print("Messages being sent to Ollama:", messages)
        try:
            prompt = "\n".join([f"{message['role']}: {message['content']}" for message in messages])
            llm = Ollama(model='llama3')
            response = llm.generate([prompt])
            
            if response.generations and response.generations[0]:
                reply = response.generations[0][0].text
            else:
                reply = "response is not generated."
            
            return reply
        except Exception as e:
            print(f"Error in chatbot function: {e}")
            return "Error in generating response"

    
    def answer_to_question(self,user_input):
        messages = [
            {"role": "system", "content": "Answer to user question"},
            {"role": "user", "content": user_input}
        ]
        print("Messages being sent to Ollama:", messages)
        try:
            prompt = "\n".join([f"{message['role']}: {message['content']}" for message in messages])
            llm = Ollama(model='llama3')
            response = llm.generate([prompt])

            if response.generations and response.generations[0]:
                reply = response.generations[0][0].text
            else:
                reply = "response is not generated."
            
            return reply
        except Exception as e:
            print(f"Error in chatbot function: {e}")
            return "Error in generating response"


# Handling chatbot
    def handle_input(self, user_input):
        user_input = user_input.strip().lower()
        print(f"Received input: {user_input} & Current state: {self.state}")

        if self.state == 'initial':
            if user_input == 'hi':
                self.state = 'generate_feedback'
                return self.greet_user()
            # else:
            #     return "Please say 'hi' to start the conversation."
            elif user_input == user_input:
                return self.answer_to_question(user_input)

        elif self.state == 'generate_feedback':
            if user_input in ['yes', 'no']:
                if user_input == 'yes':
                    self.state = 'feedback_question'
                    feedback=[self.generate_feedback(user_input),"Okay, I will send some feedback questions can you answer to that questions?"]
                    return "\n".join(feedback)
                else:
                    self.state = 'feedback_question'
                    return "Okay, I will send some feedback questions can you answer to that questions?"
            else:
                return "Please respond with 'yes' or 'no'."

        # elif self.state == 'generating_feedback':
        #     feedback = self.generate_feedback(user_input)
        #     self.state = 'initial'  # Reset state after generating feedback
        #     return feedback
        else:
            return "response is not generated."
