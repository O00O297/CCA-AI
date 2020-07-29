class LoadImages:
    folder_id = ""
    url = ""
    slide_id = ""
    MAG = 40
    image_size = 0
    api_Key = ""
    image_path = ""

    def __init__(self, url, slide_id, MAG, image_size, api_Key, folder_id, image_path):
        self.url = url
        self.slide_id = slide_id
        self.MAG = MAG
        self.image_size = image_size
        self.api_Key = api_Key
        self.folder_id = folder_id
        self.image_path = image_path

    def LoadImage(self):
        gc = girder_client.GirderClient(apiUrl=self.url)
        gc.authenticate(apiKey=self.api_Key)
        slide_metadata = gc.get("/item/%s/tiles" % (self.slide_id))
        row = int(slide_metadata["sizeY"]*(self.MAG/40)/self.image_size)
        col = int(slide_metadata["sizeX"]*(self.MAG/40)/self.image_size)
        for x in range(row):
            for y in range(col):
                get_Rest_url = "/item/%s/tiles/region?left=%d&right=%d&top=%d&bottom=%d&units=mag_pixels" % (self.slide_id, y*self.image_size, (y*self.image_size)+(self.image_size-1), x*self.image_size, (x*self.image_size)+(self.image_size-1)) + "&magnification=%d" % self.MAG +"&encoding=TIFF&tiffCompression=tiff_lzw"
                image_tile = get_image_from_htk_response(gc.get(get_Rest_url, jsonResp=False))
                image_tile = cv2.cvtColor(image_tile, cv2.COLOR_RGB2BGR)
                image_name = dir_Name + "-" + str(x) + "_" + str(y) + ".tiff"
                status = threshold(image_tile,self.image_size)
                if status:
                    cv2.imwrite(path+image_name, image_tile)

     def threshold(image,image_size):
         img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
         ret, thresh1 = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY)
         no_BPixel = sum(sum(1 - (thresh1 / 255)))
         check = (image_size * image_size) / 5
         if no_BPixel > check:
             return True
         else:
             return False