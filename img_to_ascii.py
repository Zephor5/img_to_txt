# coding=utf-8
from __future__ import division

"""
好玩的基于PIL的图片转字符画~~
"""

import sys
import os
import re
import random
from cStringIO import StringIO
from PIL import Image, ImageFont, ImageDraw

__author__ = 'Eric Wu'
__version__ = 0.1

__filename__ = os.path.basename(sys.argv[0])
__dir__ = os.getcwd()

__help__ = \
    """usage for this tool:
""" + __filename__ + """ imagePath [targetName] [size]
imagePath can be relative path to execute dir or absolute path
targetName  the name to save for the char_img
size must format in [x,y] , x and y are numbers
"""


def get_ascii_pixels():
    # 预处理部分
    # 在其他文件完成，计算每一个可打印的char所对应的灰度像素

    ascii = (
        'nul', 'soh', 'stx', 'etx', 'eot', 'enq', 'ack', 'bel', 'bs', 'ht', 'nl', 'vt', 'np', 'cr', 'so', 'si', 'dle',
        'dc1', 'dc2', 'dc3', 'dc4', 'nak', 'syn', 'etb', 'can', 'em', 'sub', 'esc', 'fs', 'gs', 'rs', 'us', ' ', '!',
        '"',
        '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8',
        '9',
        ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
        'P',
        'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f',
        'g',
        'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}',
        '~',
        'del'
    )

    font = ImageFont.load_default()

    intensities = []

    char_size = font.getsize('.')

    max_pixel = 0  # 第一遍以all_pixel为基数，通过测量得出的占比最大的字符所占像素数27，对应字符为$,H
    for i in xrange(32, 127):  # 可打印的ascii范围 32-126
        temp = 0
        im = Image.new('1', char_size, 'black')
        d = ImageDraw.Draw(im)
        d.text((0, 0), ascii[i], font=font, fill='white')
        for x in xrange(0, char_size[0]):
            for y in xrange(0, char_size[1]):
                if im.getpixel((x, y)) > 0:
                    temp += 1
        if temp > max_pixel:
            max_pixel = temp
    # 然后使用该数值对应扩展成灰度值
    for i in xrange(32, 127):  # 可打印的ascii范围 32-126
        temp = 0
        im = Image.new('1', char_size, 'black')
        d = ImageDraw.Draw(im)
        d.text((0, 0), ascii[i], font=font, fill='white')
        for x in xrange(0, char_size[0]):
            for y in xrange(0, char_size[1]):
                if im.getpixel((x, y)) > 0:
                    temp += 1
        intensities.append((i, int(round((1 - temp / max_pixel) * 255))))
    sorted_ = sorted(intensities, key=lambda intensity: intensity[1])
    pixel_ascii = {}
    for s in sorted_:
        if s[1] in pixel_ascii:
            pixel_ascii[s[1]].append(ascii[s[0]])
        else:
            pixel_ascii[s[1]] = [ascii[s[0]], ]
    return pixel_ascii


__pixel_to_ascii = None

if __pixel_to_ascii is None:
    __pixel_to_ascii = get_ascii_pixels()
# 由上面处理得到
# __pixel_to_ascii = {0: ['$', 'H'], 9: ['0', 'd', 'g', 'q'], 142: ['(', ')', '?'], 19: ['8', 'R', 'p'],
#                     28: ['5', '6', '9', '@', 'B', 'D', 'N', 'Q', 'U', 'b', 'h', 'k'], 161: ['!', '<', '>'],
#                     38: ['A', 'K'], 170: ['*', '+'], 47: ['#', '2', '4', 'E', 'G', 'O', 'Z', 'y'],
#                     179: ['/', '=', '\\', '^'], 57: ['%', '3', 'M', 'P', 'S', 'a', 'f', 'u'], 189: ['|'],
#                     66: ['&', '1', 'W', 'X', 'Y', 'l', 't', 'x'], 198: ['"', ';', '_', '~'],
#                     76: ['7', 'C', 'j', 'n', 's', 'z'], 208: ['-'],
#                     85: ['F', 'L', 'T', 'V', '[', ']', 'e', 'i', 'm', 'o', 'w'], 217: ["'", ',', ':', '`'],
#                     94: ['J', 'r'], 104: ['I', 'c', '{', '}'], 236: ['.'], 113: ['v'], 255: [' ']}


def random_int(up=10): return random.randint(0, up - 1)


def get_char(grey_value=255):
    """
    由灰度值取得字符
    """
    if grey_value < 0 or grey_value > 254:
        return ' '
    s_keys = sorted(__pixel_to_ascii.keys())
    for i in xrange(0, len(s_keys)):
        j = i
        if grey_value < s_keys[i]:
            if grey_value - s_keys[i - 1] < s_keys[i] - grey_value:
                j = i - 1
        else:
            continue
        d = __pixel_to_ascii[s_keys[j]]
        return d[random_int(len(d))]


def do_char_convert(image_abspath='', target_name=None, t_size=None):
    if not t_size:
        t_size = [500, 500]
    if not (image_abspath and os.path.isfile(image_abspath)):
        show('err_name')
        return
    try:
        img = Image.open(image_abspath)
    except:
        show('err_type')
        return

    convert_list = [get_char(x) for x in xrange(0, 256)]
    img_name, o_ext = os.path.splitext(os.path.basename(image_abspath))
    target = img_name + '_ascii'
    # tExt = o_ext
    if target_name:
        target = target_name
    # help( img )
    img = img.convert('L')
    o_size = img.size
    if o_size[0] > t_size[0] or o_size[1] > t_size[1]:
        if img.size[0] > img.size[1]:
            t_size[1] = int(round(o_size[1] * t_size[0] / o_size[0]))
        else:
            t_size[0] = int(round(o_size[0] * t_size[1] / o_size[1]))
        img = img.resize(t_size)
    s = StringIO()
    try:
        for y in xrange(0, img.size[1]):
            for x in xrange(0, img.size[0]):
                grey_value = img.getpixel((x, y))
                s.write(convert_list[grey_value] + convert_list[grey_value])
            s.write('\n')
        with open(target + '.txt', 'w') as f:
            s.seek(0)
            f.write(s.read())
    finally:
        s.close()
        # img.save('test.jpg')


def show(content):
    if content == 'help':
        print __help__
    elif content.startswith('err'):
        if content[4:] == 'name':
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
    re_size = re.compile('^[\[]\d+,\d+[\]]$')
    image_path = argv[0]
    target_name = None
    t_size = [500, 500]

    if os.path.isfile(__dir__ + os.sep + image_path):
        image_path = __dir__ + os.sep + image_path
    elif not os.path.isfile(image_path):
        show('err_name')
        return
    argv.extend(['', ''])
    if re_size.match(argv[1]):
        t_size = eval(argv[1])
    elif re_size.match(argv[2]):
        target_name = argv[1]
        t_size = eval(argv[2])
    else:
        target_name = argv[1]

    do_char_convert(image_path, target_name, t_size)


if __name__ == '__main__':
    main()
    # print __dir__
    # print sys.argv
    # get_ascii_pixels()
