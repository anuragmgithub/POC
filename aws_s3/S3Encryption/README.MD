Amazon S3 Server-Side Encryption (SSE) Options
Amazon S3 (Simple Storage Service) provides various server-side encryption options to protect your data at rest. This README explains the three main SSE options: SSE-S3, SSE-KMS, and SSE-C.

1. SSE-S3 (Server-Side Encryption with Amazon S3-Managed Keys)
Key Management:
Amazon S3 manages the encryption keys on your behalf.
Encryption:
Each object is encrypted with a unique data key.
The data key is itself encrypted with a master key that is regularly rotated.
Trade-offs:
Easy to use because S3 manages the keys.
Limited control over key management.
Use Case:
Suitable for general data protection and data at rest encryption.
2. SSE-KMS (Server-Side Encryption with AWS Key Management Service)
Key Management:
AWS Key Management Service (KMS) is used to manage encryption keys.
Encryption:
Each object is encrypted with a unique data key.
The data key is encrypted with a KMS-generated master key.
Trade-offs:
Provides more control over key management, including access control, auditing, and custom KMS keys.
Additional costs associated with KMS key usage.
Use Case:
Ideal for applications with specific security or compliance requirements and where fine-grained control over key management is necessary.
3. SSE-C (Server-Side Encryption with Customer-Provided Keys)
Key Management:
You provide your own encryption keys to S3.
Encryption:
Each object is encrypted with the provided customer key.
Trade-offs:
Offers the most control over key management.
Requires careful handling of encryption keys and can be more complex.
Use Case:
Best for situations where you have stringent security requirements and need the highest level of control over encryption.
