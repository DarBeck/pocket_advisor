import json
from watson_developer_cloud import ConversationV1
import asyncio


class ChatBot:
    def __init__(self, message):

        self.message = message

    def send_message(self, first, con_id=None):
            conversation = ConversationV1(
                username='<username>',
                password='<pasword>',
                version='2017-05-26')   # Latest version of Watson Conversation

            # replace with your own workspace_id
            workspace_id = '<workspaceid>'

            if first:
                response = conversation.message(workspace_id=workspace_id, message_input={
                    'text': self.message})
            else:
                response = conversation.message(workspace_id=workspace_id, message_input={
                    'text': self.message}, context=con_id)
            output = response["output"]["text"][0]
            if output == "":
                output = response["output"]["text"][1]
            conversation_id = response["context"]
            # print(output)
            # print(type(output))
            print(json.dumps(response))

            return output, conversation_id


