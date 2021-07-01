import re

# create a synapse class to hold data for each synapse
class ESynapse:

    # initialize a blank synapse
    def __init__(self, dNum, cNum, axeNum): 
        self.dNum = dNum
        self.cNum = cNum
        self.axeNum = axeNum
        self.cfa = 0
        self.ssvr = 0
        self.ssvd = 0
        self.mito = []
        self.MSB_names = []
        self.MSB_cfa = []
        self.MSB_ssvd = []
        self.gContact = "none"

    # return name as string
    def __str__(self):
        return "d" + self.dNum + "c" + self.cNum.upper() + "axe" + self.axeNum

    # add a mito volume to existing list
    def addMito(self, mito):
        self.mito.append(mito)

    # add MSB flat area to existing list
    def addMSB(self, name, cfa, ssvd):
        self.MSB_names.append(name)
        self.MSB_cfa.append(cfa)
        self.MSB_ssvd.append(ssvd)

    # add glia contact to existing string
    def addGContact(self, contact):
        if self.gContact == "none":
            self.gContact = contact
        elif self.gContact == "pre" and contact == "post":
            self.gContact = "prepost"
        elif self.gContact == "post" and contact == "pre":
            self.gContact = "prepost"

# list of synapses with extra functions for searching and writing to a file
class Dendrite:

    # initialize synapse list
    def __init__(self, name):
        self.name = name
        self.synapses = []

    # print list of synapse names
    def __str__(self):
        s = ""
        for synapse in self.synapses:
            s += str(synapse) + "\n"
        return s

    # add a synapse
    def add(self, synapse):
        self.synapses.append(synapse)

    # search for a synapse in the list by cNum
    def findCNum(self, cNum):
        for synapse in self.synapses:
            if synapse.cNum == cNum.lower():
                return synapse
        return None

    # search for a synapse by axeNum
    # this is not used in the program, but is kept here for any future use
    def findAxeNum(self, axeNum):
        synList = []
        for synapse in self.synapses:
            if synapse.axeNum == axeNum:
                synList.append(synapse)
        return synList

    # if any synapses are completely blank, remove them
    def removeBlanks(self):
        for synapse in self.synapses:
            if synapse.ssvr == 0 and synapse.ssvd == 0 and len(synapse.mito) == 0 and len(synapse.MSB_names) == 0 and synapse.gContact == "none":
                self.synapses.remove(synapse)

    # write the dendrite data to a file
    def writeData(self, fileName):

        # check if the file is empty/not created yet
        # if so, then the titles will need to be written
        try:
            file = open(fileName, "r")
            if not file.readlines():
                writeTitles = True
            else:
                writeTitles = False
            file.close()
        except:
            writeTitles = True

        # open the file and write titles if needed
        file = open(fileName, "a")
        if writeTitles:
            file.write("name," +
                       "cfa," +
                       "ssvd," +
                       "ssvr," +
                       "mito," +
                       "mito1," +
                       "mito2," +
                       "mito3," +
                       "total_mito_volume," +
                       "MSB," +
                       "MSB1_name," +
                       "MSB1_cfa," +
                       "MSB1_ssvd," +
                       "MSB2_name," +
                       "MSB2_cfa," +
                       "MSB2_ssvd," +
                       "MSB3_name," +
                       "MSB3_cfa," +
                       "MSB3_ssvd," +
                       "total_bouton_synapse_area,"
                       "glia_contact\n")

        # add all of the synapse data line by line
        for synapse in self.synapses:
            file.write(str(synapse) + "," +
                       str(synapse.cfa) + "," +
                       str(synapse.ssvd) + "," +
                       str(synapse.ssvr) + ",")

            mito_sum = sum(synapse.mito)
            if len(synapse.mito) == 0:
                mito_presence = "n,"
            else:
                mito_presence = "y,"
            if len(synapse.mito) < 3:
                blanks = 3 - len(synapse.mito)
                for i in range(blanks):
                    synapse.mito.append("")
            file.write(mito_presence + str(synapse.mito[0]) + "," + str(synapse.mito[1]) + "," + str(synapse.mito[2]) + ",")
            file.write(str(mito_sum) + ",")

            bouton_sum = sum(synapse.MSB_cfa) + synapse.cfa
            if len(synapse.MSB_names) == 0:
                MSB_presence = "n,"
            else:
                MSB_presence = "y,"
            if len(synapse.MSB_names) < 3:
                blanks = 3 - len(synapse.MSB_names)
                for i in range(blanks):
                    synapse.MSB_names.append("")
                    synapse.MSB_cfa.append("")
                    synapse.MSB_ssvd.append("")
            file.write(MSB_presence +
                       synapse.MSB_names[0] + "," + str(synapse.MSB_cfa[0]) + "," + str(synapse.MSB_ssvd[0]) + "," +
                       synapse.MSB_names[1] + "," + str(synapse.MSB_cfa[1]) + "," + str(synapse.MSB_ssvd[1]) + "," +
                       synapse.MSB_names[2] + "," + str(synapse.MSB_cfa[2]) + "," + str(synapse.MSB_ssvd[2]) + ",")
            file.write(str(bouton_sum) + ",")

            file.write(synapse.gContact + "\n")

        file.close()

# BEGINNING OF MAIN

# catch any exceptions so they can printed for the user
try:

    file = input("What is the name or file path of the CSV file?: ")
    allData = open(file, "r")
    lines = allData.readlines()
    allData.close()
    cont = "y"

    while cont == "y":
        print("What dendrite do you wish to pull excitatory synapse information from?")
        dendriteName = input("(Eg. d07, d013, etc.): ")

        line = ""
        firstLine = True
        
        # create dendrite object
        dendrite = Dendrite(dendriteName)

        for line in lines:

            # skip the first line (titles)
            if firstLine:
                firstLine = False
            else:
                # get each data point in the file
                data = line.split(",")
                name = data[0]
                count = int(data[1])
                flat_area = float(data[2])
                volume = float(data[3])

                # if this is a c-trace ex. d001c01Aaxe001
                if re.search(dendriteName + "c[0-9]+[a-d]?[A-D]?axe[0-9]+$", name):
                    dNum = name[name.find("d")+1 : name.find("c")]
                    cNum = name[name.find("c")+1 : name.find("axe")].lower()
                    axeNum = name[name.find("axe")+3:]
                    dendrite.add(ESynapse(dNum, cNum, axeNum))
                
                # if this is a synapse data point ex. d001c01Aaxe001_mito1
                elif re.search(dendriteName + "c[0-9]+[a-d]?[A-D]?axe[0-9]+_", name):
                    dNum = name[name.find("d")+1 : name.find("c")]
                    cNum = name[name.find("c")+1 : name.find("axe")].lower()
                    axeNum = name[name.find("axe")+3:name.find("_")]
                    extra = name[name.find("_")+1:]
                    if "mito" in extra:
                        dendrite.findCNum(cNum).addMito(volume)
                    elif "ssvr" == extra:
                        dendrite.findCNum(cNum).ssvr = count
                    elif "ssvd" == extra:
                        dendrite.findCNum(cNum).ssvd = count

                # if this is a cfa value trace ex. d001cfa001A
                elif re.search(dendriteName + "cfa", name):
                    splitName = re.split("cfa|axe", name)
                    cNum = splitName[1].lower()
                    if dendrite.findCNum(cNum):
                        dendrite.findCNum(cNum).cfa = flat_area

                # if this is a glia trace ex. d001g01A
                elif re.search(dendriteName + "g[0-9]+[a-d]?[A-D]?_", name):
                    splitName = re.split("g|_", name)
                    cNum = splitName[1].lower()
                    gContact = splitName[2]
                    if dendrite.findCNum(cNum):
                        dendrite.findCNum(cNum).addGContact(gContact)

        # check for MSBs -- any synapse in the entire series that has the same axon number
        for synapse in dendrite.synapses:
            counter = -1

            # iterate through file for every synapse in the dendrite
            for line in lines:
                counter += 1
                if counter != 0:
                    
                    # get data from line (only need name and flat area)
                    data = line.split(",")
                    name = data[0]
                    flat_area = float(data[2])

                    # look for any c-trace that contains the same axon number
                    if re.search("d[0-9]+c[0-9]+[a-d]?[A-D]?axe" + str(synapse.axeNum) + "$", name) and name != str(synapse):
                        dNum = name[name.find("d")+1 : name.find("c")]
                        cNum = name[name.find("c")+1 : name.find("axe")].lower()
                        axeNum = name[name.find("axe")+3:]

                        # ask the user if the synapses or in the same bouton
                        response = input("Are " + str(synapse) + " and " + name + " in the same bouton? (y/n): ")
                        while response != "y" and response != "n":
                            response = input("Please enter a valid answer. (y/n):")
                        if response == "y":
                            
                            # iterate through file to find cfa and ssvd for MSB
                            MSB_cfa = 0
                            MSB_ssvd = 0
                            for l in lines:
                                if re.search("d" + dNum + "cfa" + cNum + "(axe" + synapse.axeNum + ")?$", l.split(",")[0].lower()):
                                    MSB_cfa = float(l.split(",")[2])
                                elif re.search("d" + dNum + "c" + cNum + "(axe" + synapse.axeNum + ")?_ssvd$", l.split(",")[0].lower()):
                                    MSB_ssvd = int(l.split(",")[1])
                            synapse.addMSB(name, MSB_cfa, MSB_ssvd)

        # remove blank synapses (possible if c-trace was renamed but no data were added
        dendrite.removeBlanks()
        
        # add the data to a new file
        newFileName = input("What is the file name and/or file path for adding this data?: ")
        dendrite.writeData(newFileName)

        cont = input("\nWould you like to get more dendrite data from this file? (y/n): ")

except Exception as e:
    print("ERROR: " + str(e))

input("Press enter to exit.")
