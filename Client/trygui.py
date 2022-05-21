import pygame

from Server import email_sender, audio_actions, translator
from logger_config import config_client_logger

config_client_logger()
pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
alpha = (0, 88, 255)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('GUI Speech Recognition')

gameDisplay.fill(white)
carImg = pygame.image.load('hi.jpg')
gameDisplay.blit(carImg, (0, 0))


def close():
    pygame.quit()
    quit()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 30)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()


def text_objects(text, font):
    textSurface = font.render(text, True, alpha)
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def s2t():
    txt = "send hi to kate in arabic file hi"
    # if not txt:
    gameDisplay.blit(carImg, (0, 0))
    secs = int(input('Enter time duration in seconds: '))
    Recorder.record(secs)
    path = r'../out.wav'
    print('Say Something!')
    # txt = Recorder.voice_to_text(path).lower()
    print('Done!')
    print(txt)
    message_display(txt)
    try:
        send_email_by_name(txt)
    except:
        print("exception while trying to send email")


def send_email_by_name(txt):
    if txt:
        pharses = txt.split()
        if len(pharses) <= 7:
            print('Bad Format')
            return
        _1, *msg, _2, name, _3, language, _4, file_name = pharses
        print(msg)
        msg = ' '.join(msg)
        if (_1, _2, _3, _4) != ('send', 'to', 'in', 'file'):
            print('Bad Format')
            return
        file_name += '.jpg'
        # print(file_name)
        # send_email = EmailUtils('Message from VoiceTranslator', name, msg, file_name, Email_Sender.contacts)
        # send_email.send_email_with_attachment()
        translated = Translator.translate_text(msg, language)
        Email_Sender.send_email(name, msg, language, translated)


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Speak!", 150, 450, 100, 50, green, bright_green, s2t)
        button("Quit", 550, 450, 100, 50, red, bright_red, close)
        pygame.display.update()


if __name__ == '__main__':
    main()
