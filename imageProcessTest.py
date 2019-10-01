
import math
import bpy
"""
TODO:
• figure out blender autocomplete thing https://b3d.interplanety.org/en/using-microsoft-visual-studio-code-as-external-ide-for-writing-blender-scripts-add-ons/
• array rather than placing?
• more file types: animated gif would be cool!
• rounding r g and b values for more legit peg colours (issue: duplicate mats; how to check if any others have same r g and b?)
"""
#pegs = []
# path = "F:/Projects/Animation/Lite Brite/things/testimg9.bmp"
path = "F:/Projects/Animation/Lite Brite/things/testimg5.bmp"

def round_nearest(x, a):
    return round(x / a) * a

class Peg:
    def __init__(self, x, y, index,pegs):
        self.colour = "red"
        self.x = 0.2*x
        self.y = 0.2*y
        if (y%2 > 0):
            self.x = self.x+0.1
        self.index = index
        # bpy.ops.mesh.primitive_plane_add(location = (self.x,self.y,0),)

        name = 'Peg'+'{0:04}'.format(index)
        self.bObj = bpy.data.objects.new(name,bpy.data.meshes["Peg"].copy())
        self.bObj.location = (self.x,self.y,0)        
        # self.bObj.data = bpy.data.objects.get("Peg").data.copy()
        
        pegs.link(self.bObj)


def initialize_pegs(x,y):
    #for now: shifting smaller row left, will have 1 fewer pixel than larger row (will just be not drawn)
    #left to right, top to bottom
    #count = x*y - math.floor(y/2)
    count = x*y
    xpos = 0
    ypos = 0
    bpy.data.scenes[0]['oldX'] = x
    bpy.data.scenes[0]['oldY'] = y
    bpy.data.collections.new("generatedPegs")

    pegs = bpy.data.collections.get("generatedPegs").objects
    bpy.data.scenes[0].collection.children.link(bpy.data.collections.get("generatedPegs"))

    #base = bpy.data.objects.new("generatedBase",bpy.data.curves.get("Base").data.copy())
    base = bpy.data.objects.new("generatedBase",bpy.data.curves["Base"].copy())
    base.location = (0,0,0)
    base.data.splines[0].bezier_points[3].co = (-1, -1, 0)#bottom left
    base.data.splines[0].bezier_points[3].handle_right = (-1, -1+0.2, 0)
    base.data.splines[0].bezier_points[3].handle_left = (-1+0.2, -1, 0)

    for w in range(0,count):
        p = Peg(xpos,ypos,w,pegs)#0.03m radius
        spline = base.data.splines.new("BEZIER")
        spline.bezier_points.add(count=3)
        spline.bezier_points[0].co = (p.x + 0.04, p.y, 0)
        spline.bezier_points[0].handle_left = (p.x + 0.04, p.y - 0.022085, 0)
        spline.bezier_points[0].handle_right = (p.x + 0.04, p.y + 0.022085, 0)
        spline.bezier_points[1].co = (p.x, p.y + 0.04, 0)
        spline.bezier_points[1].handle_left= (p.x + 0.022085, p.y + 0.04, 0)
        spline.bezier_points[1].handle_right = (p.x - 0.022085, p.y + 0.04, 0)
        spline.bezier_points[2].co = (p.x - 0.04, p.y, 0)
        spline.bezier_points[2].handle_left = (p.x - 0.04, p.y + 0.022085, 0)
        spline.bezier_points[2].handle_right = (p.x - 0.04, p.y - 0.022085, 0)
        spline.bezier_points[3].co = (p.x, p.y - 0.04, 0)
        spline.bezier_points[3].handle_left= (p.x - 0.022085, p.y - 0.04, 0)
        spline.bezier_points[3].handle_right = (p.x + 0.022085, p.y - 0.04, 0)
        spline.use_cyclic_u = True

        xpos = xpos + 1
        #print("xpos: {0}, ypos: {1}, obj's coords: ({2},{3})".format(str(xpos),str(ypos),str(pegs[w].x),str(pegs[w].y)))
        print("init xpos: {0}, ypos: {1}".format(str(xpos),str(ypos)))
        if xpos >= x:
            xpos = 0
            ypos = ypos + 1
    base.data.splines[0].bezier_points[2].co = (width*0.2 + 1, -1, 0)        #bottom right
    base.data.splines[0].bezier_points[2].handle_left = (width*0.2 + 1, -1+0.1, 0)   
    base.data.splines[0].bezier_points[2].handle_right = (width*0.2 + 1-0.1, -1, 0)   
    base.data.splines[0].bezier_points[1].co = (width*0.2 + 1, height*0.2 + 1, 0)  #top right
    base.data.splines[0].bezier_points[1].handle_left = (width*0.2 + 1-0.1, height*0.2 + 1, 0)
    base.data.splines[0].bezier_points[1].handle_right = (width*0.2 + 1, height*0.2-0.1 + 1, 0)
    base.data.splines[0].bezier_points[0].co = (-1, height*0.2 + 1, 0)        #top left
    base.data.splines[0].bezier_points[0].handle_left = (-1, height*0.2 + 1-0.1, 0)
    base.data.splines[0].bezier_points[0].handle_right = (-1+0.1, height*0.2 + 1, 0)

#   base = bpy.data.objects.new("generatedBase",bpy.data.curves["Base"].copy())
    emit = bpy.data.objects.new("generatedEmit",bpy.data.meshes["Emit"].copy())
    emit.data.vertices[0].co = (0-0.9, 0-0.9, -0.1)                  #bottom left
    emit.data.vertices[1].co = (width*0.2+0.9, 0-0.9, -0.1)             #bottom right
    emit.data.vertices[2].co = (0-0.9, height*0.2+0.9, -0.1)            #top left
    emit.data.vertices[3].co = (width*0.2+0.9, height*0.2+0.9, -0.1) #top right

    pegs.link(base)
    pegs.link(emit)

def purge():
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)
    for block in bpy.data.curves:
        if block.users == 0:
            bpy.data.curves.remove(block)
            print("purge!")

#initialize_pegs(5,5)

with open(path, "rb") as f:
    f.read(2)
    fileSize = int.from_bytes(f.read(4),byteorder='big')

    f.read(4)
    pixelArrayStart = int.from_bytes(f.read(1),byteorder='big')
    dibsize = int.from_bytes(f.read(4),byteorder='big')
    width = int.from_bytes(f.read(4),byteorder='big')
    height = int.from_bytes(f.read(4),byteorder='big')
    

    oldx = bpy.data.scenes[0]['oldX']
    oldy = bpy.data.scenes[0]['oldy']
    
    # if oldx == -1 and oldy == -1:
    #     initialize_pegs(width,height)
    purge()
    if (bpy.data.collections.get("generatedPegs") != None ):        #existing pegs
        pegs = bpy.data.collections.get("generatedPegs").objects    
        if width != oldx and height != oldy:                        #new size?
            for obj in pegs:                                        #remake
                bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.collections.remove(bpy.data.collections.get("generatedPegs"),do_unlink=True)
            initialize_pegs(width,height)
            print("init!")
    else:
        initialize_pegs(width,height)
    purge()
    
    pegs = bpy.data.collections.get("generatedPegs").objects

    f.read(4)
    bitDepth =  int.from_bytes(f.read(2),byteorder='big')
    f.read(25)#24? 23. 25!
    #now at pixel array

    x = 0
    y = 0
    c = 0

    mats = bpy.data.materials

    while (f.readable and c < width*height):
        

        b = int.from_bytes(f.read(1),byteorder='big')/255
        g = int.from_bytes(f.read(1),byteorder='big')/255
        r = int.from_bytes(f.read(1),byteorder='big')/255
        print("c, (r,g,b):   {0}, ({1},{2},{3})  peg:{4}".format(c,r,g,b, pegs[c].name))
        if c is not 0 and (c+1)%width == 0:
            remainder = ((3*width) % 4)
            pad =  remainder
            if remainder != 0:
                f.read(pad )#for padding
        if r <0.3 and g<0.3 and b<0.3:
            r=0;g=0;b=0
            pegs[c].data = bpy.data.meshes["Blank"]
        else:
            pegs[c].data = bpy.data.meshes["Peg"].copy()
        pegs[c].material_slots[0].material = bpy.data.materials.new(name="genCol")
        mat = pegs[c].material_slots[0].material
        mat.use_nodes = True
        nt = mat.node_tree
        nodes = nt.nodes
        links = nt.links

        while(nodes): nodes.remove(nodes[0])

        d_output = nodes.new("ShaderNodeOutputMaterial")
        d_glass = nodes.new("ShaderNodeBsdfGlass")
        d_glass.location = (-200,0)

        # r = round_nearest(r, 0.33)
        # g = round_nearest(g, 0.33)
        # b = round_nearest(b, 0.33)

        d_glass.inputs[0].default_value = (r, g, b, 1)
        mat.diffuse_color = (r, g, b, 1)

        links.new(d_glass.outputs["BSDF"],d_output.inputs["Surface"])
        
        c = c+1
    purge()
        