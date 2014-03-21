#coding=utf-8
from __future__ import division
"""
好玩的基于PIL的图片转字符画~~
"""

__author__='Zephor'
__version__=0.1

import sys,os,re,random
from cStringIO import StringIO
# print dir(StringIO())
try:
	from PIL import Image
except:
	print 'you need PIL module to use this tool'
	sys.exit(0)


__filename__=os.path.basename(sys.argv[0])
__dir__=os.getcwd()

__help__=\
"""usage for this tool:
"""+__filename__+""" imagePath [targetName] [size]
	imagePath can be relative path to execute dir or absolute path
	targetName  the name to save for the char_img
	size must format in [x,y] , x and y are numbers
"""


# 预处理部分
# 在其他文件完成，计算每一个可打印的char所对应的灰度像素

# from __future__ import division
# from PIL import Image,ImageFont,ImageDraw

# ascii = ('nul', 'soh', 'stx', 'etx', 'eot', 'enq', 'ack', 'bel', 'bs', 'ht', 'nl', 'vt', 'np', 'cr', 'so', 'si', 'dle', 'dc1', 'dc2', 'dc3', 'dc4', 'nak', 'syn', 'etb', 'can', 'em', 'sub', 'esc', 'fs', 'gs', 'rs', 'us', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'del')

# font = ImageFont.load_default()

# intensities = []

# single_size = font.getsize('.')

# all_pixel = single_size[0]*single_size[1]

# max_pixel = 27 	# 第一遍以all_pixel为基数，通过测量得出的占比最大的字符所占像素数，对应字符为$,H
#					# 然后使用该数值对应扩展成灰度值
# for i in xrange(32,127): 	# 可打印的ascii范围 32-126
# 	temp = 0
# 	im = Image.new('1', single_size, 'black')
# 	d = ImageDraw.Draw(im)
# 	d.text( (0,0), ascii[i], font=font, fill='white')
# 	for x in xrange(0,single_size[0]):
# 		for y in xrange(0,single_size[1]):
# 			if im.getpixel((x,y)) >0:
# 				temp+=1
# 	intensities.append( (i, int(round((1-temp/max_pixel)*255))) )
# sorted_ = sorted(intensities, key=lambda intensity:intensity[1])
# pixel_ascii = {}
# for s in sorted_:
# 	if pixel_ascii.has_key(s[1]):
# 		pixel_ascii[s[1]].append(ascii[s[0]])
# 	else:
# 		pixel_ascii[s[1]] = [ascii[s[0]],]
# print pixel_ascii


# 由上面处理得到
__pixel_to_ascii = {0: ['$', 'H'], 9: ['0', 'd', 'g', 'q'], 142: ['(', ')', '?'], 19: ['8', 'R', 'p'], 28: ['5', '6', '9', '@', 'B', 'D', 'N', 'Q', 'U', 'b', 'h', 'k'], 161: ['!', '<', '>'], 38: ['A', 'K'], 170: ['*', '+'], 47: ['#', '2', '4', 'E', 'G', 'O', 'Z', 'y'], 179: ['/', '=', '\\', '^'], 57: ['%', '3', 'M', 'P', 'S', 'a', 'f', 'u'], 189: ['|'], 66: ['&', '1', 'W', 'X', 'Y', 'l', 't', 'x'], 198: ['"', ';', '_', '~'], 76: ['7', 'C', 'j', 'n', 's', 'z'], 208: ['-'], 85: ['F', 'L', 'T', 'V', '[', ']', 'e', 'i', 'm', 'o', 'w'], 217: ["'", ',', ':', '`'], 94: ['J', 'r'], 104: ['I', 'c', '{', '}'], 236: ['.'], 113: ['v'], 255: [' ']}

def random_int( up=10 ): return random.randint(0,up-1)

def get_char( greyValue=255 ):
	"""
	由灰度值取得字符
	"""
	if greyValue < 0 or greyValue > 254:
		return ' '
	s_keys = sorted(__pixel_to_ascii.keys())
	j = 0
	for i in xrange(0,len(s_keys)):
		j = i
		if greyValue < s_keys[i]:
			if greyValue - s_keys[i-1] < s_keys[i] - greyValue:
				j = i-1
		else:
			continue
		d = __pixel_to_ascii[s_keys[j]]
		return d[ random_int(len(d)) ]

def do_char_convert( imageAbsPath = '', targetName = None, tSize = [500,500] ):
	if not ( imageAbsPath and os.path.isfile( imageAbsPath ) ):
		show( 'err_name' )
		return
	try:
		img = Image.open( imageAbsPath )
		# print 'it is'
	except:
		show( 'err_type' )
		return

	convert_list = [ get_char(x) for x in xrange(0,256) ]
	imgName, oExt = os.path.splitext( os.path.basename(imageAbsPath) )
	tartget = imgName+'_ascii'
	# tExt = oExt
	if targetName:
		tartget = targetName
	# help( img )
	img = img.convert('L')
	oSize = img.size
	if oSize[0]>tSize[0] or oSize[1]>tSize[1]:
		if img.size[0] > img.size[1]:
			tSize[1] = int(round(oSize[1]*tSize[0]/oSize[0]))
		else:
			tSize[0] = int(round(oSize[0]*tSize[1]/oSize[1]))
		img = img.resize( tSize )
	s = StringIO()
	try:
		for y in xrange( 0, img.size[1] ):
			for x in xrange( 0, img.size[0] ):
				greyValue = img.getpixel((x,y))
				s.write( convert_list[ greyValue ] + convert_list[ greyValue ] )
			s.write( '\n' )
		with open(tartget+'.txt','w') as f:
			s.seek(0)
			f.write( s.read() )
	finally:
		s.close()
	# img.save('test.jpg')

def show( content ):
	if content == 'help':
		print __help__
	elif content.startswith('err'):
		if content[4:]  == 'name':
			print 'input name error'
		elif content[4:] == 'type':
			print 'file type isn\'t image or image data was broken'
	else:
		print content


def main():
	argv = sys.argv[1:]
	if len(argv) < 1 or 'help' == argv[0]:
		show('help')
		return
	re_size = re.compile( '^[\[]\d+,\d+[\]]$' )
	imagePath = argv[0]
	targetName = None
	tSize = [500,500]

	if os.path.isfile( __dir__+os.sep+imagePath ):
		imagePath = __dir__+os.sep+imagePath
	elif not os.path.isfile(imagePath):
			show('err_name')
			return
	argv.extend(['',''])
	if re_size.match(argv[1]):
		tSize = eval(argv[1])
	elif re_size.match(argv[2]):
		targetName = argv[1]
		tSize = eval(argv[2])
	else:
		targetName = argv[1]

	do_char_convert( imagePath, targetName, tSize )


if __name__ == '__main__':
	main()
	# print __dir__
	# print sys.argv