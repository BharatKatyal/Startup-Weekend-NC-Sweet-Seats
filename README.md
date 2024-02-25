# Startup-Weekend-NC-Sweet-Seats


S3 Landing Page to do
Figure out how to do Bucket Policy within SAM to Automate complete process





UI Changes - Bucket policy Added


Bucket Policy
```
{
    "Version": "2008-10-17",
    "Id": "PolicyForPublicWebsiteContent",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::recapiq.com/*"
        }
    ]
}
```


IAM User Policy for Github Action 
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::recapiq.com",
        "arn:aws:s3:::recapiq.com/*"
      ]
    }
  ]
}
```