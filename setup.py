#coding=utf-8

from distutils.core import setup
import py2exe

options={
	"py2exe":{
		"compressed":1,
		"optimize":2,
		"bundle_files":1
	}
}

setup(
	author='Zephor',
	version='0.11',
	options=options,
	zipfile=None,
	console=[{
		"script":"img_to_ascii.py",
		"icon_resources":[(1,"icon_64X64.ico"),(0,"icon_64X64.ico")]
	}]
)