media_download_policy = {
    'Statement': [
        {
            'Action': ['s3:GetBucketLocation', 's3:ListBucket'],
            'Effect': 'Allow',
            'Principal': {'AWS': ['*']},
            'Resource': ['arn:aws:s3:::media'],
        },
        {
            'Action': ['s3:GetObject'],
            'Effect': 'Allow',
            'Principal': {'AWS': ['*']},
            'Resource': ['arn:aws:s3:::media/*'],
        },
    ],
    'Version': '2012-10-17',
}
