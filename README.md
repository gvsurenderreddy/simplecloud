SimpleCloud - The Open Source Virtualization Management Software
===========

http://simplecloud.github.com

SimpleCloud is an IaaS (Infrastructure as a Service) software and virtualization management platform.

![SimpleCloud Dashboard screenshot](http://github.com/simplecloud/simplecloud/raw/master/screenshots/en/admindashboard.png)

Features
===========

- Virtual Resource Management
  - Add/Remove host
  - Virtualmachine lifecycle
  - Image management
  - Template management
  - Basic Network/Storage configuration
  - Role-based access control (RBAC)
- Task Management
- User Management
- KVM Hypervisor Support
- Web UI
  - Flask/Bootstrap
  - Both English and Chinese Support
  - Admin View: Dashboard/Users/Hosts/VirtualMachines/Images/Templates/Tasks/System 
  - User View: VirtualMachines/Templates

Screenshots
==========

More screenshots:

* English version: [Screenshots List](https://github.com/simplecloud/simplecloud/blob/master/screenshots.md)
* Chinese version: [Screenshots List](https://github.com/simplecloud/simplecloud/blob/master/screenshots_chs.md)
  
Install
==========

### Requirement

* 1 * SimpleCloud Server
    
    Management node, deploy all the simplecloud code. 
* At least 1 * KVM Host
    
    KVM host node, where virtual machines are running. No agent needed, just few steps of configuration.
* 1 * Storage server

    Shared storage server. SimpleCloud Server and Hypervisor Host should mounted this storage on same path.

### Install SimpleCloud Server

Add local user

    $ sudo groupadd simplecloud
    $ sudo useradd -d /home/simplecloud -m -s /bin/bash  -g simplecloud simplecloud
    $ sudo usermod -G libvirtd -a simplecloud

Create instance workspace and mount nfs server. 

    $ sudo mkdir <INSTANCE_FOLDER_PATH>
    $ sudo mkdir <INSTANCE_FOLDER_PATH>/config
    $ sudo chown simplecloud:simplecloud <INSTANCE_FOLDER_PATH>
    $ sudo mount -t nfs <NFS_SERVER>:<PATH> <INSTANCE_FOLDER_PATH>

Create the SSH key pair, the public key /home/simplecloud/id_rsa.pub will be used in libvirt connection to KVM servers.

    $ ssh-keygen

Download source code

    $ su -l simplecloud
    $ git clone https://github.com/simplecloud/simplecloud

Update the INSTANCE_FOLDER_PATH in simplecloud/fabric.py and simplecloud/simplecloud/utils.py

    $ cd simplecloud
    $ vim fabric.py
    $ vim simplecloud/utils.py

Update the default admin user and password in simplecloud/manage.py initdb()

    $ vim manage.py

Setup the virtualenv.

    $ cd simplecloud
    $ fab setup

Copy the libvirt python binding to virtualenv (python-libvirt is not included in pip)

    $ cp /usr/lib/python2.7/dist-packages/libvirt* env/lib/python2.7/

Copy configuration xml file to <INSTANCE_FOLDER_PATH>/config

    $ cp config/kvm.xml <INSTANCE_FOLDER_PATH>/config/vm.xml

Choice 1: Run in debug mode, access the web page in http://<SIMPLECLOUD_SERVER_IP>:5000

    $ fab debug

Choice 2: Deploy with apache2 and WSGI, access the web page in http://<SIMPLECLOUD_SERVER_IP>

Check the app.wsgi file, and read the comments to add /etc/apache2/sites-available/simplecloud.
    
    $ cd /var/www
    $ sudo ln -s <SIMPLECLOUD_SOURCE_PATH> simplecloud
    $ sudo service apache2 restart

### Configure KVM Host

Add local user

    $ sudo groupadd simplecloud
    $ sudo useradd -d /home/simplecloud -m -s /bin/bash  -g simplecloud simplecloud

Create instance workspace and mount nfs server. 

    $ sudo mkdir <INSTANCE_FOLDER_PATH>
    $ sudo chown simplecloud:simplecloud <INSTANCE_FOLDER_PATH>
    $ sudo mount -t nfs <NFS_SERVER>:<PATH> <INSTANCE_FOLDER_PATH>

Copy public key from SimpleCloud Server /home/simplecloud/id_rsa.pub and setup the SSH public key authentication for libvirt connection.

Libvirt SSH setup reference: http://wiki.libvirt.org/page/SSHSetup

Developer Guide
==========

* Chinese version: [Developer Guide](https://github.com/simplecloud/simplecloud/blob/master/design.md)


ACKNOWLEDGEMENTS
==========

Thanks to Wilson Xu's project [Fbone](https://github.com/imwilsonxu/fbone), Python, Flask and its extensions.

License
===========

Apache License, Version 2.0





