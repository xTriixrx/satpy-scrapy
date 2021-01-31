import os
import sys
import getopt
from PIL import Image

def merge_images_horizontally(imgs, filename):
    """
    This function merges images horizontally.
    """

    #create two lists - one for heights and one for widths
    widths, heights = zip(*(i.size for i in imgs))
    width_of_new_image = sum(widths)
    height_of_new_image = min(heights) #take minimum height
    
    # create new image
    new_im = Image.new('RGB', (width_of_new_image, height_of_new_image))
    
    new_pos = 0
    for im in imgs:
        new_im.paste(im, (new_pos,0))
        new_pos += im.size[0] #position for the next image
    
    new_im.save(filename)


def merge_images_vertically(imgs, filename):
    """
    This function merges images vertically
    """

    #create two lists - one for heights and one for widths
    widths, heights = zip(*(i.size for i in imgs))
    width_of_new_image = min(widths)  #take minimum width
    height_of_new_image = sum(heights)
    
    # create new image
    new_im = Image.new('RGB', (width_of_new_image, height_of_new_image))
    
    new_pos = 0
    for im in imgs:
        new_im.paste(im, (0, new_pos))
        new_pos += im.size[1] #position for the next image
    
    new_im.save(filename)

def main(argv):
    """
    """
    
    band0 = []
    band1 = []
    band2 = []
    band3 = []
    band4 = []
    band5 = []
    band6 = []
    band7 = []
    band8 = []
    band9 = []
    band10 = []
    band11 = []
    band12 = []
    band13 = []
    band14 = []
    band15 = []
    image_range = []

    try:
        destination = ''
        opts, args = getopt.getopt(argv, '', ['destination='])
        print(opts)
        
        for opt, arg in opts:
            if opt == '--destination':
                destination = arg
    except Exception as e:
        print(e)
        sys.exit(1)
    
    if destination == '':
        raise ValueError('Destination argument was not provided and should not be \'\'.')
    
    flatten_command = 'find ' + destination + ' -mindepth 2 -type f -exec mv \'{}\' ' + destination + ' \;'
    print(flatten_command)
    
    #os.system(flatten_command)
    destination = destination.replace('\"', '')
    for entry in os.scandir('.' + os.sep + destination):
        if os.path.isdir(entry.path) and not os.listdir(entry.path):
            os.rmdir(entry.path)
    
    for i in range(0, 16):
        for j in range(0, 16):
            if i > 9 and j < 10:
                image_range.append('0' + str(i) +  '_00' + str(j) + '.png')
            elif i > 9 and j > 9:
                image_range.append('0' + str(i) +  '_0' + str(j) + '.png')
            elif i < 10 and j < 10:
                image_range.append('00' + str(i) +  '_00' + str(j) + '.png')
            elif i < 10 and j > 9:
                image_range.append('00' + str(i) +  '_0' + str(j) + '.png')
    
    for img in image_range:
        vals = img.split('_')

        if vals[0] == '000':
            band0.append(destination + os.sep + img)
        elif vals[0] == '001':
            band1.append(destination + os.sep + img)
        elif vals[0] == '002':
            band2.append(destination + os.sep + img)
        elif vals[0] == '003':
            band3.append(destination + os.sep + img)
        elif vals[0] == '004':
            band4.append(destination + os.sep + img)
        elif vals[0] == '005':
            band5.append(destination + os.sep + img)
        elif vals[0] == '006':
            band6.append(destination + os.sep + img)
        elif vals[0] == '007':
            band7.append(destination + os.sep + img)
        elif vals[0] == '008':
            band8.append(destination + os.sep + img)
        elif vals[0] == '009':
            band9.append(destination + os.sep + img)
        elif vals[0] == '010':
            band10.append(destination + os.sep + img)
        elif vals[0] == '011':
            band11.append(destination + os.sep + img)
        elif vals[0] == '012':
            band12.append(destination + os.sep + img)
        elif vals[0] == '013':
            band13.append(destination + os.sep + img)
        elif vals[0] == '014':
            band14.append(destination + os.sep + img)
        elif vals[0] == '015':
            band15.append(destination + os.sep + img)
        
    #list of images
    print(band0)
    print(band1)
    print(band2)
    print(band3)
    print(band4)
    print(band5)
    print(band6)
    print(band7)
    print(band8)
    print(band9)
    print(band10)
    print(band11)
    print(band12)
    print(band13)
    print(band14)
    print(band15)
    
    # open images files
    band_0_imgs = [Image.open(im) for im in band0]
    band_1_imgs = [Image.open(im) for im in band1]
    band_2_imgs = [Image.open(im) for im in band2]
    band_3_imgs = [Image.open(im) for im in band3]
    band_4_imgs = [Image.open(im) for im in band4]
    band_5_imgs = [Image.open(im) for im in band5]
    band_6_imgs = [Image.open(im) for im in band6]
    band_7_imgs = [Image.open(im) for im in band7]
    band_8_imgs = [Image.open(im) for im in band8]
    band_9_imgs = [Image.open(im) for im in band9]
    band_10_imgs = [Image.open(im) for im in band10]
    band_11_imgs = [Image.open(im) for im in band11]
    band_12_imgs = [Image.open(im) for im in band12]
    band_13_imgs = [Image.open(im) for im in band13]
    band_14_imgs = [Image.open(im) for im in band14]
    band_15_imgs = [Image.open(im) for im in band15]
    
    merge_images_horizontally(band_0_imgs, destination + os.sep + 'band0.jpg')
    merge_images_horizontally(band_1_imgs, destination + os.sep + 'band1.jpg')
    merge_images_horizontally(band_2_imgs, destination + os.sep + 'band2.jpg')
    merge_images_horizontally(band_3_imgs, destination + os.sep + 'band3.jpg')
    merge_images_horizontally(band_4_imgs, destination + os.sep + 'band4.jpg')
    merge_images_horizontally(band_5_imgs, destination + os.sep + 'band5.jpg')
    merge_images_horizontally(band_6_imgs, destination + os.sep + 'band6.jpg')
    merge_images_horizontally(band_7_imgs, destination + os.sep + 'band7.jpg')
    merge_images_horizontally(band_8_imgs, destination + os.sep + 'band8.jpg')
    merge_images_horizontally(band_9_imgs, destination + os.sep + 'band9.jpg')
    merge_images_horizontally(band_10_imgs, destination + os.sep + 'band10.jpg')
    merge_images_horizontally(band_11_imgs, destination + os.sep + 'band11.jpg')
    merge_images_horizontally(band_12_imgs, destination + os.sep + 'band12.jpg')
    merge_images_horizontally(band_13_imgs, destination + os.sep + 'band13.jpg')
    merge_images_horizontally(band_14_imgs, destination + os.sep + 'band14.jpg')
    merge_images_horizontally(band_15_imgs, destination + os.sep + 'band15.jpg')
    
    band0_image = Image.open(destination + os.sep + 'band0.jpg')
    band1_image = Image.open(destination + os.sep + 'band1.jpg')
    band2_image = Image.open(destination + os.sep + 'band2.jpg')
    band3_image = Image.open(destination + os.sep + 'band3.jpg')
    band4_image = Image.open(destination + os.sep + 'band4.jpg')
    band5_image = Image.open(destination + os.sep + 'band5.jpg')
    band6_image = Image.open(destination + os.sep + 'band6.jpg')
    band7_image = Image.open(destination + os.sep + 'band7.jpg')
    band8_image = Image.open(destination + os.sep + 'band8.jpg')
    band9_image = Image.open(destination + os.sep + 'band9.jpg')
    band10_image = Image.open(destination + os.sep + 'band10.jpg')
    band11_image = Image.open(destination + os.sep + 'band11.jpg')
    band12_image = Image.open(destination + os.sep + 'band12.jpg')
    band13_image = Image.open(destination + os.sep + 'band13.jpg')
    band14_image = Image.open(destination + os.sep + 'band14.jpg')
    band15_image = Image.open(destination + os.sep + 'band15.jpg')

    bands = [band0_image, band1_image, band2_image, band3_image, band4_image, band5_image, band6_image, band7_image,
        band8_image, band9_image, band10_image, band11_image, band12_image, band13_image, band14_image, band15_image]
    
    merge_images_vertically(bands, destination + os.sep + '20210131180000.jpg')

    rm_png_command = 'rm \"' + destination + '\"' + os.sep + '*.png'
    rm_bands_command = 'rm \"' + destination + '\"' + os.sep + 'band*'
    
    os.system(rm_png_command)
    os.system(rm_bands_command)

if __name__ == '__main__':
    main(sys.argv[1:])