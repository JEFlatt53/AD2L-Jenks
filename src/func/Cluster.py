import jenkspy

def GetBounds(metric, nDivisions):
    bounds = jenkspy.jenks_breaks(metric, n_classes=nDivisions)
    return bounds
