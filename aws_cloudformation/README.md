# AWS CloudFormation Templates for Infrastructure as Code (IaC) Overview
This repository contains multiple CloudFormation templates designed for managing Infrastructure as Code (IaC). CloudFormation is a service provided by Amazon Web Services (AWS) that allows you to define and provision AWS infrastructure in a declarative manner.

1. Parameters
2. SSM
3. Rules 
4. mapping 
5. conditions 
6. transform 
7. Resources
8. Outputs 
9. stack updates
10. working with nested stacks
11. working with stacksets
12. custom resources
13. Template macros

## Usage of Fn::Base64
One common usage in the provided templates involves the intrinsic function Fn::Base64. This function returns the Base64 representation of the input string. It is often employed to encode data passed to Amazon EC2 instances through the UserData property...

# Usage of parameters
Parameters enable you to input custom values to your template each time you create or update a stack.
General requirements for parameters:
1. You can have a maximum of 200 parameters in an AWS CloudFormation template.
2. Each parameter must be assigned a parameter type that is supported by AWS CloudFormation. For more information
SSM Parameter Types:
SSM parameter types correspond to existing parameters in Systems Manager Parameter Store. You specify a Systems Manager parameter key as the value of the SSM parameter, and AWS CloudFormation fetches the latest value from Parameter Store to use for the stack. 
Supported AWS-specific parameter types:
AWS::EC2::AvailabilityZone::Name
AWS::EC2::Image::Id
AWS::EC2::Instance::Id
AWS::EC2::KeyPair::KeyName
AWS::EC2::SecurityGroup::GroupName
An EC2-Classic or default VPC security group name, such as my-sg-abc.

AWS::EC2::SecurityGroup::Id
A security group ID, such as sg-a123fd85.

AWS::EC2::Subnet::Id
A subnet ID, such as subnet-123a351e.

AWS::EC2::Volume::Id
An Amazon EBS volume ID, such as vol-3cdd3f56.

AWS::EC2::VPC::Id
A VPC ID, such as vpc-a123baa3.

## SSM - AWS Systems Manager Parameter Store

Parameter Store, a capability of AWS Systems Manager, provides secure, hierarchical storage for configuration data management and secrets management. You can store data such as passwords, database strings, Amazon Machine Image (AMI) IDs, and license codes as parameter values. You can store values as plain text or encrypted data. 
Note: To implement password rotation lifecycles, use AWS Secrets Manager. You can rotate, manage, and retrieve database credentials, API keys, and other secrets throughout their lifecycle using Secrets Manager. Parameter Store is also integrated with Secrets Manager. You can retrieve Secrets Manager secrets when using other AWS services that already support references to Parameter Store parameters. 
Accessible from other AWS services:

Amazon Elastic Compute Cloud (Amazon EC2)

Amazon Elastic Container Service (Amazon ECS)

AWS Secrets Manager

AWS Lambda

AWS CloudFormation

AWS CodeBuild

AWS CodePipeline

AWS CodeDeploy

Integrate with other AWS services

Configure integration with the following AWS services for encryption, notification, monitoring, and auditing:

AWS Key Management Service (AWS KMS)

Amazon Simple Notification Service (Amazon SNS)

Assigning parameter policies:
Parameter policies help you manage a growing set of parameters by allowing you to assign specific criteria to a parameter such as an expiration date or time to live. Parameter policies are especially helpful in forcing you to update or delete passwords and configuration data stored in Parameter Store, a capability of AWS Systems Manager. Parameter Store offers the following types of policies: Expiration, ExpirationNotification, and NoChangeNotification.
Add policies to an existing parameter (AWS CLI)
aws ssm put-parameter   
    --name "parameter name" \
    --value 'parameter value' \
    --type parameter type \
    --overwrite \
    --policies "[{policies-enclosed-in-brackets-and-curly-braces}]"

## Working with rules
Each template rule consists of two properties:

Rule condition (optional) – determines when a rule takes effect.
Assertions (required) – describes what values users can specify for a particular parameter.

For each rule, you can define only one rule condition. You can define one or more asserts within the Assertions property. If you don't define a rule condition, the rule's assertions always take effect.

Rule-specific intrinsic functions:
1) Fn::And
The minimum number of conditions that you can include is 2, and the maximum is 10.

!And [condition]

Parameters
condition
A condition that evaluates to true or false.

2) Fn::Equals

!Equals [value_1, value_2]

3) Fn::If
Currently, CloudFormation supports the Fn::If intrinsic function in the metadata attribute, update policy attribute, and property values in the Resources section and Outputs sections of a template. You can use the AWS::NoValue pseudo parameter as a return value to remove the corresponding property.

!If [condition_name, value_if_true, value_if_false]
Fn::If: [condition_name, value_if_true, value_if_false]

4) Fn::Not
Returns true for a condition that evaluates to false or returns false for a condition that evaluates to true. Fn::Not acts as a NOT operator.

!Not [condition]

Supported functions

You can use the following functions in the Fn::If condition:

Fn::Base64
Fn::FindInMap
Fn::GetAtt
Fn::GetAZs
Fn::If
Fn::Join
Fn::Select
Fn::Sub
Ref

## Mappings
You use the Fn::FindInMap intrinsic function to retrieve values in a map.
You can't include parameters, pseudo parameters, or intrinsic functions in the Mappings section.
example : basic mapping
Mappings: 
  RegionMap: 
    us-east-1: 
      "HVM64": "ami-0ff8a91507f77f867"
    us-west-1: 
      "HVM64": "ami-0bdb828fd58c52235"
    eu-west-1: 
      "HVM64": "ami-047bb4163c506cd98"
    ap-southeast-1: 
      "HVM64": "ami-08569b978cc4dfa10"
    ap-northeast-1: 
      "HVM64": "ami-06cd52961ce9f0d85"

Pseudo parameters reference:
Pseudo parameters are parameters that are predefined by AWS CloudFormation. You don't declare them in your template. Use them the same way as you would a parameter, as the argument for the Ref function.
The following snippet assigns the value of the AWS::Region pseudo parameter to an output value:
Outputs:
  MyStacksRegion:
    Value: !Ref "AWS::Region"

AWS::AccountId

Returns the AWS account ID of the account in which the stack is being created.

AWS::NoValue

## NESTED STACKS 
In AWS CloudFormation, nested stacks refer to the concept of breaking down a complex CloudFormation template into smaller, modular templates, which are then referenced or included within a main template. This allows you to create a hierarchy of templates where a "parent" or main template can include or reference "child" templates, creating a nested structure.

The key benefits of using nested stacks in CloudFormation include:

1. Modularity: Break down a large and complex CloudFormation template into smaller, more manageable pieces. 
 piece can focus on specific resources or components of your infrastructure.

2. Reusability: Create reusable templates that can be used across different stacks. This can be particularly useful when you have common infrastructure patterns that are repeated in multiple environments or applications.

3. Scoping Permissions: Assign permissions at the nested stack level, allowing you to control access to specific parts of your infrastructure.

4. Parallelization: Deploying nested stacks can be done in parallel, which can improve deployment times.

### Does the order of resource definitions matter? ?
The order of resource declaration within a CloudFormation template doesn't usually matter, but defining dependencies correctly is crucial for successful stack creation.


