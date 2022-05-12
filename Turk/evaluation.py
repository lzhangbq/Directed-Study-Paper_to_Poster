import boto3
import os
from os import listdir
import cv2
import numpy as np
import shutil



region_name = 'xxxxxxxxxxx'
aws_access_key_id = 'xxxxxxxxxxxxxxxxx'
aws_secret_access_key = 'xxxxxxxxxxxxxxxxxxxx'
# Uncomment this line to use in production
endpoint_url = 'xxxxxxxxxxxxxxxxxxxxx'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

# This will return $10,000.00 in the MTurk Developer Sandbox
print(client.get_account_balance()['AvailableBalance'])

def evaluate(poster_folder):
    filenames = os.listdir(poster_folder)
    for folder in filenames:
        if "LW" not in folder:
            continue
        print("The folder name is ", folder)
        poster_result_path = poster_folder + "/" + folder
        #poster_result_path = poster_folder + "/" + "LW0425-new6"
        while len(listdir(poster_result_path)) > 0:

            poster = listdir(poster_result_path)[0]
            #print(os.listdir(poster_result_path))
            print(poster)
            if "jpg" not in poster:
                os.remove(poster_result_path + "/" + poster)
                continue
            id_lst = poster.replace(".jpg", "").split("_")
            hit_id = id_lst[0]
            poster_id = id_lst[-1]
            print("Hit Id: ", hit_id)
            print("Poster Id: ", poster_id)

            response = client.list_assignments_for_hit(HITId=hit_id)

            assignment_id = response['Assignments'][0]['AssignmentId']
            print("Assignment Id: ", assignment_id)

            p_path = os.path.join(poster_result_path, poster)
            # cv2.namedWindow("poster to be evaluated", cv2.WINDOW_AUTOSIZE)
            im = cv2.imread(p_path)
            h, w, _ = np.shape(im)
            p_im = cv2.resize(im, ((int)(w * 1080 / h), 1080))
            cv2.imshow("poster to be selected", p_im)
            keystroke = cv2.waitKey(0)
            print("keystroke is ", keystroke)

            if keystroke == 106:
                # press keystork 'j', the file is evaluated as a good poster
                response = client.approve_assignment(
                    AssignmentId=assignment_id,
                    RequesterFeedback='',
                )

                print(response)

                try:
                    shutil.copy(p_path, os.path.join(poster_approve_path, poster_id+".jpg"))
                    os.remove(os.path.join(poster_result_path, poster))

                except:
                    print("Unable to copy file: ", poster)


            elif keystroke == 102:
                # press keystork 'f', the file is evaluated as good poster
                response = client.reject_assignment(
                    AssignmentId=assignment_id,
                    RequesterFeedback='',
                )

                print(response)
                try:
                    shutil.copy(p_path, os.path.join(poster_reject_path, poster_id+".jpg"))
                    os.remove(os.path.join(poster_result_path, poster))
                except:
                    print("Unable to copy file: ", poster)
            elif keystroke == 27:
                # exit the program
                break
            else:
                print("Wrong Input!")
if __name__ == "__main__":
    poster_folder = "./Posters_Folders"
    poster_approve_path = "./poster_approve"
    poster_reject_path = "./poster_reject"
    evaluate(poster_folder)
    print("The number of approved is ", len(os.listdir(poster_approve_path)))
    print("The number of rejected is ", len(os.listdir(poster_reject_path)))