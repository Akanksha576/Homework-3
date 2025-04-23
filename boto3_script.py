import boto3

# -------- Step 1: List files in an S3 bucket --------
s3 = boto3.client('s3')
bucket_name = 'bucketri79216'  # Replace with your actual bucket name

print(f"Files in bucket '{bucket_name}':")
response = s3.list_objects_v2(Bucket=bucket_name)

if 'Contents' in response:
    for obj in response['Contents']:
        print(f" - {obj['Key']} ({obj['Size']} bytes)")
else:
    print("No files found.")

# -------- Step 2: Create DynamoDB table --------
dynamodb = boto3.client('dynamodb')

table_name = 'MyBoto3Table'

# Check if table already exists
existing_tables = dynamodb.list_tables()['TableNames']
if table_name not in existing_tables:
    print(f"\nCreating table '{table_name}'...")
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'ID', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'ID', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print("Table creation requested. Please wait until it is ACTIVE.")
else:
    print(f"\nTable '{table_name}' already exists.")

# -------- Step 3: Insert an item into DynamoDB --------
print(f"\nInserting item into '{table_name}'...")
dynamodb.put_item(
    TableName=table_name,
    Item={
        'ID': {'S': '1'},
        'Name': {'S': 'Akanksha Patel'},
        'Role': {'S': 'Data Analyst'}
    }
)
print("Item inserted successfully.")

