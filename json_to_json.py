import json
import glob, os
from tqdm import tqdm


input_dir = "input/"
output_dir = "output/"

#file = open(f"{input_dir}project-2-at-2022-12-02-11-13-6969e270.json")


def load_json():
    file = open(f"{input_dir}json/project-6-at-2023-01-18-14-04-a31f1417.json")
    data = json.load(file)
    return data

#useless
def load_lines():
    data = load_json()
    for line in data:
        return line

def write_json(input):
    name = str(input["id"])
    with open(f"{output_dir}/{name}.json", "w") as out:
        json.dump(input, out)

classes = "test"

def data_cleaning():
    #load names of images
    #search for matching annotations
    output_json = []
    useless_images = []
    for name_image in tqdm(os.listdir("input/all_pictures/")):
        json_data = load_json()
        for line in json_data:
            annotation = line["annotations"][0]
            if name_image in line["file_upload"]:
                #check if image can be skipped
                if annotation["result"][0]["value"]["rectanglelabels"][0] == "useless":
                    useless_images.append(name_image)
                    continue
                keypoint_list = []
                counter = 0
                for i in annotation["result"]:
                    classes = i["value"]["rectanglelabels"][0]
                    x = i["value"]["x"]
                    y = i["value"]["y"]
                    width = i["value"]["width"]
                    height = i["value"]["height"]
                    box = {
                        "x": x,
                        "y": y,
                        "width": width,
                        "height": height,
                        "class": classes
                    }
                    keypoint_list.append(box)

                #sum index 3,4
                right = keypoint_list[3]
                x_right = right["x"]
                y_right = right["y"]
                left = keypoint_list[4]
                x_left = left["x"]
                y_left = left["y"]

                x_sum = (x_right+x_left) / 2
                y_sum = (y_right + y_left) / 2

                right["x"] = x_sum
                right["y"] = y_sum

                keypoint_list.pop(4)

                #make dicts
                keypoints_cone = {
                    "name": name_image,
                    "keypoints": keypoint_list,
                }
                output_json.append(keypoints_cone)
    with open(f"{output_dir}/keypoints.json", "w") as out:
        json.dump(output_json, out)






if __name__ == '__main__':
    data = load_json()
    data_cleaning()