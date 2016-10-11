#
# John Smeaton
#
# Script to examine straw strikes which follow scintillator strikes.
# Finds straw strikes immediately following a scintillator strike, with long and short
# upper limits on delay time. Plots delay times, and number of straw strikes within this
# time.
#

import ROOT

class StrawHitCluster:

    # Class for cluster of straw hits

    def __init__(self, runNum, eventNum):

        # Get run number, event number. Set up list of event times 
        self.runNum = runNum
        self.eventNum = eventNum
        self.hitTimes = []

    # Append hit time for straw to list
    def addStraw(self, hitTime):
        self.hitTimes.append(hitTime)

    # Return number of hit straws in cluster
    def getStrawCount(self):
        return len(self.hitTimes)
    
    # Return list of hit times
    def getHitTimes(self):
        return self.hitTimes



class ScintStrike:

    # Class for strike of scintillator (either one)

    def __init__(self, runNum, eventNum, hitTime):

        # Get run number, event number, and hit time for strikes. Sets up containters for
        # straw hits coinciding with scintillator hits, with both long and short cut in time delay
        self.runNum = runNum
        self.eventNum = eventNum
        self.hitTime = hitTime
        self.strawClusterLongCut = StrawHitCluster(self.runNum, self.eventNum)
        self.strawClusterShortCut = StrawHitCluster(self.runNum, self.eventNum)
    
    # Returns run number for strike
    def getRun(self):
        return self.runNum

    # Returns event number for strike
    def getEvent(self):
        return self.eventNum

    # Returns hit time
    def getHitTime(self):
        return self.hitTime

    # Returns collection of straw hits with long delay cut
    def getStrawHitClusterLongCut(self):
        return self.strawClusterLongCut

    # Returns collection of straw hits with short delay cut
    def getStrawHitClusterShortCut(self):
        return self.strawClusterShortCut


class ScintStrikeCollection:

    # Class for collection of scintillator strikes

    def __init__(self):
        # Sets up dictionary for strikes
        self.scintStrikeDict = dict()

    def addStrike(self, scintStrike):

        # Gets key for scintillator strike, from run number and event number
        key = str(scintStrike.getRun()) + '-' + str(scintStrike.getEvent())

        # If already strike for this event and run, append strike to list found with key
        if key in self.scintStrikeDict:
            self.scintStrikeDict[key].append(scintStrike)

        # If no strike for event and run, create list of strikes for key
        else:
            self.scintStrikeDict[key] = [scintStrike]


    def getStrikes(self, run, event):

        key = str(run) + '-' + str(event) # Generate key from run, event numbers

        # If key in dictionary, return list of strikes, else return empty list
        if key in self.scintStrikeDict:
            return self.scintStrikeDict[key]
        else:
            return []

    # Returns dictionary of strikes
    def getDict(self):
        return self.scintStrikeDict

#################################################################################
    


# Get input file
f = ROOT.TFile.Open("Lab3TreeDumper_00695_00696_00697_00698_00699_00702_00706_00707_00708.root", "read")

# Get tree of straw and scintillator strikes
strawTree = f.Get("professorTreeDumper/strawHits")
scintTree = f.Get("professorTreeDumper/scintHits")

# Create collection of scintillator strikes
scintStrikeCollection = ScintStrikeCollection()

# Delay time cut for coincidences between scintillator and straw strikes, in ns
shortCutTime = 75
longCutTime = 500

print ""
print "Iterating Across Scintillator Tree"

# Loop across all entries in tree
for i in xrange(100000):

    # To show progress
    if (i % 50000) == 0:
        print i

    scintTree.GetEntry(i) # Get entry from tree

    # Get current values for strike
    currentEvent = scintTree.Event
    currentRun = scintTree.Run
    currentWire = scintTree.Wire
    currentHitTime = scintTree.HitTime

    # Create object for strike, and 
    foundStrike = ScintStrike(currentRun, currentEvent, currentHitTime)
    scintStrikeCollection.addStrike(foundStrike)



print ""
print "Iterating Across Straw Tree:"

# Loop across all entries in tree
for i in xrange(500000):
    
    strawTree.GetEntry(i) # Get entry from tree

    # To show progress
    if (i % 50000 == 0):
        print i

    # Get current values for entry
    currentRun = strawTree.Run
    currentEvent = strawTree.Event
    currentHitTime = strawTree.HitTime

    # Get list of scintillator strikes for event and run
    strikes = scintStrikeCollection.getStrikes(currentRun, currentEvent)

    # Iterate over scintillator strikes for event
    for scintStrike in strikes:
        
        # If straw hit time after scintillator hit time, and before long cut time, add straw to collection for scint hit
        if ((currentHitTime > scintStrike.getHitTime()) & (currentHitTime < scintStrike.getHitTime() + longCutTime)):    
            scintStrike.getStrawHitClusterLongCut().addStraw(currentHitTime)
        
        # Ditto, for short cut time
        if ((currentHitTime > scintStrike.getHitTime()) & (currentHitTime < scintStrike.getHitTime() + shortCutTime)):
            scintStrike.getStrawHitClusterShortCut().addStraw(currentHitTime)


# Filling Histograms

# Histograms for number of straws in clusters, with long and short cut time
hStrawsCoincidingLongCut = ROOT.TH1I("hStrawsCoincidingLongCut", "hStrawsCoincidingLongCut", 10, 0, 10)
hStrawsCoincidingShortCut = ROOT.TH1I("hStrawsCoincidingShortCut", "hStrawsCoincidingShortCut", 10, 0, 10)

# Histograms for delay time for each straw in cluster
hStrawDelayLongCut = ROOT.TH1I("hStrawDelayLongCut", "hStrawDelayLongCut", 50, 0, longCutTime)
hStrawDelayShortCut = ROOT.TH1I("hStrawDelayShortCut", "hStrawDelayShortCut", 50, 0, shortCutTime)

# Get dictionary of scintillator strikes from collection object
strikeDictionary = scintStrikeCollection.getDict()

# Iterate across all keys, then all entries in dictionary of scint strikes            
for key in strikeDictionary:
    for scintStrike in strikeDictionary[key]:
            
        # If collection of straw strikes for scint strikes exists, fill histograms for number of strikes,
        # and delay time, with long cut time
        if (scintStrike.getStrawHitClusterLongCut().getStrawCount() > 0):
            hStrawsCoincidingLongCut.Fill(scintStrike.getStrawHitClusterLongCut().getStrawCount())
            for strawHitTime in scintStrike.getStrawHitClusterLongCut().getHitTimes():
                hStrawDelayLongCut.Fill(strawHitTime - scintStrike.getHitTime())
                
        # Ditto, with short cut time
        if (scintStrike.getStrawHitClusterShortCut().getStrawCount() > 0):
            hStrawsCoincidingShortCut.Fill(scintStrike.getStrawHitClusterShortCut().getStrawCount())
            for strawHitTime in scintStrike.getStrawHitClusterShortCut().getHitTimes():
                hStrawDelayShortCut.Fill(strawHitTime - scintStrike.getHitTime())


    

# Post-processing

# Canvas for number of straw in clusters with long cut times
cStrawsCoincidingLongCut = ROOT.TCanvas("cStrawsCoincidingLongCut", "cStrawsCoincidingLongCut", 2000, 1500)

# Set titles
hStrawsCoincidingLongCut.SetTitle("Straw Hits Less Than" + str(longCutTime) + "ns After Scint Hits")
hStrawsCoincidingLongCut.GetXaxis().SetTitle("Number of Straws Coinciding with Scint Hit")
hStrawsCoincidingLongCut.GetYaxis().SetTitle("Events")

# Draw histogram, then print to pdf
hStrawsCoincidingLongCut.Draw("HIST")
cStrawsCoincidingLongCut.Print("straw_coincidence_long.pdf")


# Canvas for delay times for straw hits, with long cut times
cStrawDelayLongCut = ROOT.TCanvas("cStrawDelayLongCut", "cStrawDelayLongCut", 2000, 1500)

# Set titles
hStrawDelayLongCut.SetTitle("Straw Hits Delay after Scint Hits")
hStrawDelayLongCut.GetXaxis().SetTitle("Delay / ns")
hStrawDelayLongCut.GetYaxis().SetTitle("Events")

# Draw histogram, then print to pdf
hStrawDelayLongCut.Draw("HIST")
cStrawDelayLongCut.Print("straw_delay_long.pdf")




# Canvas for number of straw in clusters with short cut times
cStrawsCoincidingShortCut = ROOT.TCanvas("cStrawsCoincidingShortCut", "cStrawsCoincidingShortCut", 2000, 1500)

# Set titles
hStrawsCoincidingShortCut.SetTitle("Straw Hits Less Than" + str(shortCutTime) + "ns After Scint Hits")
hStrawsCoincidingShortCut.GetXaxis().SetTitle("Number of Straws Coinciding with Scint Hit")
hStrawsCoincidingShortCut.GetYaxis().SetTitle("Events")

# Draw histogram, then print to pdf
hStrawsCoincidingShortCut.Draw("HIST")
cStrawsCoincidingShortCut.Print("straw_coincidence_short.pdf")


# Canvas for delay times for straw hits, with short cut times
cStrawDelayShortCut = ROOT.TCanvas("cStrawDelayShortCut", "cStrawDelayShortCut", 2000, 1500)

# Set titles
hStrawDelayShortCut.SetTitle("Straw Hits Delay after Scint Hits")
hStrawDelayShortCut.GetXaxis().SetTitle("Delay / ns")
hStrawDelayShortCut.GetYaxis().SetTitle("Events")

# Draw histogram, then print to pdf
hStrawDelayShortCut.Draw("HIST")
cStrawDelayShortCut.Print("straw_delay_short.pdf")




# Create output file, then write histograms to it
out_file = ROOT.TFile("scint_straw_coincidence.root", "RECREATE")
hStrawsCoincidingLongCut.Write()
hStrawDelayLongCut.Write()
hStrawsCoincidingShortCut.Write()
hStrawDelayShortCut.Write()
