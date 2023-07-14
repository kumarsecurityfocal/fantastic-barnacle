#!/usr/bin/python
import boto3
import os, sys, getopt
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# added new shared AWS account ID feb 2020 and grabbed pool ID

client = boto3.client('cognito-identity','us-east-1', verify=False)
resp =  client.get_id(AccountId='493163585588',IdentityPoolId='us-east-1:b8d77e04-009b-45b4-88e5-0cbaf27fa1d0')
#print "\nIdentity ID: %s"%(resp['IdentityId'])
#print "\nRequest ID: %s"%(resp['ResponseMetadata']['RequestId'])
resp = client.get_open_id_token(IdentityId=resp['IdentityId'])
token = resp['Token']
#print "\nToken: %s"%(token)
#print "\nIdentity ID: %s"%(resp['IdentityId'])
resp = client.get_credentials_for_identity(IdentityId=resp['IdentityId'])
secretKey = resp['Credentials']['SecretKey']
accessKey = resp['Credentials']['AccessKeyId']
sessionToken = resp['Credentials']['SessionToken']
#print "\nSecretKey: %s"%(secretKey)
#print "\nAccessKey ID: %s"%(accessKey)
#print resp
#ptint test

def main(argv):
   Bucket = ''
   try:
      opts, args = getopt.getopt(argv,"hb:",["bbucket="])
   except getopt.GetoptError:
      print ('s3upload.py -b <number>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('s3upload.py -b <number>')
         sys.exit()
      elif opt in ("-b", "--bbucket"):
         Bucket = arg
         if not os.path.exists("hello.txt"):
            print ('hello.txt not in folder')
            quit()

         
      

   try:
      # Retrieve the list of existing buckets
      # Changed bucket name to nscoa feb 2020
      s3 = boto3.client('s3', use_ssl=False, aws_access_key_id=accessKey,aws_secret_access_key=secretKey,aws_session_token=sessionToken,verify=False)
      s3 = boto3.resource('s3', use_ssl=False, aws_access_key_id=accessKey,aws_secret_access_key=secretKey,aws_session_token=sessionToken,verify=False)
      s3.meta.client.upload_file('hello.txt', 'nscoa'+Bucket, 'hello.txt')
    
      print ('File Uploaded to Bucket Student',Bucket)

   except:
         print ('Oops something went wrong',Bucket)
         raise

if __name__ == "__main__":
   main(sys.argv[1:])
