import cv2
import pandas as pd
from timeit import default_timer as timer
import csv

file_name = "data/colorpic.jpg"  # Change this to search different images
save_dict = True  # Change this to save the output as a csv


def get_color_name(red, green, blue):
    minimum = 765
    for i in range(len(csv)):
        distance = abs(red - int(csv[i][2])) + abs(green - int(csv[i][3])) + abs(blue - int(csv[i][4]))
        if distance <= minimum:
            minimum = distance
            color_name = csv[i][0]
    return color_name


def load_data():
    # Loads image into numpy array then converts it to Python list
    # For some reason converting it to a list makes it run much faster
    print("Loading image into list")
    img = cv2.imread(file_name).tolist()
    # Creates pandas data frame from colors.csv file and removes unused columns
    color_data = pd.read_csv('data/colors.csv', names=["color", "color_name", "hex", "R", "G", "B"], header=None)
    color_data = color_data.drop(['color'], axis=1)
    color_data = color_data.to_numpy()
    return img, color_data


def get_rgb_count():
    print("Making dictionary of r,g,b counts")
    start = timer()
    output = {}
    for row in image:
        for pixel in row:
            b, g, r = pixel
            output[(r, g, b)] = output.get((r, g, b), 0) + 1
    end = timer()
    # print(end-start, "Time to complete get_rgb_count")
    return output


def get_color_name_count():
    print("Making dictionary of color names")
    start = timer()
    color_name_count = {}
    most_common_color = "Something went wrong."
    for key in sorted(rgb_count, key=rgb_count.get, reverse=True):
        r, g, b = key
        color_name = get_color_name(r, g, b)
        color_name_count[color_name] = color_name_count.get(color_name, 0) + rgb_count.get((r, g, b))
        if color_name_count[color_name] >= (len(image) * len(image[0]) / 2):
            most_common_color = color_name
            break
    end = timer()
    # print(end-start, "Time to complete get_color_name_count")
    return color_name_count


if __name__ == "__main__":
    try:
        df = pd.read_pickle(file_name[0:-4] + ".pkl")
    except FileNotFoundError:
        image, csv = load_data()
        rgb_count = get_rgb_count()
        color_name_count = get_color_name_count()
        print("Creating dictionary of color name -> count")
        answer = []
        for key in sorted(color_name_count, key=color_name_count.get, reverse=False):
            answer.append([key, color_name_count[key]])
        data_out = []
        for answer_row in answer:
            for csv_row in csv:
                if csv_row[0] == answer_row[0]:
                    data_out.append([answer_row[1], csv_row[2], csv_row[3], csv_row[4], csv_row[1]])
        # print(data_out)
        df = pd.DataFrame([row[0:5] for row in data_out], index=[row[0] for row in answer], columns=["Count", "R", "G", "B", "Hex"])
    if save_dict:
        pd.to_pickle(df, file_name[0:-4] + ".pkl")
    print(df)
    print("Most common color:", df.index[-1])
    temp = df.index.tolist()[-5:]
    temp.reverse()
    print("The top 5 are:", temp)
