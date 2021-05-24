import cv2
import tkinter
import tkinter.ttk
import tkinter.filedialog
import PIL
import PIL.ImageTk
import ctypes
import numpy


class MainWindow(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("IMagic")
        width,height=ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1)
        self.desktopWidth=width
        self.desktopHeight=height
        self.iconbitmap("icons/icon.ico")
        self.geometry(str(self.desktopWidth)+"x"+str(self.desktopHeight)+"+0+0")
        self.state("zoomed")
        self.resizable(0,0)

        #menu part starts here
        self.menuBar=tkinter.Menu(self)
        self.config(menu=self.menuBar)

        #file Menu
        self.fileMenu=tkinter.Menu(self.menuBar,tearoff=0)
        self.fileMenu.add_command(label="New")
        self.fileMenu.add_command(label="Open",command=self._open)
        self.fileMenu.add_command(label="Save",command=self._save)
        self.fileMenu.add_command(label="Save as")
        self.fileMenu.add_command(label="Close")
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit",command=self._exit)

        self.menuBar.add_cascade(label="File",menu=self.fileMenu)

        #edit Menu
        self.editMenu=tkinter.Menu(self.menuBar,tearoff=0)
        self.editMenu.add_command(label="Cut")
        self.editMenu.add_command(label="Copy")
        self.editMenu.add_command(label="Paste")
        self.menuBar.add_cascade(label="Edit",menu=self.editMenu)

        #view Menu
        self.viewMenu=tkinter.Menu(self.menuBar,tearoff=0)
        self.viewMenu.add_command(label="Zoom in")
        self.viewMenu.add_command(label="Zoom out")
        self.menuBar.add_cascade(label="View",menu=self.viewMenu)


        #magnification Menu
        self.magnificationMenu=tkinter.Menu(self.menuBar,tearoff=0)
        self.magnificationMenu.add_command(label="50%")
        self.magnificationMenu.add_command(label="100%")
        self.magnificationMenu.add_command(label="150%")
        self.magnificationMenu.add_command(label="200%")
        self.viewMenu.add_cascade(label="Magnification",menu=self.magnificationMenu)

        #transform Menu
        self.transformMenu=tkinter.Menu(self.menuBar,tearoff=0)
        self.transformMenu.add_command(label="Crop",command=self._crop)
        self.transformMenu.add_command(label="Rotate",command=self._rotate90Right)
        self.transformMenu.add_command(label="Rotate 90\u00B0 right",command=self._rotate90Right)
        self.transformMenu.add_command(label="Rotate 90\u00B0 left",command=self._rotate90Left)
        self.transformMenu.add_command(label="Rotate 180\u00B0",command=self._rotate180)
        self.transformMenu.add_command(label="Flip Horizontal",command=self._flipHorizontal)
        self.transformMenu.add_command(label="Flip Vertical",command=self._flipVertical)
        self.menuBar.add_cascade(label="Transform",menu=self.transformMenu)

        #filter Menu

        self.filterMenu=tkinter.Menu(self.menuBar,tearoff=0)
        self.filterMenu.add_command(label="Mean")
        self.filterMenu.add_command(label="Median")
        self.filterMenu.add_command(label="Fourier Transform")
        self.filterMenu.add_command(label="Gaussian Smoothing")
        self.filterMenu.add_command(label="Unsharp")
        self.filterMenu.add_command(label="Laplacian")
        self.menuBar.add_cascade(label="Filter",menu=self.filterMenu)

        #toolbar
        self.toolBar=tkinter.Frame(self,relief=tkinter.RAISED,bd=1)
        self.toolBar.pack(side=tkinter.TOP,fill=tkinter.X)



        #toolBar buttons
        self.imagePick=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/pick.png"))
        self.toolBarPickButton=tkinter.Button(self.toolBar,image=self.imagePick)
        self.toolBarPickButton.pack(side=tkinter.LEFT,padx=2,pady=2)

        self.imageNew=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/new.png"))
        self.toolBarNewButton=tkinter.Button(self.toolBar,image=self.imageNew)
        self.toolBarNewButton.pack(side=tkinter.LEFT,padx=(15,2),pady=2)

        self.imageOpen=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/open.png"))
        self.toolBarOpenButton=tkinter.Button(self.toolBar,image=self.imageOpen,command=self._open)
        self.toolBarOpenButton.pack(side=tkinter.LEFT,padx=2,pady=2)

        self.imageSave=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/save.png"))
        self.toolBarSaveButton=tkinter.Button(self.toolBar,image=self.imageSave)
        self.toolBarSaveButton.pack(side=tkinter.LEFT,padx=2,pady=2)

        self.imageCut=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/cut.png"))
        self.toolBarCutButton=tkinter.Button(self.toolBar,image=self.imageCut)
        self.toolBarCutButton.pack(side=tkinter.LEFT,padx=(15,2),pady=2)

        self.imageCopy=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/copy.png"))
        self.toolBarCopyButton=tkinter.Button(self.toolBar,image=self.imageCopy)
        self.toolBarCopyButton.pack(side=tkinter.LEFT,padx=2,pady=2)
        
        self.imagePaste=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/paste.png"))
        self.toolBarPasteButton=tkinter.Button(self.toolBar,image=self.imagePaste)
        self.toolBarPasteButton.pack(side=tkinter.LEFT,padx=2,pady=2)

        self.imageBrightness=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/brightness.png"))
        self.toolBarBrightnessButton=tkinter.Button(self.toolBar,image=self.imageBrightness,command=self._brightness)
        self.toolBarBrightnessButton.pack(side=tkinter.LEFT,padx=(15,2),pady=2)

        self.imageContrast=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/contrast.png"))
        self.toolBarContrastButton=tkinter.Button(self.toolBar,image=self.imageContrast,command=self._contrast)
        self.toolBarContrastButton.pack(side=tkinter.LEFT,padx=2,pady=2)

        self.imageCrop=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/crop.png"))
        self.toolBarCropButton=tkinter.Button(self.toolBar,image=self.imageCrop,command=self._crop)
        self.toolBarCropButton.pack(side=tkinter.LEFT,padx=(15,2),pady=2)

        self.imageResize=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/resize.png"))
        self.toolBarResizeButton=tkinter.Button(self.toolBar,image=self.imageResize)
        self.toolBarResizeButton.pack(side=tkinter.LEFT,padx=2,pady=2)

        self.imageRotate90Right=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/rotate90right.png"))
        self.toolBarRotate90RightButton=tkinter.Button(self.toolBar,image=self.imageRotate90Right,command=self._rotate90Right)
        self.toolBarRotate90RightButton.pack(side=tkinter.LEFT,padx=(15,2),pady=2)


        self.imageRotate90Left=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/rotate90left.png"))
        self.toolBarRotate90LeftButton=tkinter.Button(self.toolBar,image=self.imageRotate90Left,command=self._rotate90Left)
        self.toolBarRotate90LeftButton.pack(side=tkinter.LEFT,padx=2,pady=2)


        self.imageRotate180=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/rotate180.png"))
        self.toolBarRotate180Button=tkinter.Button(self.toolBar,image=self.imageRotate180,command=self._rotate180)
        self.toolBarRotate180Button.pack(side=tkinter.LEFT,padx=2,pady=2)


        self.imageFlipHorizontal=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/flipHorizontal.png"))
        self.toolBarFlipHorizontalButton=tkinter.Button(self.toolBar,image=self.imageFlipHorizontal,command=self._flipHorizontal)
        self.toolBarFlipHorizontalButton.pack(side=tkinter.LEFT,padx=2,pady=2)

        self.imageFlipVertical=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/flipVertical.png"))
        self.toolBarFlipVerticalButton=tkinter.Button(self.toolBar,image=self.imageFlipVertical,command=self._flipVertical)
        self.toolBarFlipVerticalButton.pack(side=tkinter.LEFT,padx=2,pady=2)

        self.imageGrayscale=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/grayscale.png"))
        self.toolBarGrayscaleButton=tkinter.Button(self.toolBar,image=self.imageGrayscale,command=self._grayscale)
        self.toolBarGrayscaleButton.pack(side=tkinter.LEFT,padx=(15,2),pady=2)

        self.imagePan=PIL.ImageTk.PhotoImage(PIL.Image.open("icons/pan.png"))
        self.toolBarPanButton=tkinter.Button(self.toolBar,image=self.imagePan)
        self.toolBarPanButton.pack(side=tkinter.LEFT,padx=(15,2),pady=2)


        self.imageContainerFrame=tkinter.Frame(self,bd=1)
        self.imageContainerFrame.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True)

        self.imageCanvas=tkinter.Canvas(self.imageContainerFrame)
        self.imageCanvas.pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=True)       


        self.imageFileName=None
        self.currentImage=None
        self._disableComponent()

    def _disableComponent(self):
        self.toolBarPickButton["state"]="disable"
        self.toolBarNewButton["state"]="disable"
        self.toolBarSaveButton["state"]="disable"
        self.toolBarCutButton["state"]="disable"
        self.toolBarCopyButton["state"]="disable"
        self.toolBarPasteButton["state"]="disable"
        self.toolBarBrightnessButton["state"]="disable"
        self.toolBarContrastButton["state"]="disable"
        self.toolBarCropButton["state"]="disable"
        self.toolBarResizeButton["state"]="disable"
        self.toolBarGrayscaleButton["state"]="disable"
        self.toolBarPanButton["state"]="disable"
        self.toolBarRotate90LeftButton["state"]="disable"
        self.toolBarRotate90RightButton["state"]="disable"
        self.toolBarRotate180Button["state"]="disable"
        self.toolBarFlipHorizontalButton["state"]="disable"
        self.toolBarFlipVerticalButton["state"]="disable"
       



    def _enableComponent(self):
        self.toolBarPickButton["state"]="normal"
        self.toolBarNewButton["state"]="normal"
        self.toolBarSaveButton["state"]="normal"
        self.toolBarCutButton["state"]="normal"
        self.toolBarCopyButton["state"]="normal"
        self.toolBarPasteButton["state"]="normal"
        self.toolBarBrightnessButton["state"]="normal"
        self.toolBarContrastButton["state"]="normal"
        self.toolBarCropButton["state"]="normal"
        self.toolBarResizeButton["state"]="normal"
        self.toolBarGrayscaleButton["state"]="normal"
        self.toolBarPanButton["state"]="normal"
        self.toolBarRotate90LeftButton["state"]="normal"
        self.toolBarRotate90RightButton["state"]="normal"
        self.toolBarRotate180Button["state"]="normal"
        self.toolBarFlipHorizontalButton["state"]="normal"
        self.toolBarFlipVerticalButton["state"]="normal"


    def _exit(self):
        self.quit()
        self.destroy()
        exit()

    def _flipHorizontal(self):
        imageData=cv2.imread(self.imageFileName)
        img=numpy.flip(imageData,0)
        cv2.imwrite(self.imageFileName,img)
        self.image=PIL.Image.open(self.imageFileName)
        self.currentImage=PIL.ImageTk.PhotoImage(self.image)
        self.imageCanvas.create_image(0,0,image=self.currentImage,anchor="nw")


    def _flipVertical(self):
        imageData=cv2.imread(self.imageFileName)
        img=numpy.flip(imageData,1)
        cv2.imwrite(self.imageFileName,img)
        self.image=PIL.Image.open(self.imageFileName)
        self.currentImage=PIL.ImageTk.PhotoImage(self.image)
        self.imageCanvas.create_image(0,0,image=self.currentImage,anchor="nw")




    def _save(self):
        files=[("png file","*.png"),("jpg file","*.jpg"),("jpeg file","*.jpeg")]
        file=tkinter.filedialog.asksaveasfile(filetypes=files,defaultextension=files) 
        print("File Saved:",file)
        self.image.save(str(file)+'.png','PNG')
        print("Saved")


    def _open(self):
        imgfn=tkinter.filedialog.askopenfilename(initialdir=".",filetypes=(("jpg file","*.jpg"),("png file","*.png")))
        if len(imgfn)==0: return
        print("(",imgfn,")")
        self._enableComponent()

        self.imageFileName=imgfn
        self.image=PIL.Image.open(self.imageFileName)
        self.currentImage=PIL.ImageTk.PhotoImage(self.image)
        self.imageCanvas.create_image(0,0,image=self.currentImage,anchor="nw")

    def _rotate90Right(self):
        imageData=cv2.imread(self.imageFileName)

        row=imageData.shape[0]
        column=imageData.shape[1]
        print("row",row)
        print("Column",column)
        newImage=numpy.zeros((column,row,3))
        print(imageData)
        k=row-1
        for r in range(row):
            r1=imageData[r]

            j=0
            for c in range(column):
                newImage[c][k]=r1[j]
        
                j+=1
            k-=1
        cv2.imwrite(self.imageFileName,newImage)
        self.currentImage=PIL.ImageTk.PhotoImage(PIL.Image.open(self.imageFileName))
        self.imageCanvas.create_image(0,0,image=self.currentImage,anchor="nw")


    def _rotate90Left(self):
        imageData=cv2.imread(self.imageFileName)

        row=imageData.shape[0]
        column=imageData.shape[1]
        print("row",row)
        print("Column",column)
        newImage=numpy.zeros((column,row,3))
        print(imageData)
        k=0
        for r in range(row):
            r1=imageData[r]

            j=column-1
            l=0
            for c in range(column):
                newImage[j][r]=r1[l]
                l+=1
                j-=1
            k-=1
        cv2.imwrite(self.imageFileName,newImage)
        self.currentImage=PIL.ImageTk.PhotoImage(PIL.Image.open(self.imageFileName))
        self.imageCanvas.create_image(0,0,image=self.currentImage,anchor="nw")


    def _rotate180(self):
        imageData=cv2.imread(self.imageFileName)

        row=imageData.shape[0]
        column=imageData.shape[1]
        print("row",row)
        print("Column",column)
        newImage=numpy.zeros((row,column,3))
        print(imageData)
        k=row-1
        for r in range(row):
            r1=imageData[r]
    
            j=column-1
            for c in range(column):
                newImage[k][j]=r1[c]
        
                j-=1
            k-=1

        cv2.imwrite(self.imageFileName,newImage)
        self.currentImage=PIL.ImageTk.PhotoImage(PIL.Image.open(self.imageFileName))
        self.imageCanvas.create_image(0,0,image=self.currentImage,anchor="nw")

    def _crop(self):
        self.wm_attributes("-disabled",True)
        print("Ok Crop")
        self.toplevel_dialog=tkinter.Toplevel(self)
        self.toplevel_dialog.minsize(300,100)
        self.toplevel_dialog.geometry("200x200+300+150")
        self.toplevel_dialog.iconbitmap("icons/icon.ico")

        self.toplevel_dialog.transient(self)
        self.toplevel_dialog.protocol("WM_DELETE_WINDOW",self.closeTopLevel)

        self.xLabel=tkinter.Label(master=self.toplevel_dialog,bg='#e75480',width=5,height=1,text="CropX",anchor="nw")
        self.yLabel=tkinter.Label(master=self.toplevel_dialog,bg='#e75480',width=5,height=1,text="CropY",anchor="nw")
        self.widthLabel=tkinter.Label(master=self.toplevel_dialog,bg='#e75480',width=5,height=1,text="Width",anchor="nw")
        self.heightLabel=tkinter.Label(master=self.toplevel_dialog,bg='#e75480',width=5,height=1,text="Height",anchor="nw")

        self.xEntry=tkinter.Entry(master=self.toplevel_dialog,width=15)
        self.yEntry=tkinter.Entry(master=self.toplevel_dialog,width=15)
        self.widthEntry=tkinter.Entry(master=self.toplevel_dialog,width=15)
        self.heightEntry=tkinter.Entry(master=self.toplevel_dialog,width=15)

        lm=20
        self.xLabel.place(x=lm+10,y=10)
        self.xEntry.place(x=lm+100,y=10)

        self.yLabel.place(x=lm+10,y=50)
        self.yEntry.place(x=lm+100,y=50)

        self.widthLabel.place(x=lm+10,y=90)
        self.widthEntry.place(x=lm+100,y=90)

        self.heightLabel.place(x=lm+10,y=130)
        self.heightEntry.place(x=lm+100,y=130)

        self.cropButton=tkinter.Button(self.toplevel_dialog,text="Crop",command=self._cropping)
        self.cropButton.place(x=120,y=165)
    def _cropping(self):
        print("crop starts")
        imageData=cv2.imread(self.imageFileName)


        cropFrom=(int(self.xEntry.get()),int(self.yEntry.get()))
        cropSize=(int(self.widthEntry.get()),int(self.heightEntry.get()))

        c1=cropFrom[0]
        r1=cropFrom[1]


        c2=cropSize[0]-1
        r2=cropSize[1]-1



        if r2>=imageData.shape[0]: r2=imageData.shape[0]-1
        if c2>=imageData.shape[1]: c2=imageData.shape[1]-1
        print("Actual Size",imageData.shape)
        print(cropSize)
        cropSize=(c2-c1+1,r2-r1+1)
        print(cropSize)


        newImage=numpy.zeros((cropSize[1],cropSize[0],3))
        print(newImage.shape)


        rr=0
        r=r1
        while r<=r2:
            cc=0
            c=c1
            while c<=c2:
                newImage[rr][cc]=imageData[r][c]

                cc+=1
                c+=1
            rr+=1
            r+=1      


        cv2.imwrite(self.imageFileName,newImage)
        self.currentImage=PIL.ImageTk.PhotoImage(PIL.Image.open(self.imageFileName))
        self.imageCanvas.create_image(0,0,image=self.currentImage,anchor="nw")

        print("Image Cropped")            
        self.closeTopLevel()

    def _contrast(self):
        print("Contrast")
        self.wm_attributes("-disabled",True)
        self.toplevel_dialog=tkinter.Toplevel(self)
        self.toplevel_dialog.minsize(500,200)
        self.toplevel_dialog.geometry("500x200+300+150")
        self.toplevel_dialog.iconbitmap("icons/icon.ico")

        self.toplevel_dialog.transient(self)
        self.toplevel_dialog.protocol("WM_DELETE_WINDOW",self.closeTopLevel)
        self._job=None        
        #,troughcolor='#000000'
        self.slider=tkinter.Scale(master=self.toplevel_dialog,showvalue=0,bg='#e75480',width=10,length=400,highlightcolor='#000000',from_=-255,to=255,tickinterval=1,orient=tkinter.HORIZONTAL,command=self.onContrastFactorChanged)
        self.slider.set(0)
        self.slider.place(x=10,y=20)
    def onContrastFactorChanged(self,event):
        print("Contrast Factor Changed")
        if self._job:
            self.after_cancel(self._job)
        self._job=self.after(500,self._changeContrast)
    


    def _changeContrast(self):
        self._job=None
        print("new Value:",self.slider.get())


        imageData=cv2.imread(self.imageFileName)
        contrast=self.slider.get()
        f=(259*(contrast+255))/(255*(259-contrast))
        for r in range(imageData.shape[0]):
            for c in range(imageData.shape[1]):
                rgb=imageData[r][c]
                red=rgb[0]
                green=rgb[1]
                blue=rgb[2]
                newRed=f*(red-128)
                newGreen=f*(green-128)
                newBlue=f*(blue-128)                


                if newRed<=0: newRed=0
                if newRed>255: newRed=255

                if newGreen<=0: newGreen=0
                if newGreen>255: newGreen=255
                if newBlue<=0: newBlue=0
                if newBlue>255: newBlue=255

                imageData[r][c]=(red,green,blue)
        cv2.imwrite(self.imageFileName,imageData)
        self.currentImage=PIL.ImageTk.PhotoImage(PIL.Image.open(self.imageFileName))
        self.imageCanvas.create_image(0,0,image=self.currentImage,anchor="nw")

        print("Contrast Task Done")            
        self.closeTopLevel()





    def _brightness(self):
        print("Change Brightness")
        self.wm_attributes("-disabled",True)
        self.toplevel_dialog=tkinter.Toplevel(self)
        self.toplevel_dialog.minsize(500,200)
        self.toplevel_dialog.geometry("500x200+300+150")
        self.toplevel_dialog.iconbitmap("icons/icon.ico")

        self.toplevel_dialog.transient(self)
        self.toplevel_dialog.protocol("WM_DELETE_WINDOW",self.closeTopLevel)
        self._job=None        
        #,troughcolor='#000000'
        self.slider=tkinter.Scale(master=self.toplevel_dialog,showvalue=0,bg='#e75480',bd=-1,width=10,length=400,highlightcolor='#000000',from_=-255,to=255,tickinterval=1,orient=tkinter.HORIZONTAL,command=self.onBrightnessFactorChanged)
        self.slider.set(0)
        self.slider.place(x=10,y=20)
    def onBrightnessFactorChanged(self,event):
        print("Update Value Chala")
        if self._job:
            self.after_cancel(self._job)
        self._job=self.after(500,self._changeBrightness)

    def _changeBrightness(self):
        self._job=None
        print("new Value:",self.slider.get())


        imageData=cv2.imread(self.imageFileName)
        brightness=self.slider.get()
        for r in range(imageData.shape[0]):
            for c in range(imageData.shape[1]):
                rgb=imageData[r][c]
                red=rgb[0]
                green=rgb[1]
                blue=rgb[2]
                red+=brightness
                green+=brightness
                blue+=brightness

                if red<=0: red=0
                if red>255: red=255

                if green<=0: green=0
                if green>255: green=255
                if blue<=0: blue=0
                if blue>255: blue=255

                imageData[r][c]=(red,green,blue)
        cv2.imwrite(self.imageFileName,imageData)
        self.currentImage=PIL.ImageTk.PhotoImage(PIL.Image.open(self.imageFileName))
        self.imageCanvas.create_image(0,0,image=self.currentImage,anchor="nw")

        print("Brightness Task Done")            
        self.closeTopLevel()


    def _grayscale(self):
        print("Grayscale")
        self.wm_attributes("-disabled",True)
        self.toplevel_dialog=tkinter.Toplevel(self)
        self.toplevel_dialog.minsize(300,100)
        self.toplevel_dialog.geometry("300x100+300+150")
        self.toplevel_dialog.iconbitmap("icons/icon.ico")

        self.toplevel_dialog.transient(self)
        self.toplevel_dialog.protocol("WM_DELETE_WINDOW",self.closeTopLevel)
        self._job=None        


        n=tkinter.StringVar(self)
        n.set("Select method")
        self.methodCombobox=tkinter.ttk.Combobox(self.toplevel_dialog,width=25,values=('Select a method','Average Method','Maximum Method','Minimum Method','Luminosity Method','All Four Methods'))
        #self.methodCombobox.grid(row=2,column=3)
        self.methodCombobox.current(0)
        self.methodCombobox.place(x=30,y=20)

        self.convertButton=tkinter.ttk.Button(self.toplevel_dialog,text="Convert",command=self.onClickToConvertButton)
        self.convertButton.place(x=40,y=50,anchor="nw")


    def onClickToConvertButton(self):
        print("Convert to grayscale",self.imageFileName)

        imageData=cv2.imread(self.imageFileName)
        for r in range(imageData.shape[0]):
            for c in range(imageData.shape[1]):
                rgb=imageData[r][c]
                red=int(rgb[0])
                green=int(rgb[1])
                blue=int(rgb[2])
                avg=int((red+green+blue)/3)
                imageData[r][c]=(avg,avg,avg)
        cv2.imwrite(self.imageFileName,imageData)
        self.currentImage=PIL.ImageTk.PhotoImage(PIL.Image.open(self.imageFileName))
        self.imageCanvas.create_image(0,0,image=self.currentImage,anchor="nw")

        print("Grayscale Task Done")            
        self.closeTopLevel()

        


    def closeTopLevel(self):
        self.wm_attributes("-disabled",False)
        self.toplevel_dialog.destroy()
        self.deiconify()
            

mainWindow=MainWindow()
mainWindow.mainloop()