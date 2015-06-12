#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Initial data for a databae

Projects description sources:
http://www.datamation.com/open-source/35-open-source-tools-for-the-internet-of-things-1.html

to run use command: python lotsofprojects.py
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Project, User


engine = create_engine('sqlite:///projects_catalog_users.db', echo=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#Create dummy user
User1 = User(social_id = 45256457,
             name = "Robo Barista",
             email = "tinnyTim@udacity.com",
             picture = "https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png")
session.add(User1)
session.commit()


#Projects in Development Tools category
category1 = Category(user_id=1,
                     name = "Development Tools",
                     image = u"http://www.geekylemon.com/xcode-1.png")

session.add(category1)
session.commit()
print("1. Development Tools: added to Category table")


project1 = Project(name = u"Arduino",
                   abstract = u"Arduino is both a hardware specification for interactive electronics and a set of software that includes an IDE and the Arduino programming language.",
                   description = u"Arduino is both a hardware specification for interactive electronics and a set of software that includes an IDE and the Arduino programming language. The website explains that Arduino is a tool for making computers than can sense and control more of the physical world than your desktop computer. The organization behind it offers a variety of boards, starter kits, robots and related products for sale, and many other groups have used Arduino to build IoT-related hardware and software products of their own.",
                   image = u"https://im1-tub-ru.yandex.net/i?id=75c3770933a4c87db36ccc71edc62f2b&n=21",
                   license = u"LGPL",
                   website = u"http://www.arduino.cc/",
                   category = category1,
                   user_id=1)

session.add(project1)
session.commit()


project2 = Project(name = u"Eclipse IoT Project",
                   abstract = u"Eclipse is sponsoring several different projects surrounding IoT.",
                   description = u"Eclipse is sponsoring several different projects surrounding IoT. They include application frameworks and services; open source implementations of IoT protocols, including MQTT CoAP, OMA-DM and OMA LWM2M; and tools for working with Lua, which Eclipse is promoting as an ideal IoT programming language. Eclipse-related projects include Mihini, Koneki and Paho. The website also includes sandbox environments for experimenting with the tools and a live demo.",
                   image = u"http://www.eclipse.org/community/eclipse_newsletter/2014/february/images/iot_news.png",
                   license = u"unclear",
                   website = u"http://iot.eclipse.org/",
                   category = category1,
                   user_id=1)

session.add(project2)
session.commit()


project1 = Project(name = u"Kinoma",
                   abstract = u"Kinoma’s platform is optimized for connected, high-performance consumer electronics and Internet of Things (IoT) products. Build rich consumer experiences that orchestrate connected devices, their companion apps, and cloud services.",
                   description = u"Owned by Marvell, the Kinoma software platform encompasses three different open source projects. Kimona Create is a DIY construction kit for prototyping electronic devices. Kimona Studio is the development environment that works with Create and the Kinoma Platform Runtime. Kimona Connect is a free iOS and Android app that links smartphones and tables with IoT devices.",
                   image = u"http://kinoma.com/develop/docs/technotes/images/dial/create-home.jpg",
                   license = u"Depends on project",
                   website = u"http://www.marvell.com/kinoma/",
                   category = category1,
                   user_id=1)

session.add(project1)
session.commit()


project3 = Project(name = u"Node-RED",
                   abstract = u"Built on Node.js, Node-RED describes itself as a visual tool for wiring the Internet of Things.It allows developers to connect devices, services and APIs together using a browser-based flow editor. It can run on Raspberry Pi, and more than 60,000 modules are available to extend its capabilities.",
                   description = u"Node-RED provides a browser-based flow editor that makes it easy to wire together flows using the wide range nodes in the palette. Flows can be then deployed to the runtime in a single-click. JavaScript functions can be created within the editor using the a rich text editor. A built-in library allows you to save useful functions, templates or flows for re-use.",
                   image = u"http://nodered.org/images/node-red-screenshot-sm.png",
                   license = u"Apache License",
                   website = u"http://nodered.org/",
                   category = category1,
                   user_id=1)

session.add(project3)
session.commit()


#Projects in Hardware category
category2 = Category(user_id=1,
                     name = "Hardware",
                     image = u"http://lh3.ggpht.com/XCpnkn71ohACTG3Zfqz0lv35UvZAYvlnK4LuONIpwbNsfUU318LXERRdGmLoMHeE_JQ=w300")
print("2. Hardware: added to Category table")
session.add(category2)
session.commit()


project1 = Project(name = u"Arduino Yun",
                   abstract = u"This microcontroller combines the ease of an Arduino-based board with Linux",
                   description = u"This microcontroller combines the ease of an Arduino-based board with Linux. It includes two processors—the ATmega32u4 (which supports Arduino) and the Atheros AR9331 (which runs Linux). Other features include Wi-Fi, Ethenet support, a USB port, micro-SD card slot, three reset buttons and more. They are available for purchase from the Arduino website.",
                   image = u"http://blog.antory.ru/wp-content/uploads/arduino_uno_r3_1_LRG.jpg",
                   license = u"unclear",
                   website = u"http://arduino.cc/en/Main/ArduinoBoardYun?from=Main.ArduinoYUN",
                   category = category2,
                   user_id=1)

session.add(project1)
session.commit()


project2 = Project(name = u"BeagleBoard",
                   abstract = u"BeagleBoard offers credit-card sized computers that can run Android and Linux.",
                   description = u"BeagleBoard offers credit-card sized computers that can run Android and Linux. Because they have very low power requirements, they're a good option for IoT devices. Both the hardware designs and the software they run are open source, and BeagleBoard hardware (often sold under the name BeagleBone) is available through a wide variety of distributors.",
                   image = u"http://blogosquare.com/wp-content/uploads/2013/06/09444-01.jpg",
                   license = u"unclear",
                   website = u"http://beagleboard.org/",
                   category = category2,
                   user_id=1)

session.add(project2)
session.commit()


project3 = Project(name = u"Flutter",
                   abstract = u"Flutter's claim to fame is its long range. ",
                   description = u"Flutter's claim to fame is its long range. This Arduino-based board has a wireless transmitter that can reach more than a half mile. Plus, you don't need a router; flutter boards can communicate with each other directly. It includes 256-bit AES encryption, and it's easy to use. Both the hardware and the software are completely open source, and the price for a basic board is just $20.",
                   image = u"http://www.rlocman.ru/i/Image/2013/09/04/Flutter.jpg",
                   license = u"unclear",
                   website = u"http://www.flutterwireless.com/",
                   category = category2,
                   user_id=1)

session.add(project3)
session.commit()


project4 = Project(name = u"Local Motors Connected Car",
                   abstract = u"Local Motors is a car company that manufactures open source car designs on a small scale. ",
                   description = u"Local Motors is a car company that manufactures open source car designs on a small scale. They collaborated with IBM on an IoT-connected vehicle that they showed off at a conference last spring. Much of the open source software and design specifications for the prototype are available for download from the link above.",
                   image = u"http://uploads.webflow.com/54526d02b51342c22660562d/54b0065e7cff80c063172322_hero.png",
                   license = u"unclear",
                   website = u"https://localmotors.com/awest/connected-car-project-internet-of-things/",
                   category = category2,
                   user_id=1)

session.add(project4)
session.commit()


project5 = Project(name = u"Microduino",
                   abstract = u"Microduino offers really small boards that are compatible with Arduino",
                   description = u"As you might guess from its name, Microduino offers really small boards that are compatible with Arduino. In fact, these boards are about the size of a quarter and can be stacked together to create new things. All the hardware designs are open source, and core modules start at just $8 each. It was funded by a Kickstarter campaign that raised $134,563",
                   image = u"http://www.hobbycomponents.com/images/forum/HCMIDU0001_800.jpg",
                   license = u"unclear",
                   website = u"http://www.microduino.cc/",
                   category = category2,
                   user_id=1)

session.add(project5)
session.commit()


#Projects in Automation Software category
category3 = Category(user_id=1,
                     name = u"Home Automation Software",
                     image = u"http://www.vesternet.com/media/wysiwyg/Heating_main.jpg")
print("3. Home Automation Software: added to Category table")
session.add(category3)
session.commit()


project1 = Project(name = u"OpenHAB",
                   abstract = u"OpenHAB lets the smart devices you already have in your home talk to one another",
                   description = u"OpenHAB lets the smart devices you already have in your home talk to one another. It's vendor- and hardware-neutral, running on any Java-enabled system. One of its goals is to allow users to add new features to their devices and combine them in new ways. It's won several awards, and it has a companion cloud computing service called my.openHAB.",
                   image = u"http://www.nixp.ru/uploads/news/fullsize_image/6919e088ac708360bc6a70cc606d52aefdea8710.png",
                   license = u"unclear",
                   website = u"http://www.openhab.org/",
                   category = category3,
                   user_id=1)

session.add(project1)
session.commit()


project2 = Project(name = u"The Thing System",
                   abstract = u"This project includes both software components and network protocols",
                   description = u"This project includes both software components and network protocols. It promises to find all the Internet-connected things in your house and bring them together so that you can control them. It supports a long list of devices, including Nest thermostats, Samsung Smart Air Conditioners, Insteon LED Bulbs, Roku, Google Chromecast, Pebble smartwatches, Goji smart locks and much more. It's written in Node.js and can fit on a Raspberry Pi.",
                   image = u"https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSzFB9vzEwpc1PhX2RcJx9AuPmHK4vtnNlfTSsoMaivwnILVNef",
                   license = u"unclear",
                   website = u"http://thethingsystem.com/index.html",
                   category = category3,
                   user_id=1)

session.add(project2)
session.commit()


print "All projects added!"

