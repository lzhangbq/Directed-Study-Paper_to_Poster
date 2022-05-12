import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import requests
from io import BytesIO
from PIL import Image
import os

def readbox(boundingbox):
    annotation = []
    box = boundingbox.replace('[', '').replace(']', '')
    tokens = box.split('},')
    for item in tokens:
        if item == '':
            continue
        temp = {}
        item = item.replace('{', '').replace('}', '')
        attributes = item.split(',')
        for attribute in attributes:
            #print(attribute)
            tok = attribute.split(':')
            #print(tok)
            key = tok[0].replace('"', '')
            value = tok[1].replace('"', '') if key == 'label' else int(tok[1])
            temp[key] = value
        annotation.append(temp)
    return annotation

def read_data(filename):
    df = pd.read_csv(filename)
    image_urls = df["Input.image_url"].tolist()
    boundingboxes = df["Answer.annotatedResult.boundingBoxes"].tolist()
    hitids = df["HITId"].tolist()
    result = []
    urls = []
    hitid_names = []
    image_names = []
    for hitid, url, str_boundingbox in zip(hitids, image_urls, boundingboxes):
        if str_boundingbox == "[]":
            continue
        boundingbox = readbox(str_boundingbox)
        hitid_names.append(hitid)
        urls.append(url)
        image_name = url.split('/')[-1]
        image_names.append(image_name)
        result.append(boundingbox)
    return hitid_names, image_names, urls, result

def saveimages(csvpath, attributes, colors, savedir):
    colordict = {k:v for k,v in zip(attributes, colors)}
    hitid_names, image_names, urls, result = read_data(csvpath)
    for hit_name, img_name, url, worker_answer in zip(hitid_names, image_names, urls, result):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        im = np.array(img, dtype=np.uint8)
        fig,ax = plt.subplots(1)
        ax.imshow(im)
        for answer in worker_answer:
            rect = patches.Rectangle((answer['left'],answer['top']),answer['width'],answer['height'],linewidth=1,edgecolor=colordict[answer["label"]],facecolor='none')
            ax.add_patch(rect)
        plt.savefig(savedir + hit_name + "_" + img_name)
        plt.close()


if __name__ == "__main__":

    filenames = os.listdir("./CSV")
    LW_attributes = ['Section-Header', 'Section-Body', 'Figure', 'Table']
    JY_attributes = ['Title', 'Author', 'Logo']
    LW_colors = ['#0000FF', '#008000', '#FF0000', '#FFFF00'] #blue, green, red, yellow
    JY_colors = ['#0000FF', '#008000', '#FF0000'] #blue, green, red
    for csvpath in filenames:
        savedir = "./Posters_Folders/" + csvpath.replace(".csv", "/")
        csvpath = "./CSV/" + csvpath
        if not os.path.isdir(savedir):
            os.mkdir(savedir)
        if "LW" in csvpath:
            saveimages(csvpath, LW_attributes, LW_colors, savedir)
        elif "JY" in csvpath:
            saveimages(csvpath, JY_attributes, JY_colors, savedir)
 