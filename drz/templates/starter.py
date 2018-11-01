import boto3

print('Loading function $1')


def lambda_handler(event, context):
    print("Hello, world!")

    return "Success!"
