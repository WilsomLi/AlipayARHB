# -*- coding: utf-8 -*-

from PIL import Image, ImageFilter
import os,sys

position = {
    '750*1335':{'left':205,'top':638,'width':340} # 对应iPhone6的截图图片的 坐标点
}

def handlerImg(path,savepath=''):

    filename=path[path.rfind('/')+1:]
    extension=path[path.rfind('.')+1:]

    #读取图像
    im = Image.open(path)
    w=im.width
    h=im.height

    global position
    pos=position.get(str(w)+'*'+str(h))
    if pos==None:
        pos=position.get('750*1335')

    left=pos['left']
    top=pos['top']
    width=pos['width']
    #从截图中裁出线索图片
    pic=im.crop((left,top,left+width,top+width))


    # 高度偏移值
    # 这些规则完全是从图片中找出来的，不一定完全正确，凭感觉，只是为了提高准确率
    #exc=2;
    #for index in range(0,27):
    #   if index%6==0:
    #        exc=exc+1;
    #   copyandpaste(pic,exc+index*12,width)

    pic2=remove_line(pic)
    if ''==savepath:
        pic2.show()
    else:
        pic2.save(savepath+'/'+filename,extension)

def copyandpaste(pic,start,width):
    destpos=7
    hight=3
    tmp=pic.crop((0,start+(destpos-hight),width,start+destpos))
    pic.paste(tmp,(0,start+destpos,width,start+destpos+hight))
    tmp=pic.crop((0,start+destpos+destpos,width,start+destpos+destpos+destpos-hight))
    pic.paste(tmp,(0,start+destpos+hight,width,start+destpos+destpos))

def remove_line(pic1):
    print '##########remove_line begin'
    pic2 = pic1.copy()
    w, h = pic1.size
    pic1_pix = pic1.load()
    pic2_pix = pic2.load()

#值
    max_variance = 20000
    max_color = 120
    min_color = 20

    black_in_line=False
    black_start_y=0
    black_end_y = 0

    for y in range(0,h):
        x_color_r = 0
        x_color_g = 0
        x_color_b = 0
        for x in range(0,w):
            r,g,b=pic1_pix[x,y]
            x_color_r += r
            x_color_g += g
            x_color_b += b

        r_average = x_color_r / w
        g_average = x_color_g / w
        b_average = x_color_b / w

        r_variance = 0
        g_variance = 0
        b_variance = 0

        for x in range(0,w):
            r,g,b = pic1_pix[x,y]
            r_variance += abs(r_average - r)
            g_variance += abs(g_average - g)
            b_variance += abs(b_average - b)

        sumVariance = r_variance+g_variance+b_variance

        if sumVariance<max_variance and min_color<r_average<max_color and min_color<g_average<max_color and min_color <b_average<max_color:
            #print y,'*********',sumVariance
            if black_in_line==False:
                black_start_y=y-2
                black_in_line=True
                #print 'black_start_y:',y
        else:
            if black_in_line==True:
                black_in_line=False
                black_end_y=y+2
                #print 'black_end_y:',y

                if black_start_y>=0 and black_end_y>black_start_y:
                    average_y=(black_end_y - black_start_y)/2+2
                    print 'from ',black_start_y,' to ',black_end_y
                    #print 'copy_down ',black_start_y,' to ',average_y+black_start_y
                    #print 'copy_up ',black_end_y,' to ',black_end_y-average_y
                    for i in range(0,average_y):
                        for x2 in range(0,w):
                            #pic2_pix[x2,i+black_start_y-1]=pic1_pix[x2,black_start_y-1]
                            y_index=i+black_start_y
                            if y_index>0 and y_index <h:
                                pic2_pix[x2,y_index]=pic1_pix[x2,black_start_y]

                            y_index = black_end_y-i
                            if y_index>0 and y_index < h:
                                pic2_pix[x2,y_index]=pic1_pix[x2,black_end_y]
                            #pic2_pix[x2,black_end_y-i+1]=pic1_pix[x2,black_end_y+1]
                
        

            #black_start_y = 0

    return pic2

def input():
    if (len(sys.argv))<2:
        print '错误：请输入图片路径\npython alipayar.py [filepath]'
        return;
    else:
        path1=sys.argv[1] # 原路径
        if os.path.isdir(path1):
            if len(sys.argv)<3:
                print '错误：请输入两个目录\npython alipayar.py [inputpath] [outputpath]'
                return
            else:
                path2=sys.argv[2] # 输入目录
                for file in os.listdir(path1):
                    path = os.path.join(path1, file).lower()
                    if path.endswith('png'):
                        handlerImg(path,path2)
        else:
            handlerImg(sys.argv[1])

if __name__ == '__main__':
    input()
