import os
import boto3
import pandas as pd
def get_pictures(access_key, access_secret, bucket_name, group_id, savepath):
    s3_client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = access_secret)
    s3_resource = boto3.resource('s3', aws_access_key_id = access_key, aws_secret_access_key = access_secret)
    my_bucket = s3_resource.Bucket(bucket_name)
    res = []
    for file in my_bucket.objects.filter(Prefix="poster_group_new/poster_job_" + str(group_id) + "/input/"):
        if ".jpg" not in file.key and ".png" not in file.key and ".jpeg" not in file.key:
            continue
        response = s3_client.put_object_acl(
            ACL="public-read", Bucket=bucket_name, Key=file.key
        )
        url = f'https://{bucket_name}.s3.amazonaws.com/{file.key}'
        res.append(url)
    #df = pd.DataFrame(res, columns=["image_url"])
    #df.to_csv(savepath, index=False)
    return res

if __name__ == "__main__":
    access_key = "xxxxxxxxxxxx"
    access_secret = "xxxxxxxxxxxxxxxxxxxxxx"
    #Brand new s3 key from Paper2Poster
    bucket_name = 'xxxxxxxxxxxxx'
    urls_list = []
    for i in range(1, 16):
        savepath = bucket_name + "-group" + str(i) + ".csv"
        res = get_pictures(access_key, access_secret, bucket_name, i, savepath)
        urls_list.extend(res)
       # print('size of urls_list is', len(urls_list))
    url_dict = {}
    for url in urls_list:
        key = url.split("/")[-1]
        url_dict[key] = url
   # print(url_dict)
    previous_path = "poster_reject"
    ans = []
    for reject_key in os.listdir(previous_path):
        if "jpg" not in reject_key:
            continue
        ans.append(url_dict[reject_key])
    df = pd.DataFrame(ans, columns=["image_url"])
    df.to_csv("rejection.csv", index=False)


    #df = pd.DataFrame(res, columns=["image_url"])
    #df.to_csv('lw-job1.csv', index=False)
