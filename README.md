Predator
========

What is it?
-----------

Predator is a copy detection system. It is a fork of ROCOP-A plagiarism
detection system. Written in a completely modular architecture with state-of
-art message passing technology, developers aim to provide a robust,
industry standard copy detection software with freely available source code.

Installation
------------

Predator uses various Free and Open Source Softwares. Please make sure to go
through REQUIRES file included in the distribution and install all the
mentioned dependencies beforehand to run predator. Follow the steps below
for the complete setup:

1. Execute the shell script install.sh;  
    `./install.sh`

2. You can access the rest of the features at `http://localhost` or http://ip_address
    once you login using credentials given below:     
        `username: admin`     
        `password: admin`     
    
Operation & Administration
--------------------------

Each logged in user can set their own preferences for copy detection.
Configurable parameters are label and threshold.

Once the threshold is set, percentage match below the threshold value will
be rejected. You can also set labels with the color for the match percentage.
All the matching documents will be displayed with the label color and label
text lying in the match range.

You can upload the files in the repository by visiting the 'upload' link in
the main menu. You can select multiples files to upload. But the maximum
file upload limit size is 50MB at once for uploading & checking. For
checking the copy, please visit the 'check' link in main menu and upload
your file to check.  

**In order to start all the predator services**     
    `cd /opt/predator`         
    `./bin/start_predator`     
    
**In order to stop all the predator services**    
    `cd /opt/predator`       
    `./bin/stop_predator`     
        
**In order to see all the service logs**           
    `cd /opt/predator`        
    `./bin/service_logs`          

Screenshots
-----------

It would have been even better if predator was hosted somewhere. But since i
cannot afford to put this up, i have rather uploaded the screenshots here ...
http://www.flickr.com/photos/kailashbuki/sets/72157629071025502/

Licensing
---------

Please see the LICENSE file included in the distribution.

Contacts
--------

* Email the developer at kailash.buki@gmail.com for your feedbacks, suggestions. 
* Use the tracking system in our github repository at
http://github.com/kailashbuki/predator/issues for any issues.
    
Credits
-------

Please see the AUTHORS file included in the distribution.
