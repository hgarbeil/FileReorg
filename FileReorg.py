import os
import re
import sys
import shutil


class FileReorg :
    def __init__(self):
        self.numCrysts = 0
        self.dsetName = ''

        # edit below to change input directory...
        #self.mainSource = os.path.normpath('c:/Users/gregf/Dropbox (UH Mineral Physics)/Hawaii_Data/oamph_gedrite/')
        self.mainSource = os.path.normpath ('/Users/hg/workdir/python_rename/P5_copy')




        # get the list of all tif files in the directory
        self.allFiles = os.listdir (self.mainSource)
        self.imgFiles = [f for f in os.listdir(self.mainSource) if f.endswith('.tif')]
        self.miscFiles = [f for f in os.listdir(self.mainSource) if f.endswith('.tif.txt')]
        print 'Number of files in directory is : ', len (self.allFiles)
        print 'Number of imageFiles in directory is : ', len(self.imgFiles)
        print 'Number of text files in directory is : ', len (self.miscFiles)


    ###
    # countCrystals - class member to go through dataset and identify each unique crystal and create a subdirectory for each
    ###
    def countCrystals (self) :
        self.crystName=[]

        # look for unique crystal identifiers and append to crystName list
        for f in self.imgFiles :
            sp = re.split("_", f)
            if not sp[2] in self.crystName :
                self.crystName.append(sp[2])



        print self.crystName
        self.numCrysts = len (self.crystName)
        self.dsetName = sp[0]
        print "Number of crystals in directory is : ", len (self.crystName)
        if self.numCrysts == 0 :
            return
        # create directories
        for c in self.crystName :
            outDir = os.path.normpath(self.mainSource + '/' + c)
            if not os.path.exists(outDir) :
                os.makedirs (outDir)
                print "Making : ", outDir
            else :
                print "Directory exists : ", outDir

    ###
    # moveMiscFiles - class member which moves files other then tif files and moves them to the misc subdirectory
    ###
    def moveMiscFiles (self) :
        outDir = os.path.normpath (self.mainSource + '/misc')
        # make the misc directory if necessary
        if not os.path.exists (outDir) :
            os.makedirs (outDir)
            print "Making : ", outDir
        # then move all files (not tifs) to misc directory
        for f in  self.allFiles :

            if f.endswith (".tif") :
                continue

            infile = os.path.normpath(self.mainSource + '/' + f)
            # also check if its a directory, if so skip
            if os.path.isdir (infile) :
                continue
            outfile = os.path.normpath(outDir+ '/' + f)
            # replace shutil.copy with shutil.move to delete original
            shutil.copy (infile, outfile)


    ###
    # moveFiles - class member which goes through the list of tif files, creating directories for D1s, D1w, etc... and then
    #   copying or moving the original file to the correct directory with the .mccd suffix. Note that this method only copies or
    #   moves tiff files
    ###
    def moveFiles (self) :
        numViews = 0

        for icryst in range (self.numCrysts) :
            #list of available types (D1s,D1w,D2w,etc..)
            acqTypes = []

            cid = self.crystName[icryst]
            subname = os.path.normpath(self.mainSource+'/')+'/*'+cid+'*.tif'
            outDir = self.mainSource+ '/' + cid
            print "Copying files to  : ", outDir
            imgFiles = [f for f in os.listdir(self.mainSource) if f.endswith('.tif')]

            # go through list of files - check for crystal type, then create view directory if that does not exist
            for f in imgFiles :

                substrs = re.split("_",f)
                crystDir = substrs[2]

                # if file not of crystal we are searching for, skip it
                if not crystDir  == cid :
                    continue
                #get D1s, D1w, or D2w
                aType = substrs[3]
                #get the sequence number of the file from the name
                seqNumber = substrs[4]
                seqNumber = int(seqNumber[:-4])

                #make the subdirectory for aType if it does not exist
                if not aType in acqTypes :
                    acqTypes.append (aType)
                    outDir = self.mainSource+'/'+cid+'/'+aType
                    if not os.path.exists(outDir) :
                        os.makedirs (outDir)
                # build the input and output file for the copy step
                aTypeIndex = acqTypes.index(aType) + 1
                #shutil.copy (name, outDir)
                infile = os.path.normpath(self.mainSource + '/' + f)

                #make the strings for the copy or move input and output files
                newfile = "%s_%02d_%04d.mccd"%(self.dsetName, aTypeIndex, seqNumber)
                outfile =  os.path.normpath(self.mainSource + '/' + cid + '/' + aType + '/' + newfile)
                print "renaming : " + infile + "  \n\tto : " + outfile

                ### replace shutil.copy with shutil.move for a move rather than a copy (deletes orig file)
                shutil.copy (infile, outfile)




freorg = FileReorg()
freorg.countCrystals()
freorg.moveFiles()
freorg.moveMiscFiles ()
