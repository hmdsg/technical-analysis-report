import json

def lambda_handler(event, context):
    # TODO implement
    print ("terraformer!")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambdaaa!!!')
    }
