#
# John Smeaton
#
# Script to examine scintillator strikes.
# Examines number of times each scintillator struck in each event recording period, outputting 2D histogram
# Finds when one scintillator struck, followed by the other. Finds the lowest delay time between such hits in
# each recording period, and graphs this delay time, with one plot for large time range, and one for short
# time range.
#


import ROOT

# Get input file
f = ROOT.TFile.Open("Lab3TreeDumper_00695_00696_00697_00698_00699_00702_00706_00707_00708.root", "read")

# Get tree of straw and scintillator strikes
strawTree = f.Get("professorTreeDumper/strawHits")
scintTree = f.Get("professorTreeDumper/scintHits")

# Histogram for number of hits for each scintillator
hScintWireHits = ROOT.TH2D("hScintWireHits", "hScintWireHits", 15, 0, 15, 15, 0, 15)
hScintWireHits.SetStats(0)

# Histograms for delay times between scintillator hits, with and without 100ns cut.
hTimeOffsets = ROOT.TH1D("hTimeOffsets", "hTimeOffsets", 100, 0, 100)
hTimeOffsetsNocut = ROOT.TH1D("hTimeOffsetsNocut", "hTimeOffsetsNocut", 100, 0, 20000000)

# Number of times each scintillator hit in an event
scint0Hits = 0
scint1Hits = 0

eventCount = 0 # Number for event

# Number for scint hit in current and previous entry
previousScintHit = 1000
currentScintHit = 1000

# Hit time for current and previous entry
previousHitTime = 0
currentHitTime = 0

# Run number for current and previous entry
currentRun = 0
previousRun = 0

# List of time differences between hits of each scintillator
delayTimes = []

print scintTree.GetEntries()

# Loop across all entries in tree
for i in xrange(scintTree.GetEntries()):

    # To show progress
    if (i % 50000) == 0:
        print i

    scintTree.GetEntry(i) # Get entry from tree
    
    # Set number of scintillator in previous entry, then get number for current entry
    previousScintHit = currentScintHit
    currentScintHit = scintTree.Wire

    # Set hit time of scintillator in previous entry, then get time for current entry
    previousHitTime = currentHitTime
    currentHitTime = scintTree.HitTime

    previousRun = currentRun
    currentRun = scintTree.Run

    # Check if this entry covers new event
    if (scintTree.Event != eventCount):
        eventCount = scintTree.Event # Get new event number for this entry

        # Check if times between scintillator hits have been recorded for previous event
        if (len(delayTimes) > 0):

            # If minimum offset time recorded is below 100ns, fill relevent histogram
            if (min(delayTimes) < 100):
                hTimeOffsets.Fill(min(delayTimes))

            # Fill histogram with minimum recorded offset time
            hTimeOffsetsNocut.Fill(min(delayTimes))

        # Fill histogram with number of times each scintillator hit in previous event
        hScintWireHits.Fill(scint0Hits, scint1Hits) 
        
        # Reset number of times each scintillator hit, and list of hit time offsets
        scint0Hits = 0
        scint1Hits = 0
        delayTimes = []

    # Check if not new event, but different scintillator struck to last time, and not new run.
    elif ((currentScintHit != previousScintHit) & (currentRun == previousRun)):
             
        # Append difference between hit time for current and previous scintillator hit to list
        delayTimes.append(currentHitTime - previousHitTime)
        
    # Increment counter for number of times given scintillator hit
    if (currentScintHit == 0):
        scint0Hits += 1
    elif (currentScintHit == 1):
        scint1Hits += 1


# Create canvas for histogram of number of times each scintillator hit, then set colours
cScintWireHits = ROOT.TCanvas("cScintWireHits", "cScintWireHits", 2000, 1500)
ROOT.gStyle.SetPalette(53)

# Set titles
hScintWireHits.SetTitle("Events with Given Number of Strikes on Each Scintillator")
hScintWireHits.GetXaxis().SetTitle("Scintillator 0 Strikes")
hScintWireHits.GetYaxis().SetTitle("Scintillator 1 Strikes")

# Draw histogram with colours, and output to pdf
hScintWireHits.Draw("colz")
cScintWireHits.Print("scint_wire_hits.pdf")

# Create canvas for hit time offsets histogram
cTimeOffsets = ROOT.TCanvas("cTimeOffsets", "cTimeOffsets", 2000, 1500)

# Set titles
hTimeOffsets.SetTitle("Scintillator Hit Time Offsets Below 100ns")
hTimeOffsets.GetXaxis().SetTitle("Hit Time Offset / ns")
hTimeOffsets.GetYaxis().SetTitle("Events")

# Draw histogram, then output
hTimeOffsets.Draw("HIST")
cTimeOffsets.Print("time_offsets.pdf")

# Create canvas for hit time offsets histogram without time cut
cTimeOffsetsNocut = ROOT.TCanvas("cTimeOffsetsNocut", "cTimeOffsetsNocut", 2000, 1500)

# Set titles
hTimeOffsetsNocut.SetTitle("Scintillator Hit Time OffsetsNocut Below 100ns")
hTimeOffsetsNocut.GetXaxis().SetTitle("Hit Time Offset / ns")
hTimeOffsetsNocut.GetYaxis().SetTitle("Events")

# Draw historam, then output
hTimeOffsetsNocut.Draw("HIST")
cTimeOffsetsNocut.Print("time_offsets_nocut.pdf")
