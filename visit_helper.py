
from visit import *
import glob

def hide(plot_num):
    """ hide a plot """
    SetActivePlots(plot_num)
    HideActivePlots()


def load_data(fname):
    """ lod a database """
    print("Reading data")
    # open the silo file
    OpenDatabase(fname, 0)


def make_normed_data(name, norm_fac, tnum):
    """ create the normalised data """
    exp_string = str(tnum)+"_mean_000*"+str(norm_fac)
    DefineScalarExpression(name, exp_string)


def add_pseudo(min, max, name):
    """ add a pseudocolor plot """
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
    """ add a contour plot """
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
    """ add slice operator """
    AddOperator("Slice", 1)
    set_slice(axis, intercept)


def set_slice(axis, intercept):
    """ set slce attributes, can be used to change slice once added """
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
    """ remove the visit specific annotations"""
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


def set_view(co_ords):
    """  set the 2d view window """
    # set the view
    View2DAtts = View2DAttributes()
    View2DAtts.windowCoords = co_ords
    SetView2D(View2DAtts)


def save(fname):
    """ save image """
    SaveWindowAtts = SaveWindowAttributes()
    SaveWindowAtts.outputDirectory = "."
    SaveWindowAtts.fileName = fname
    SaveWindowAtts.family = 0
    SaveWindowAtts.format = SaveWindowAtts.PNG  # BMP, CURVE, JPEG, OBJ, PNG, POSTSCRIPT, POVRAY, PPM, RGB, STL, TIFF, ULTRA, VTK, PLY, EXR
    SaveWindowAtts.width = 1024
    SaveWindowAtts.height = 1024
    
    SetSaveWindowAttributes(SaveWindowAtts)
    SaveWindow()

   
def read_all_ply_files(ply_path):
    """ read all ply files in a folder """
    print("Reading geometry ply files")
    print(ply_path)
    flist = glob.glob(ply_path)
    print(len(flist))
    
    open_ply_files(flist)

    
def read_ply_file_from_list(ply_path, cell_list):
    """ read all ply files from folder matching cell numbers in a list """
    print("Reading geometry ply files")
    print(ply_path)
    flist = glob.glob(ply_path)
    print(len(flist))
    ply_list = []
    
    cell_list = list(set(cell_list))
    for num in cell_list:
        cpath = ply_path[:-1] + str(num) + ".ply"
        if cpath in flist:
            ply_list.append(cpath)
        else:
            print(num, "Not found")
    
    open_ply_files(ply_list)

    
def open_ply_files(flist):
    """ open 3d ply models """ 
    for f in flist:
        OpenDatabase(f, 0)
        AddPlot("Mesh", "PLY_mesh", 1, 1)
        MeshAtts = MeshAttributes()
        MeshAtts.legendFlag = 0
        SetPlotOptions(MeshAtts)
    print("finished loading ply files")
    
    
def combine_meshes(file1_data, file2_data, norm_fac, exp_name="combined_dose"):
    """ create a combined mesh variable 
        e.g. for combining phton and neutron dose rate meshes
        filex_data should be a list with the path and tally number
    """
    load_data(file1_data[0])
    load_data(file2_data[0])
    
    tnum2 = file2_data[1]
    name2 = str(tnum2) + "_norm"
    make_normed_data(name2, norm_fac, tnum2)
    
    ActivateDatabase(file1_data[0])
    
    tnum1 = file1_data[1]
    name1 = str(tnum1) + "_norm"
    make_normed_data(name1, norm_fac, tnum1)
    
    
    expression_str = "(pos_cmfe(<"+file2_data[0]+":"+name2+">, <ADVANTG_mesh>, 0.000000)+" + name1 +")"
    DefineScalarExpression(exp_name, expression_str)

    
def read_stl(path):
    """ read an stl file """
    OpenDatabase(path, 0)
    AddPlot("Mesh", "STL_mesh", 1, 1)
    MeshAtts = MeshAttributes()
    MeshAtts.legendFlag = 0
    SetPlotOptions(MeshAtts)
    print("finished loading Stl files")    
    