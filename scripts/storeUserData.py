import json
import boto3

sql_query = """
        INSERT INTO spoticry
        (
            email,
            username,
            password,
            dob_day,
            dob_month,
            dob_year,
            proxy_ip,
            proxy_country,
            status
        )
        VALUES
        (
            sc_email,
            sc_username,
            sc_password,
            sc_dob_day,
            sc_dob_month,
            sc_dob_year,
            sc_proxy_ip,
            sc_proxy_country,
            sc_status
        )
      """

def lambda_handler(event, context):
    client = boto3.client('rds-data')

    sc_email = {'name': 'email', 'value':{ 'stringValue': event['email'] }}
    sc_username = {'name': 'username', 'value':{ 'stringValue': event['username'] }}
    sc_password = {'name': 'password', 'value':{ 'stringValue': event['password'] }}
    sc_dob_day = {'name': 'dob_day', 'value':{ 'longValue': event['dob']['day'] }}
    sc_dob_month = {'name': 'dob_month', 'value':{ 'longValue': event['dob']['month'] }}
    sc_dob_year = {'name': 'dob_year', 'value':{ 'longValue': event['dob']['year'] }}
    sc_proxy_ip = {'name': 'proxy_ip', 'value':{ 'stringValue': event['proxy']['ip'] }}
    sc_proxy_country = {'name': 'proxy_country', 'value':{ 'stringValue': event['proxy']['country'] }}
    sc_status = {'name': 'status', 'value':{ 'longValue': event['status'] }}

    parameter_set = [sc_email, sc_username, sc_password, sc_dob_day, sc_dob_month, sc_dob_year, sc_proxy_ip, sc_proxy_country, sc_status]
    db_arn = 'arn:aws:rds:us-west-2:666563685639:cluster:spoticry'
    db_secret_arn = ''

    response = client.execute_statement (
        resourceArn = db_arn,
        secretArn = db_secret_arn,
        database = 'spoticry',
        sql = sql_query,
        parameters = parameter_set
    )

    return 0