
from .utils import clean_text, load_pattern
import requests
import json
import os

class IntentRecognition:
    def __init__(self, root: str, ai_service=None):
        """
        args:
            - ai_service: URL of API to call the AI model to predict the intent
        return:
            intent type, probability, cleaned message
        """
        
        self.dict_question_signal = load_pattern(os.path.join(root, "question_signal.json"))
        self.dict_random_intent = load_pattern(os.path.join(root, "random_intent.json"))
        self.dict_rule_based_intent = load_pattern(os.path.join(root, "business_intent.json"))
        self.configs = load_pattern(os.path.join(root, "configs.json"))
        self.ai_service = ai_service
        self.default_intent = "not_intent"

    def _find_pattern(self, query: str, gallery: list):
        for pattern in gallery:
            if query.lower().find(pattern) != -1:
                return True
        return False
    
    def _check_is_question(self, mess: str):
        for k in list(self.dict_question_signal.keys()):
            is_question = self._find_pattern(
                query=mess,
                gallery=self.dict_question_signal[k]
            )
            if is_question:
                return is_question
            else:
                continue
        return False

    def _classify_intent(self, mess: str, dict_intent: dict):
        
        for intent in dict_intent:
            is_valid = self._find_pattern(
                query=mess,
                gallery=dict_intent[intent]
            )
            if is_valid:
                return intent, 1.0
            else:
                continue
        return self.default_intent, 1.0
    
    def ai_based_predict_intent(self, mess: str):
        
        pred = requests.post(
            self.ai_service,
            json={
                "message": mess
            }
        ).json()
        
        if pred['probability'] >= self.configs[pred['intent']]:
            return pred['intent'], pred['probability']
        else:
            return 'other', 1.0
    
    def predict(self, mess: str):
        """
        To predict the intent of input message
        args:
            - mess: the message
        return: 
            - intent, probability, mess cleaned
        """

        ## 1. Clean the input message

        cleaned_mess = clean_text(mess)

        ## 2. Check the question
        is_question = self._check_is_question(mess=cleaned_mess)
        if is_question:
            ## 2.2 Classify the business intent
            (intent, probability) = self._classify_intent(
                mess=cleaned_mess,
                dict_intent=self.dict_rule_based_intent
            )
            if intent == self.default_intent and self.ai_service:
                ## need to AI-based
                (intent, probability) = self.ai_based_predict_intent(
                    mess=cleaned_mess
                )
        else:
            ## 3. Classify the random intent
            (intent, probability) = self._classify_intent(
                mess=cleaned_mess,
                dict_intent=self.dict_random_intent
            )

        return intent, probability, cleaned_mess

if __name__ == "__main__":
    catcher = IntentRecognition()
    message = "em muốn hỏi là mình đăng kí xét tuyển chương trình việt pháp như thế nào ạ"
    result = catcher.predict(message)
    print(result)

