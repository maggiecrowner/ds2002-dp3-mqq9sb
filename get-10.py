import boto3
from botocore.exceptions import ClientError
import requests
import json

url = "https://sqs.us-east-1.amazonaws.com/440848399208/mqq9sb"
sqs = boto3.client('sqs')

messages = []

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

def get_message():
    for i in range(10):
        try:
        # Receive message from SQS queue. Each message has two MessageAttributes: order and word
        # You want to extract these two attributes to reassemble the message
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ]
            )
        # Check if there is a message in the queue or not
            if "Messages" in response:
            # extract the two message attributes you want to use as variables
            # extract the handle for deletion later
                order = response['Messages'][0]['MessageAttributes']['order']['StringValue']
                word = response['Messages'][0]['MessageAttributes']['word']['StringValue']
                handle = response['Messages'][0]['ReceiptHandle']
            # store messages   
                phrase_dict = {}
                phrase_dict["order"] = order
                phrase_dict["word"] = word
                messages.append(phrase_dict)

        # If there is no message in the queue, print a message and exit    
            else:
                print("No message in the queue")
                continue
            
    # Handle any errors that may occur connecting to SQS
        except ClientError as e:
            print(e.response['Error']['Message'])
        finally:
            delete_message(handle)


# Trigger the function
if __name__ == "__main__":
    get_message()

reassembled = sorted(messages, key=lambda x: x['order'])
words = [item['word'] for item in reassembled]
sentence = ' '.join(words)
print(sentence)

