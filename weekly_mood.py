from PIL import Image, ImageDraw


def draw_block(start, difference, moods):
    daily_moods = []
    mood_count = {}
    highest = 0

    for mood in moods:
        if mood not in daily_moods:
            daily_moods.append(mood)
            mood_count[mood] = moods.count(mood)
            if moods.count(mood) > highest:
                highest = moods.count(mood)

    daily_moods = sorted(daily_moods)

    increment = difference / len(daily_moods)
    coord_list = [[start]]

    for i in range(len(daily_moods)):
        lower_x = start + (increment * (i+1))
        print(f"{mood_count[daily_moods[i]]} {highest}")
        y_coord = (1 - (mood_count[daily_moods[i]] / highest)) * 93
        coord_list.append([lower_x, y_coord])

    return coord_list, daily_moods


def weekly_moods(moods, uuid):   #uuid is passed as a string
    colours = {'anger': 'red', 'fear': 'yellow', 'joy': 'aqua', 'sadness': 'blue', 'confident': 'orange', 'tentative': 'green', 'analytical': 'pink'}
    lower = 260
    upper = 167
    difference = 93
    blocks = [857, 722, 586, 450, 313, 176, 44]

    back = Image.open("grey_back.png")
    back_draw = ImageDraw.Draw(back)

    for i in range(len(blocks)):
        if len(moods[i]) != 0:
            coords, daily_moods = draw_block(blocks[i], difference, moods[i])

            for j in range(len(daily_moods)):
                back_draw.rectangle((coords[j][0]+1, upper + coords[j+1][1], coords[j+1][0], lower), fill=colours[daily_moods[j]])

    back.save(f"{uuid}.png")
