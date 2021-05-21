from PIL import Image, ImageDraw

def weekly_moods(moods):
    back = Image.open("resource/grey_back.png")
    print('ran')
    back.save('process/weekly_mood.png')


weekly_moods('yeet')