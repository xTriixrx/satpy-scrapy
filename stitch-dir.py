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

    bands = []
    dimension = ''
    destination = ''
    band_images = []
    image_range = []
    PATCH_SIZE = 688
    image_name = '20210131180000.jpg'

    try:
        opts, args = getopt.getopt(argv, '', ['destination=', 'dimension='])
        
        for opt, arg in opts:
            if opt == '--destination':
                destination = arg
            elif opt == '--dimension':
                dimension = int(arg)
    except Exception as e:
        print(e)
        sys.exit(1)
    
    if destination == '':
        raise ValueError('Destination argument was not provided and should not be \'\'.')
    elif dimension == '':
        raise ValueError('Dimension argument was not provided and should not be \'\' (either 16 or 8).')
    
    flatten_command = 'find ' + destination + ' -mindepth 2 -type f -exec mv \'{}\' ' + destination + ' \;'
    
    os.system(flatten_command)
    
    destination = destination.replace('\"', '')
    for entry in os.scandir('.' + os.sep + destination):
        if os.path.isdir(entry.path) and not os.listdir(entry.path):
            os.rmdir(entry.path)
    
    for i in range(0, dimension):
        bands.append([])
        band_images.append([])
        for j in range(0, dimension):
            if i > 9 and j < 10:
                image_range.append('0' + str(i) + '_00' + str(j) + '.png')
            elif i > 9 and j > 9:
                image_range.append('0' + str(i) + '_0' + str(j) + '.png')
            elif i < 10 and j < 10:
                image_range.append('00' + str(i) + '_00' + str(j) + '.png')
            elif i < 10 and j > 9:
                image_range.append('00' + str(i) + '_0' + str(j) + '.png')
    
    count = 0
    intra_count = 0
    # Build destinations to images for each set of bands
    for img in image_range:
        vals = img.split('_')

        if count < 10:
            if vals[0] == '00' + str(count):
                bands[count].append(destination + os.sep + img)
        else:
            if vals[0] == '0' + str(count):
                bands[count].append(destination + os.sep + img)

        intra_count += 1
        if intra_count == dimension:
            count += 1
            intra_count = 0

    # Open 688x688 images files and store into each respective band_images[i] list.
    for i, band_list in enumerate(bands):
            band_images[i] = [Image.open(im) for im in band_list]

    # Create horizontal bands for each list of images for that row
    for i in range(0, dimension):
        merge_images_horizontally(band_images[i], destination + os.sep + 'band' + str(i) + '.jpg')

    # Create list containing stitched horizontal band images.
    band_horz_images = []
    for i in range(0, dimension):
        band_horz_images.append(Image.open(destination + os.sep + 'band' + str(i) + '.jpg'))

    # Merge all horizontal images vertically to build final image.
    merge_images_vertically(band_horz_images, destination + os.sep + image_name)
    
    print(image_name + ' has been created from sub-image directory ' + destination + ' with resolution ' \
        + str(dimension*PATCH_SIZE) + 'x' + str(dimension*PATCH_SIZE) + '.')

    # Delete all png and band images that built final image.
    rm_png_command = 'rm \"' + destination + '\"' + os.sep + '*.png'
    rm_bands_command = 'rm \"' + destination + '\"' + os.sep + 'band*'
    os.system(rm_png_command)
    os.system(rm_bands_command)

if __name__ == '__main__':
    main(sys.argv[1:])