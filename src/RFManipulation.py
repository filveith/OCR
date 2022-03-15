import copy
from PIL import Image

IMG_WIDTH = IMG_HEIGHT = 50

def getBinaryImg(img):
    """Return the binary version of an image (Only black and white pixels)

    Args:
        img (Image)

    Returns:
        array: The binary image as a nested array [[0,1,1,...][1,1,1,...]] 
    """
    imagePixels = list(img.getdata())
    binaryImage = []
    width = img.size[0]
    nb = 0
    row = []
    for p in imagePixels:
        nb += 1
        if p == 255 or p == 1:
            row.append(1)
        else:
            row.append(0)   

        if width == nb:
            binaryImage.append(row)
            nb = 0
            row = []

    return binaryImage

def standardize(image):
    image = image.resize((IMG_WIDTH, IMG_HEIGHT))
    imagePixels = list(image.getdata())
    newImage = []

    for p in imagePixels:
    
        if p >= 255/2:
            newImage.append(255)
        else:
            newImage.append(0)       

    img = Image.new(image.mode, image.size)
    img.putdata(newImage) #Unblurred verion of the image
    
    dilatedImg = dilatation(img)
    img = Image.new('1', dilatedImg.size) # Create a new image object because we save it in binary 
    img.putdata(list(dilatedImg.getdata())) #Unblurred + dilated image

    erodedImg = erosion(img)
    img.putdata(list(erodedImg.getdata())) #Unblurred + dilated + eroded image
    
    return img


def dilatation(img):
    imagePixels = getBinaryImg(img)
    newImage = copy.deepcopy(imagePixels)

    for row, val in enumerate(imagePixels):
        for i, p in enumerate(imagePixels[row]):
            if p == 0:
                for x in range(-1,2,1):
                    for y in range(-1,2,1):
                        try:
                            if imagePixels[row+x][i+y] == 1:
                                newImage[row+x][i+y] = 0
                        except:
                            pass
    
    dilatedImg = Image.new('1', img.size)
    newImage_flat = [item for sublist in newImage for item in sublist]
    dilatedImg.putdata(newImage_flat)
    return dilatedImg

def erosion(img):
    """Erode an image

    Args:
        img (Image)
        eroder_size (int, optional): The size of the eroder. Defaults to 3.

    Returns:
        Image: an eroded version of the given image
    """
    imagePixels = getBinaryImg(img)
    newImage = copy.deepcopy(imagePixels)

    for row, val in enumerate(imagePixels):
        for i, p in enumerate(imagePixels[row]):
            if p == 1:
                for x in range(-1,2,1):
                    for y in range(-1,2,1):
                        try:
                            if imagePixels[row+x][i+y] == 0:
                                newImage[row+x][i+y] = 1
                        except:
                            pass
    
    erodedImg = Image.new('1', img.size)
    newImage_flat = [item for sublist in newImage for item in sublist]
    erodedImg.putdata(newImage_flat)
    return erodedImg