from abaqus import *
from abaqusConstants import *

width  = 20.0
height = 5.0
origin = (15.0, 0.0)
pitch = 50.0
numTurns = 2.0

s = mdb.models['Model-1'].ConstrainedSketch(name='rect', sheetSize=200.0)
g = s.geometry
s.setPrimaryObject(option=STANDALONE)
cl = s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
s.FixedConstraint(entity=g[2])
s.FixedConstraint(entity=g[cl.id])
s.rectangle(point1=(origin[0], origin[1]), point2=(origin[0]+width, origin[1]+height))

p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']

p.BaseSolidRevolve(sketch=s, angle=numTurns*360.0, flipRevolveDirection=OFF, 
    pitch=pitch, flipPitchDirection=OFF, moveSketchNormalToPath=OFF) 
    #In above command try changing the following member: moveSketchNormalToPath=ON

s.unsetPrimaryObject()

session.viewports['Viewport: 1'].setValues(displayedObject=p)