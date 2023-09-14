from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

from random import randint
import settings
from telegram import ReplyKeyboardMarkup, KeyboardButton


def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Ваше число {user_number}, мое число {bot_number}.Вы выйграли!"
    elif user_number == bot_number:
        message = message = f"Ваше число {user_number}, мое число {bot_number}.Ничья!"
    else:
        message = message = f"Ваше число {user_number}, мое число {bot_number}.Вы проиграли!"
    return message


def main_keyboard():
    return ReplyKeyboardMarkup(
        [
            ['Заполнить анкету'],
            [KeyboardButton('Мои координаты', request_location=True)],
            ['Покажи котика', 'Давай поиграем']
            ])


def is_cat(file_name):
    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', f'Key{settings.CLARIFI_API_KEY}'),)

    with open(file_name, 'rb') as f:
        file_data = f.read()
        image = resources_pb2.Image(base64=file_data)

    request = service_pb2.PostModelOutputsRequest(
        model_id='aaa03c23b3724a16a56b629203edc62c',
        inputs=[
            resources_pb2.Input(data=resources_pb2.Data(image=image))
        ])
    response = app.PostModelOutputs(request, metadata=metadata)
    print(response)


if __name__ == '__main__':
    print(is_cat('images/cat_3.jpg'))
