import os
import boto3
import re
from .helper import path_to, contents_of, get_drizzle_json


p_aws_credentials = path_to("~/.aws/credentials")


# Checks if ~/.aws/credentials exists and has the given profile.
# Otherwise, initializes it.
def config_profile(profile):
    if os.path.exists(p_aws_credentials) and "[%s]\n" % profile in contents_of(p_aws_credentials):
        return  # profile already configured

    access = input("AWS Access Key ID: ")
    secret = input("AWS Secret Access Key: ")

    os.makedirs(os.path.dirname(p_aws_credentials))
    aws_creds = open(p_aws_credentials, 'a')
    aws_creds.write("\n[%s]\naws_access_key_id = %s\naws_secret_access_key = %s" % (profile, access, secret))
    aws_creds.close()


def aws(service):
    profile = get_drizzle_json()["AWS Profile"]

    # todo escape profile name for regex
    access, secret = re.compile(r"\[%s\]\naws_access_key_id = ([^\n]*)\naws_secret_access_key = ([^\n]*)" % profile)\
        .search(contents_of(p_aws_credentials))

    return boto3.client(service,
                        aws_access_key_id=access,
                        aws_secret_access_key=secret)
