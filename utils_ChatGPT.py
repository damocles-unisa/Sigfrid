from tqdm import tqdm
import openai

class QuestionAnswerChatGPT(object):

    TEMP = ""

    def __init__(self, api_key):
        openai.api_key = api_key

    def get_answer_environment_elements(self, event, label):

        environmental_elements = ['temperature', 'illumination', 'humidity', 'motion', 'location', 'water', 'ventilation',
                                          'sound', 'smoke', 'gas state', 'air quality', 'security', 'energy', 'network']

        online_elements = ['storage', 'communication and messaging', 'time and date',
                                         'weather conditions', 'web content', 'planning and scheduling',
                                         'financial and shopping', 'privacy', 'entertainment']

        all_system_elements = environmental_elements + online_elements

        event_questions = []
        filter_information = ' Answer with yes or no and explain why.'

        if label == 'action':
            for element in all_system_elements:
                event_questions.append(['Does executing the action event \'' + event + '\' cause changes to the system element \'' + element + '\'?' + filter_information, element])
        elif label == 'trigger':
            for element in all_system_elements:
                event_questions.append(['Does the activation of the trigger event \'' + event + '\' rely on the system element \'' + element + '\'?' + filter_information, element])

        output = []

        for event_question in tqdm(event_questions):
            answer = self.__get_answer(event_question[0])
            if answer == 'Yes':
                output.append(event_question[1])

        return output

    def get_answer_relation(self, first_event, second_event, label):

        filter_information = ' Answer with yes or no and explain why.'
        resource_limitation = ' Please do not consider conflicts in terms of resources.'

        match label:
            case 'RULE_CHAINING':
                question = 'Can the execution of the action event \'' + first_event + '\' directly or indirectly cause the activation of the trigger event \'' + second_event + '\'?' + filter_information
            case 'ACTION_DUPLICATE':
                question = 'Do the action event \'' + first_event + '\' and the action event \'' + second_event + '\' express the same meaning?' + filter_information
            case 'ACTION_CONFLICT':
                question = 'Is there a potential conflict between the execution of the action event \'' + first_event + '\' and the execution of the action event \'' + second_event + '\'?' + filter_information + resource_limitation
            case 'TRIGGER_BLOCK':
                question = 'Can the execution of the action event \'' + first_event + '\' directly or indirectly block the activation of the trigger event \'' + second_event + '\'?' + filter_information + resource_limitation
            case 'ACTION_BLOCK':
                question = 'Can the execution of the action event \'' + first_event + '\' directly or indirectly block the execution of the action event \'' + second_event + '\'?' + filter_information + resource_limitation
            case _:
                raise ValueError('Unrecognized label')

        return self.__get_answer(question)

    def __get_answer(self, user_prompt):
        message = [
            {"role": "user", "content": user_prompt},
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message,
            temperature=self.TEMP
        )

        if 'choices' in response and len(response['choices']) > 0:
            content = response['choices'][0]['message']['content'].lower()
            if 'yes.' in content or 'yes,' in content:
                return 'Yes'
            elif 'no.' in content or 'no,' in content:
                return 'No'
        else:
            return None

