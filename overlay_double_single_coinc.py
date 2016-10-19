import ROOT

# Open files for single scint strike, and double
fSingle = ROOT.TFile.Open("scint_straw_coincidence.root", "read")
fDouble = ROOT.TFile.Open("double_scint_straw_coincidence.root", "read")

# Load histograms for number of straws hit
hSingleShortCutCoincidence = fSingle.Get("hStrawsCoincidingShortCut").Clone()
hSingleLongCutCoincidence = fSingle.Get("hStrawsCoincidingLongCut").Clone()
hDoubleShortCutCoincidence = fDouble.Get("hStrawsCoincidingShortCut").Clone()
hDoubleLongCutCoincidence = fDouble.Get("hStrawsCoincidingLongCut").Clone()

# Load histograms for straw hit delays
hDoubleShortCutDelay = fDouble.Get("hStrawDelayShortCut").Clone()
hDoubleLongCutDelay = fDouble.Get("hStrawDelayLongCut").Clone()
hSingleShortCutDelay = fSingle.Get("hStrawDelayShortCut").Clone()
hSingleLongCutDelay = fSingle.Get("hStrawDelayLongCut").Clone()

# Define histograms with double bins (for normalisation)
hSingleShortCutCoincidenceDoub = ROOT.TH1D()
hSingleLongCutCoincidenceDoub = ROOT.TH1D()
hDoubleShortCutCoincidenceDoub = ROOT.TH1D()
hDoubleLongCutCoincidenceDoub = ROOT.TH1D()

hSingleShortCutDelayDoub = ROOT.TH1D()
hSingleLongCutDelayDoub = ROOT.TH1D()
hDoubleShortCutDelayDoub = ROOT.TH1D()
hDoubleLongCutDelayDoub = ROOT.TH1D()

# Copy histograms to double containers 
hSingleShortCutCoincidence.Copy(hSingleShortCutCoincidenceDoub)
hSingleLongCutCoincidence.Copy(hSingleLongCutCoincidenceDoub)
hDoubleShortCutCoincidence.Copy(hDoubleShortCutCoincidenceDoub)
hDoubleLongCutCoincidence.Copy(hDoubleLongCutCoincidenceDoub)

hSingleShortCutDelay.Copy(hSingleShortCutDelayDoub)
hSingleLongCutDelay.Copy(hSingleLongCutDelayDoub)
hDoubleShortCutDelay.Copy(hDoubleShortCutDelayDoub)
hDoubleLongCutDelay.Copy(hDoubleLongCutDelayDoub)


# Normalise histograms
hSingleShortCutCoincidenceDoub.Scale(1.0 / hSingleShortCutCoincidence.Integral())
hSingleLongCutCoincidenceDoub.Scale(1.0 / hSingleLongCutCoincidence.Integral())
hDoubleShortCutCoincidenceDoub.Scale(1.0 / hDoubleShortCutCoincidence.Integral())
hDoubleLongCutCoincidenceDoub.Scale(1.0 / hDoubleLongCutCoincidence.Integral())

hSingleShortCutDelayDoub.Scale(1.0 / hSingleShortCutDelay.GetBinContent(hSingleShortCutDelay.GetMaximumBin()))
hSingleLongCutDelayDoub.Scale(1.0 / hSingleLongCutDelay.GetBinContent(hSingleLongCutDelay.GetMaximumBin()))
hDoubleShortCutDelayDoub.Scale(1.0 / hDoubleShortCutDelay.GetBinContent(hDoubleShortCutDelay.GetMaximumBin()))
hDoubleLongCutDelayDoub.Scale(1.0 / hDoubleLongCutDelay.GetBinContent(hDoubleLongCutDelay.GetMaximumBin()))


# Create canvases for straw numbers
cSingleStrawsCoinciding = ROOT.TCanvas("cSingleStrawsCoinciding", "cSingleStrawsCoinciding", 2000, 1500)
cDoubleStrawsCoinciding = ROOT.TCanvas("cDoubleStrawsCoinciding", "cDoubleStrawsCoinciding", 2000, 1500)

# Create canvases for straw delays, with long and short cuts
cStrawDelayLong = ROOT.TCanvas("cStrawDelayLong", "cStrawDelayLong", 2000, 1500)
cStrawDelayShort = ROOT.TCanvas("cStrawDelayShort", "cStrawDelayShort", 2000, 1500)

# Remove stats boxes from histograms
hSingleShortCutCoincidenceDoub.SetStats(0)
hSingleLongCutCoincidenceDoub.SetStats(0)
hDoubleShortCutCoincidenceDoub.SetStats(0)
hDoubleLongCutCoincidenceDoub.SetStats(0)

hSingleShortCutDelayDoub.SetStats(0)
hSingleLongCutDelayDoub.SetStats(0)
hDoubleShortCutDelayDoub.SetStats(0)
hDoubleLongCutDelayDoub.SetStats(0)


hSingleShortCutDelayDoub.SetMinimum(0)
hSingleLongCutDelayDoub.SetMinimum(0)
hDoubleShortCutDelayDoub.SetMinimum(0)
hDoubleLongCutDelayDoub.SetMinimum(0)



# HIT NUMBERS PLOT DRAWING

# Set histogram titles, for coincidence number plots
hSingleShortCutCoincidenceDoub.SetTitle("Straw Hits After Scint Hits (Single Scint Hit)")
hSingleLongCutCoincidenceDoub.SetTitle("Straw Hits After Scint Hits (Single Scint Hit)")
hDoubleShortCutCoincidenceDoub.SetTitle("Straw Hits After Scint Hits (Two Coinciding Scint Hits)")
hDoubleLongCutCoincidenceDoub.SetTitle("Straw Hits After Scint Hits (Two Coinciding Scint Hits)")

# Set axis titles, line colours
hSingleShortCutCoincidenceDoub.GetXaxis().SetTitle("Number of Straw Hits")
hSingleShortCutCoincidenceDoub.GetYaxis().SetTitle("Proportion of Coincidence Events")
hSingleShortCutCoincidenceDoub.SetLineColor(4)

hSingleLongCutCoincidenceDoub.GetXaxis().SetTitle("Number of Straw Hits")
hSingleLongCutCoincidenceDoub.GetYaxis().SetTitle("Proportion of Coincidence Events")
hSingleLongCutCoincidenceDoub.SetLineColor(2)

hDoubleShortCutCoincidenceDoub.GetXaxis().SetTitle("Number of Straw Hits")
hDoubleShortCutCoincidenceDoub.GetYaxis().SetTitle("Proportion of Coincidence Events")
hDoubleShortCutCoincidenceDoub.SetLineColor(4)

hDoubleLongCutCoincidenceDoub.GetXaxis().SetTitle("Number of Straw Hits")
hDoubleLongCutCoincidenceDoub.GetYaxis().SetTitle("Proportion of Coincidence Events")
hDoubleLongCutCoincidenceDoub.SetLineColor(2)

# Draw histograms to canvas
cSingleStrawsCoinciding.cd()
hSingleShortCutCoincidenceDoub.Draw("HIST")
hSingleLongCutCoincidenceDoub.Draw("HIST SAME")

cDoubleStrawsCoinciding.cd()
hDoubleShortCutCoincidenceDoub.Draw("HIST")
hDoubleLongCutCoincidenceDoub.Draw("HIST SAME")

# Set up, draw legends
cSingleStrawsCoinciding.cd()
single_leg = ROOT.TLegend(0.7,0.7,0.9,0.9);
single_leg.SetHeader("Delay Cut Time / ns")
single_leg.AddEntry(hSingleShortCutCoincidenceDoub, "75 ns", "l")
single_leg.AddEntry(hSingleLongCutCoincidenceDoub, "500 ns", "l")
single_leg.Draw()

cDoubleStrawsCoinciding.cd()
double_leg = ROOT.TLegend(0.7,0.7,0.9,0.9);
double_leg.SetHeader("Delay Cut Time / ns")
double_leg.AddEntry(hDoubleShortCutCoincidenceDoub, "75 ns", "l")
double_leg.AddEntry(hDoubleLongCutCoincidenceDoub, "500 ns", "l")
double_leg.Draw()

# Print to pdf
cSingleStrawsCoinciding.Print("single_straw_coincidence_overlay.pdf")
cDoubleStrawsCoinciding.Print("double_straw_coincidence_overlay.pdf")


# STRAW DELAY PLOT DRAWING

# Set plot titles
hSingleShortCutDelayDoub.SetTitle("Straw Hit Delay Time (Short Time Cut)")
hSingleLongCutDelayDoub.SetTitle("Straw Hit Delay Time (Long Time Cut)")
hDoubleShortCutDelayDoub.SetTitle("Straw Hit Delay Time (Short Time Cut)")
hDoubleLongCutDelayDoub.SetTitle("Straw Hit Delay Time (Long Time Cut)")

# Set axis titles, line colours
hSingleShortCutDelayDoub.GetXaxis().SetTitle("Delay Time")
hSingleShortCutDelayDoub.GetYaxis().SetTitle("Events")
hSingleShortCutDelayDoub.SetLineColor(4)

hSingleLongCutDelayDoub.GetXaxis().SetTitle("Delay Time")
hSingleLongCutDelayDoub.GetYaxis().SetTitle("Events")
hSingleLongCutDelayDoub.SetLineColor(4)

hDoubleShortCutDelayDoub.GetXaxis().SetTitle("Delay Time")
hDoubleShortCutDelayDoub.GetYaxis().SetTitle("Events")
hDoubleShortCutDelayDoub.SetLineColor(2)

hDoubleLongCutDelayDoub.GetXaxis().SetTitle("Delay Time")
hDoubleLongCutDelayDoub.GetYaxis().SetTitle("Events")
hDoubleLongCutDelayDoub.SetLineColor(2)

# Draw histograms to canvases
cStrawDelayLong.cd()
hSingleLongCutDelayDoub.Draw("HIST")
hDoubleLongCutDelayDoub.Draw("HIST SAME")

cStrawDelayShort.cd()
hSingleShortCutDelayDoub.Draw("HIST")
hDoubleShortCutDelayDoub.Draw("HIST SAME")

# Set up, draw legends
cStrawDelayLong.cd()
long_leg = ROOT.TLegend(0.7,0.7,0.9,0.9);
long_leg.SetHeader("Scint Hits")
long_leg.AddEntry(hSingleLongCutDelayDoub, "1", "l")
long_leg.AddEntry(hDoubleLongCutDelayDoub, "2", "l")
long_leg.Draw()

cStrawDelayShort.cd()
short_leg = ROOT.TLegend(0.7,0.7,0.9,0.9);
short_leg.SetHeader("Scint Hits")
short_leg.AddEntry(hSingleShortCutDelayDoub, "1", "l")
short_leg.AddEntry(hDoubleShortCutDelayDoub, "2", "l")
short_leg.Draw()

# Print to pdf
cStrawDelayLong.Print("long_delay_overlay.pdf")
cStrawDelayShort.Print("short_delay_overlay.pdf")
