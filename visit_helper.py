

def hide(plot_num):
    SetActivePlots(plot_num)
    HideActivePlots()


def save(fname, outdir="C:\\visit"):
    # save file
    SaveWindowAtts = SaveWindowAttributes()
    SaveWindowAtts.outputDirectory = outdir
    SaveWindowAtts.fileName = fname
    SaveWindowAtts.family = 0
    SaveWindowAtts.format = SaveWindowAtts.PNG  # BMP, CURVE, JPEG, OBJ, PNG, POSTSCRIPT, POVRAY, PPM, RGB, STL, TIFF, ULTRA, VTK, PLY, EXR
    SaveWindowAtts.width = 1024
    SaveWindowAtts.height = 1024

    SetSaveWindowAttributes(SaveWindowAtts)
    SaveWindow()


def prep_geometry(geom_path):
    """ load and transform stl file """
    print("Reading geometry")
    # open geometry file
    OpenDatabase(geom_path, 0)

    # transform and scale geometry
    AddPlot("Mesh", "STL_mesh", 1, 1)
    AddOperator("Transform", 1)
    SetActivePlots(0)
    TransformAtts = TransformAttributes()
    TransformAtts.doRotate = 1
    TransformAtts.rotateOrigin = (0, 0, 0)
    TransformAtts.rotateAxis = (0, 0, 1)
    TransformAtts.rotateAmount = -44
    TransformAtts.rotateType = TransformAtts.Deg  # Deg, Rad
    TransformAtts.doScale = 1
    TransformAtts.scaleOrigin = (0, 0, 0)
    TransformAtts.scaleX = 0.1
    TransformAtts.scaleY = 0.1
    TransformAtts.scaleZ = 0.1
    TransformAtts.doTranslate = 1
    TransformAtts.translateX = -50
    TransformAtts.translateY = 700
    TransformAtts.translateZ = 0
    SetOperatorOptions(TransformAtts, 0, 1)


def load_data(fname):
   print("Reading data")
   # open the silo file
   OpenDatabase(fname, 0)


def make_normed_data(name, norm_fac, tnum):
    """ """
    # create the normalised dose rate
    exp_string = str(tnum)+"_mean_000*"+str(norm_fac)
    DefineScalarExpression(name, exp_string)


def add_pseudo(min, max, name):
    """ """
    # add pseudocolor plot
    AddPlot("Pseudocolor", name, 1, 0)
    SetActivePlots(1)
    PseudocolorAtts = PseudocolorAttributes()
    PseudocolorAtts.scaling = PseudocolorAtts.Log  # Linear, Log, Skew
    PseudocolorAtts.minFlag = 1
    PseudocolorAtts.min = min
    PseudocolorAtts.maxFlag = 1
    PseudocolorAtts.max = max
    SetPlotOptions(PseudocolorAtts)


def add_contour(name, con_vals=(3, 10, 100)):
    # add contour plot
    AddPlot("Contour", name, 1, 0)
    SetActivePlots(2)
    ContourAtts = ContourAttributes()
    ContourAtts.SetMultiColor(0, (255, 0, 0, 255))
    ContourAtts.SetMultiColor(1, (255, 0, 255, 255))
    ContourAtts.SetMultiColor(2, (0, 0, 255, 255))
    ContourAtts.contourValue = con_vals
    ContourAtts.contourMethod = ContourAtts.Value  # Level, Value, Percent
    SetPlotOptions(ContourAtts)


def add_slice(axis, intercept):
    # slice geometry
    AddOperator("Slice", 1)
    set_slice(axis, intercept)


def set_slice(axis, intercept):
    SliceAtts = SliceAttributes()
    SliceAtts.originType = SliceAtts.Intercept  # Point, Intercept, Percent, Zone, Node
    SliceAtts.originPoint = (0, 0, 0)
    SliceAtts.originIntercept = intercept
    if axis == 'z':
        SliceAtts.normal = (0, 0, 1)
        SliceAtts.axisType = SliceAtts.ZAxis  # XAxis, YAxis, ZAxis, Arbitrary, ThetaPhi
        SliceAtts.upAxis = (0, 1, 0)
    elif axis == 'y':
        SliceAtts.normal = (0, 1, 0)
        SliceAtts.axisType = SliceAtts.YAxis  # XAxis, YAxis, ZAxis, Arbitrary, ThetaPhi
        SliceAtts.upAxis = (0, 0, 1)
    elif axis == 'x':
        SliceAtts.normal = (1, 0, 0)
        SliceAtts.axisType = SliceAtts.XAxis  # XAxis, YAxis, ZAxis, Arbitrary, ThetaPhi
        SliceAtts.upAxis = (0, 0, 1)
    SliceAtts.meshName = "ADVANTG_mesh"
    SetOperatorOptions(SliceAtts, 0, 1)


def tidy_general_annotations():
    """ """
    # set general annotations remove user name and filename
    AnnotationAtts = AnnotationAttributes()
    AnnotationAtts.userInfoFlag = 0
    AnnotationAtts.databaseInfoFlag = 0
    AnnotationAtts.timeInfoFlag = 0
    AnnotationAtts.legendInfoFlag = 1
    SetAnnotationAttributes(AnnotationAtts)

    # sort out scale labels
    names = GetAnnotationObjectNames()
    for i in names:
        ref = GetAnnotationObject(i)
        ref.drawMinMax = 0
        ref.drawTitle = 0

    # Add title to pseudo color
    ref = GetAnnotationObject(names[1])
    ref.drawTitle = 1


def set_view(axis):
    """ """
    # set the view
    View2DAtts = View2DAttributes()
    if axis == 'z':
        View2DAtts.windowCoords = (0.0, 3000.0, -100.0, 2000.0)
    elif axis == 'y':
        View2DAtts.windowCoords = (0.0, 2500.0, -300.0, 400.0)
    SetView2D(View2DAtts)
