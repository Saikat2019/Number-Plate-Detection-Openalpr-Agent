# NUMBER PLATE RECOGNITION USING OPENALPR AGENT

<img src="https://raw.githubusercontent.com/Saikat2019/MY_README_TEMPLATE/master/README_RES/icon.jpeg" align="right" />

> Used Programming languages/Libraries

[![Language](https://img.shields.io/badge/python-3.7-009900.svg)](https://docs.python.org/3/)
[![Library](https://img.shields.io/badge/OPENALPR-006600.svg)](https://cloud.openalpr.com/)

We deployed our code in a Respberry Pi 4 (4GB RAM) with a standard IP Camera.

## Table of Contents
- [Installation](#Installation)
- [Steps](#Steps)
- [Examplanation](#Examplanation)
- [Contributers](#Contributers)
- [License](#License)

## Installation
First we need to install and sign in to Openalpr agent in our system. A detailed tutorial can be found [here](http://doc.openalpr.com/on_premises.html#watchman-agent).

[OpenALPR Agent Installation](http://doc.openalpr.com/on_premises.html#installation). Click here for the installation process.http://doc.openalpr.com/on_premises.html#installation.

After installation is completed, our agent need to be configured. First open OpenALPR agent by<b> ```$sudo alprdconfig```</b>

Then go to <b>Configure -> Agent settings -> Advanced.</b>

<pre>Now change the values of <b>- store_plate = 1
                         - store_video = 1
                         - store_video_maxsize_gb = 1
                         - upload_data = 0
                         - web_server_enabled = 1
                         - websockets_enabled = 0</b></pre>
<b>Now restart OpenALPR.</b>
To test the program, first launch the OpenALPR Agent and then sign in and add the camera, then run the script to upload numbers into our server
```bash
python3 openAlpr2db.py
```
You may need to install some python3 dependencies.
```bash
pip3 install -r requirements.txt
```
[↥ back to top](#table-of-contents)

## Steps  
- ### If you clone the repository
- 1.Open the npd.sh file and change the path to the python script according to your system. If you have installed the
    OpenALPR Agent correctly, you should have an alprdconfig file at the location /usr/bin/alprdconfig .
    The npd.sh file will look like this    
```bash
1 python3 /home/saikat/openAlpr2db.py & 
2 sleep 5
3 /usr/bin/sudo /usr/bin/alprdconfig 
```
- 2.Open the npd.desktop file and change the paths ,Exec=path_to-npd.sh and Icon=your-icon.png.
- 3.Make the npd.sh and npd.desktop executable by
```bash
$ chmod +x npd.sh
$ chmod +x npd.desktop
```
Now launch the program by clicking the npd.desktop file

- ### If you don't have or haven't created the npd.desktop file as mentioned earlier.
- 1.First Sign in to https://cloud.openalpr.com/
- 2.Install OpenALPR Agent and sign in.
- 3.Add and select your camera in the panel in left side.
- 4.Run the openAlpr2dp.py


[↥ back to top](#table-of-contents)

## Explanation

Openalpr Agent store the number plate results after detection as a beanstalk queue. From there we store the results in local 
database and upload to our database eventually from the script,openAlpr2db.py

[↥ back to top](#table-of-contents)

## Contributers

[Saikat Mondal  ](https://github.com/Saikat2019)<img src="https://avatars2.githubusercontent.com/u/33754597?v=4" width="20" height="20" />

[↥ back to top](#table-of-contents)

## License

[↥ back to top](#table-of-contents)
