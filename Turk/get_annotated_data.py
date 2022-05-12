import os
import pandas as pd
import json

def getfiles(dir):
    approved = os.listdir(dir)
    approve_pic = []
    for name in approved:
        if "jpg" not in name:
            continue
        if "_" not in name:
            approve_pic.append(name)
        else:
            filename = name.split('_')[-1]
            os.rename(dir + name, dir + filename)
            approve_pic.append(filename)
    print("The amount of approved pic is ", len(approve_pic))
    print("The amount of unduplicated approved pic is ", len(set(approve_pic)))
    return approve_pic

def readbox(boundingbox):
    annotation = []
    box = boundingbox.replace('[', '').replace(']', '')
    tokens = box.split('},')
    for item in tokens:
        temp = {}
        item = item.replace('{', '').replace('}', '')
        attributes = item.split(',')
        for attribute in attributes:
            tok = attribute.split(':')
            key = tok[0].replace('"', '')
            value = tok[1].replace('"', '') if key == 'label' else int(tok[1])
            temp[key] = value
        annotation.append(temp)
    return annotation

def get_annotation_dict(csvfiles):
    result_dict = {}
    for csv in csvfiles:
        df = pd.read_csv(csv)
        for index, row in df.iterrows():
            url = row["Input.image_url"]
            img_name = url.split('/')[-1] 
            if img_name not in result_dict:
                result_dict[img_name] = {}
            result_dict[img_name]["image_name"] = img_name
            result_dict[img_name]["url"] = url
            boundingbox = row["Answer.annotatedResult.boundingBoxes"]
            annotation = readbox(boundingbox)
            for item in annotation:
                if item["label"] not in result_dict[img_name]:
                    result_dict[img_name][item["label"]] = []
                result_dict[img_name][item["label"]].append({"height": item["height"], 'left': item['left'], 'top': item['top'], 'width': item['width']})
            height = row["Answer.annotatedResult.inputImageProperties.height"]
            result_dict[img_name]["height"] = height
            width = row["Answer.annotatedResult.inputImageProperties.width"]
            result_dict[img_name]["width"] = width
    return result_dict

if __name__ == "__main__":
    approve_pic = getfiles("./poster_approve_old")
    approved_csvs = ["./LW-Result-CSV/" + file for file in os.listdir("./LW-Result-CSV") if "rejection" not in file and "csv" in file]
    approved_dict = get_annotation_dict(approved_csvs)
    reference_dict = {}
    for img in approve_pic:
        if img in reference_dict:
            print("Wrong! Duplicate detected")
        else:
            reference_dict[img] = approved_dict[img]
    print("length of approved_dict is ", len(approved_dict))
    print("length of reference_dict is ", len(reference_dict))

    rej1_pic = getfiles("./poster_approve")
    rej1_approved_csvs = ["./LW-Result-CSV/LW-rejection1.csv"]
    rej1_approved_dict = get_annotation_dict(rej1_approved_csvs)
    for img in rej1_pic:
        if img in reference_dict:
            print("Wrong! Duplicate detected")
        else:
            reference_dict[img] = rej1_approved_dict[img]
    print("length of rej1_approved_dict is ", len(rej1_approved_dict))
    print("length of reference_dict is ", len(reference_dict))

    rej2_approved_csvs = ["./LW-Result-CSV/LW-rejection2.csv"]
    rej2_approved_dict = get_annotation_dict(rej2_approved_csvs)
    for img in list(rej2_approved_dict.keys()):
        if img in reference_dict:
            print("Wrong! Duplicate detected")
        else:
            reference_dict[img] = rej2_approved_dict[img]
    print("length of rej1_approved_dict is ", len(rej2_approved_dict))
    print("length of reference_dict is ", len(reference_dict))
    with open("LW-Annotated300.json", 'w') as fp:
        json.dump(reference_dict, fp)


