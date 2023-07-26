"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const aws_edge_resolver_1 = require("../aws/aws-edge-resolver");
const edge_target_1 = require("../aws/edge-target");
describe("candidate target edges are well scraped from any thing", () => {
    it(`sample no.1`, () => {
        const haystack = {
            "dimensions": [
                {
                    "name": "QueueName",
                    "value": {
                        "Fn::GetAtt": [
                            "mayQueue111",
                            "QueueName"
                        ]
                    }
                }
            ]
        };
        const targets = new aws_edge_resolver_1.AwsEdgeResolver().scrapePossibleEdgeTargets(haystack);
        const expectedTargetValues = [
            new edge_target_1.EdgeTargetSimpleString("mayQueue111"),
            new edge_target_1.EdgeTargetSimpleString("QueueName")
        ];
        expectTargetValuesToBeInSet(targets, expectedTargetValues);
        expect(targets.length).toEqual(2);
    });
    it(`sample no.2`, () => {
        const haystack = {
            "policyDocument": {
                "Statement": [
                    {
                        "Action": [
                            "dynamodb:BatchGetItem",
                            "dynamodb:GetRecords",
                            "dynamodb:GetShardIterator",
                            "dynamodb:Query",
                            "dynamodb:GetItem",
                            "dynamodb:Scan",
                            "dynamodb:BatchWriteItem",
                            "dynamodb:PutItem",
                            "dynamodb:UpdateItem",
                            "dynamodb:DescribeTable"
                        ],
                        "Effect": "Allow",
                        "Resource": [
                            {
                                "Fn::GetAtt": [
                                    "table123",
                                    "Arn"
                                ]
                            },
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        {
                                            "Fn::GetAtt": [
                                                "table123",
                                                "Arn"
                                            ]
                                        },
                                        "/index/*"
                                    ]
                                ]
                            }
                        ]
                    },
                    {
                        "Action": [
                            "s3:GetObject*",
                            "s3:GetBucket*",
                            "s3:List*"
                        ],
                        "Effect": "Allow",
                        "Resource": [
                            {
                                "Fn::GetAtt": [
                                    "bkt1",
                                    "Arn"
                                ]
                            },
                            {
                                "Fn::Join": [
                                    "",
                                    [
                                        {
                                            "Fn::GetAtt": [
                                                "bkt1",
                                                "Arn"
                                            ]
                                        },
                                        "/*"
                                    ]
                                ]
                            }
                        ]
                    },
                    {
                        "Action": [
                            "s3:PutObject*",
                            "s3:Abort*"
                        ],
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::Join": [
                                "",
                                [
                                    {
                                        "Fn::GetAtt": [
                                            "bkt1",
                                            "Arn"
                                        ]
                                    },
                                    "/*"
                                ]
                            ]
                        }
                    },
                    {
                        "Action": [
                            "sqs:ChangeMessageVisibility",
                            "sqs:DeleteMessage",
                            "sqs:ReceiveMessage",
                            "sqs:GetQueueAttributes",
                            "sqs:GetQueueUrl",
                            "sqs:SendMessage"
                        ],
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::GetAtt": [
                                "queue123",
                                "Arn"
                            ]
                        }
                    },
                    {
                        "Action": "sns:Publish",
                        "Effect": "Allow",
                        "Resource": {
                            "Ref": "topic123"
                        }
                    },
                    {
                        "Action": [
                            "sqs:ChangeMessageVisibility",
                            "sqs:DeleteMessage",
                            "sqs:ReceiveMessage",
                            "sqs:GetQueueAttributes",
                            "sqs:GetQueueUrl",
                            "sqs:SendMessage"
                        ],
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::GetAtt": [
                                "queue222",
                                "Arn"
                            ]
                        }
                    },
                    {
                        "Action": [
                            "sqs:ChangeMessageVisibility",
                            "sqs:DeleteMessage",
                            "sqs:ReceiveMessage",
                            "sqs:GetQueueAttributes",
                            "sqs:GetQueueUrl",
                            "sqs:SendMessage"
                        ],
                        "Effect": "Allow",
                        "Resource": {
                            "Fn::GetAtt": [
                                "queue333",
                                "Arn"
                            ]
                        }
                    }
                ],
                "Version": "2012-10-17"
            }
        };
        const targets = new aws_edge_resolver_1.AwsEdgeResolver().scrapePossibleEdgeTargets(haystack);
        const expectedTargetValues = [
            new edge_target_1.EdgeTargetSimpleString("queue333"),
            new edge_target_1.EdgeTargetSimpleString("queue123"),
            new edge_target_1.EdgeTargetSimpleString("topic123"),
            new edge_target_1.EdgeTargetSimpleString("bkt1"),
            new edge_target_1.EdgeTargetSimpleString("table123"),
            new edge_target_1.EdgeTargetSimpleString("queue222")
        ];
        expectTargetValuesToBeInSet(targets, expectedTargetValues);
        expect(targets.length).toEqual(7);
    });
    function expectTargetValuesToBeInSet(targets, expectedTargetInArray) {
        expectedTargetInArray.forEach(targetValue => {
            expect(targets).arrayToContainEdgeTarget(targetValue);
        });
    }
    it(`sample no.3`, () => {
        const haystack = {
            "policyDocument": {
                "Statement": [
                    {
                        "Action": "sqs:SendMessage",
                        "Condition": {
                            "ArnEquals": {
                                "aws:SourceArn": {
                                    "Ref": "TopicX"
                                }
                            }
                        },
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "sns.amazonaws.com"
                        },
                        "Resource": {
                            "Fn::GetAtt": [
                                "queueX2",
                                "Arn"
                            ]
                        }
                    }
                ],
                "Version": "2012-10-17"
            }
        };
        const targets = new aws_edge_resolver_1.AwsEdgeResolver().scrapePossibleEdgeTargets(haystack);
        const expectedTargetValues = [
            new edge_target_1.EdgeTargetSimpleString("TopicX"),
            new edge_target_1.EdgeTargetSimpleString("queueX2"),
            new edge_target_1.EdgeTargetSimpleString("Arn")
        ];
        expectTargetValuesToBeInSet(targets, expectedTargetValues);
        expect(targets.length).toEqual(3);
    });
    it(`sample no.4 `, () => {
        const haystack = {
            "dimensions": [
                {
                    "name": "QueueName",
                    "value": {
                        "Fn::GetAtt": [
                            "mayQueue111",
                            "QueueName"
                        ]
                    }
                },
                {
                    "name": "QueueName2",
                    "value": {
                        "Fn::ImportValue": "stack-name-here:export-name-here"
                    }
                }
            ]
        };
        const targets = new aws_edge_resolver_1.AwsEdgeResolver().scrapePossibleEdgeTargets(haystack);
        const expectedTargetValues = [
            new edge_target_1.EdgeTargetSimpleString("mayQueue111"),
            new edge_target_1.EdgeTargetSimpleString("QueueName"),
            new edge_target_1.EdgeTargetStackExport('stack-name-here', 'export-name-here')
        ];
        expectTargetValuesToBeInSet(targets, expectedTargetValues);
        expect(targets.length).toEqual(3);
    });
});
expect.extend({
    arrayToContainEdgeTarget(array, expected) {
        const foundTarget = array.find((target) => target.isEqual(expected));
        if (foundTarget) {
            return {
                message: () => `Found ${expected} in array`,
                pass: true
            };
        }
        else {
            return {
                message: () => `array does not contain expected EdgeTarget:${expected}`,
                pass: false
            };
        }
    }
});
//# sourceMappingURL=aws-edge-resolver.test.js.map