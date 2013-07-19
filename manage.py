# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from simplecloud import create_app
from simplecloud.extensions import db
from simplecloud.user import User, ADMIN, USER, USER_ACTIVE
from simplecloud.image import Image
from simplecloud.template import Template
from simplecloud.host import Host

app = create_app()
manager = Manager(app)

@manager.command
def run():
    """Run in local machine."""

    app.run()


@manager.command
def inittestdb():
    """Init/reset database."""

    db.drop_all()
    db.create_all()

    admin = User(
            name=u'admin',
            email=u'admin@example.com',
            password=u'000000',
            role_code=ADMIN,
            status_code=USER_ACTIVE)
    user = User(
            name=u'test',
            email=u'test@example.com',
            password=u'000000',
            role_code=USER,
            status_code=USER_ACTIVE)
    db.session.add(admin)
    db.session.add(user)
    
    # Just for test
    image1 = Image(name=u'image1', src_path="/")
    image2 = Image(name=u'image2', src_path="/")
    image3 = Image(name=u'image3', src_path="/")
    template1 = Template(
            name=u'template1',
            image_id=1,
            vcpu=1,
            memory=1024,
            disk=10240)
    template2 = Template(
            name=u'template2',
            image_id=2,
            vcpu=2,
            memory=2048,
            disk=102400)
    host1 = Host(
            address="192.168.1.1",
            uri="qemu+ssh://root@192.168.1.1/system")
    host2 = Host(
            address="192.168.1.2",
            uri="xen+ssh://root@192.168.1.2/")
    db.session.add(image1)
    db.session.add(image2)
    db.session.add(image3)
    db.session.add(template1)
    db.session.add(template2)
    db.session.add(host1)
    db.session.add(host2)
    db.session.commit()

@manager.command
def initdb():
    """Init/reset database."""

    db.drop_all()
    db.create_all()

    admin = User(
            name=u'admin',
            email=u'admin@example.com',
            password=u'000000',
            role_code=ADMIN,
            status_code=USER_ACTIVE)
    db.session.add(admin)
    db.session.commit()



manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
