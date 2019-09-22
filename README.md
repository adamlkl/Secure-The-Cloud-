# Secure The Cloud #

## Purpose ##
The aim of this project is to develop a secure cloud storage application for Dropbox, Box, Google Drive, Ofﬁce365 etc. For example, the application should be able to secure all ﬁles that are uploaded to the cloud, such that only people that are part of your “Secure Cloud Storage Group” will be able to decrypt your uploaded ﬁles. To all other users the ﬁles will be encrypted.
<br />
A suitable key management system will be designed and implemented for the application that will allow ﬁles to be shared securely, and users to be added and removed from “Secure Cloud Storage Group”. The application can be set up on a desktop or mobile platform and make use of any open source cryptographic libraries.

## Introduction ##
Data encryptionare typically employed in activities concerned with communications to protect the contents of text, messages and even ﬁles from being comprehended by anyone but the intended recipients. Aside from that, it allow recipients prove that a message came from a particular sender and has not been intercepted and altered.
<br />
End-to-end encryption relies heavily on public key cryptography tools. Under normal circumstances, this can be achieved using Symmetric Encryption. The problem statement behind this approach is that the sender wants to pass a message to the intended receiver through a channel. However,this channel consists of several intermediaries that are nosy and insecure. In other words, it is constantly being peeked on by an outsider and vulnerable to attacks. Thus,it is vital to encrypt the message before transmission and have it decrypted when payload data reaches the receiver. This way, even if the message is intercepted in the middle of the transmission, no one other than the intended receiver could comprehend its contents. In this approach,the encryption keys used for both sides are the same, hence it is called symmetric encryption.
<br />
<img src="https://github.com/adamlkl/Secure-The-Cloud-/blob/master/documentation/Images/normal.png" />
Nevertheless, this is nowhere close in providing ample assurance on the security of the transmission as symmetric cryptography doesn’t address the issue where someone could just eavesdrop and steal the symmetric key being sent from the sender to the receiver.
<img src="https://github.com/adamlkl/Secure-The-Cloud-/blob/master/documentation/Images/midatk.png" />
This allows the eavesdropper to conduct attacks in the middle by intercepting the message and make alterations to the contents. the attacker could read, alter and delete information packed in the payload and sends it to the receiver.
<img src="https://github.com/adamlkl/Secure-The-Cloud-/blob/master/documentation/Images/messing.png" />
Consequently, the wrong message will be directed towards the receiver instead.
<img src="https://github.com/adamlkl/Secure-The-Cloud-/blob/master/documentation/Images/wrong.png" />
To compensate for this vulnerability, another encryption has to be implemented to make the symmetric key resilient to the attacks mentioned above. One initiative that can be resorted to is by encrypting the symmetric key using public key and read the decrypted version using the corresponding private key. The idea is to have the receiver broadcasting his or her public key while the sender use it to encrypt the keys or messages. As a result, only the intended can read the data while the intermediaries only have access to the metadata, such as the subject line, dates, sender, and recipient.
<img src="https://github.com/adamlkl/Secure-The-Cloud-/blob/master/documentation/Images/proper.png" />
## Design ##
The implementation of this assignment can be divided into mainly two components: User Interface and a Cloud Storage Group. These components make use of different modules that consists of helper functions to execute their tasks.
<br />
The highlight of the design revolves around how to transmit symmetric keys to valid users in the group securely. The symmetric keys used for encryption when uploading ﬁles and decryption when downloading. One critical assumption that is took on during the development of the application is such that the activities of the cloud storage group is always being peeked on and the contents in it is always exposed to outsiders.
<br />
As a result, the contents in the cloud storage has to be encrypted for data protection and can only be decrypted by users who have access to the symmetric keys. To achieve this, a symmetric key has to shared securely among the users. The initiative taken here is to have the users send their public keys to the cloud storage group, so that it can be used to encrypt the symmetric key during transmission.
<br />
For this assignment, the target cloud storage is Google Drive. Further and more circumstantial explanation of the modus operandi will be elaborated later while the described design is as illustrated below.
<img src="https://github.com/adamlkl/Secure-The-Cloud-/blob/master/documentation/Images/design.png" />
A more thorough explanation can be found <a href="https://github.com/adamlkl/Secure-The-Cloud-/blob/master/documentation/Assignment%20Report%20.pdf">here</a>.
