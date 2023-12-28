#!/usr/bin/env python
import sys
from geant4_pybind import *
class X5DetectorConstruction(G4VUserDetectorConstruction):
   """
   Simple model: a sphere with water in the air box.
   """
 
   def __init__(self):
        super().__init__()
        self.fScoringVolume = None
        
   def Construct(self):

        nist = G4NistManager.Instance()

        envelop_x = 64*cm
        envelop_y = 64*cm
        envelop_z = 64*cm
        envelop_mat = nist.FindOrBuildMaterial("G4_AIR")
 
        sphere_rad1 = 29*cm
        sphere_rad2 = 28*cm
        x_axis = 15*cm
        y_axis = 8*cm
        z_axis = 15*cm
        x_axis2 = 10*cm
        y_axis2 = 6*cm
        z_axis2 = 10*cm
        mat1 = nist.FindOrBuildMaterial("B-100_BONE")
        mat2 = nist.FindOrBuildMaterial("G4_WATER")
        mat3 = nist.FindOrBuildMaterial("G4_ACETONE")
        mat4 = nist.FindOrBuildMaterial("G4_BENZENE")
         
        checkOverlaps = True
 
        world_x = 2*envelop_x
        world_y = 2*envelop_y
        world_z = 2*envelop_z
 
        sWorld = G4Box("World", 0.5*world_x, 0.5*world_y, 0.5*world_z)
        lWorld = G4LogicalVolume(sWorld, envelop_mat, "World")
        pWorld = G4PVPlacement(None, G4ThreeVector(),lWorld, "World", None, False,0, checkOverlaps)

        sEnvelop = G4Box ("Envelop", 0.5*envelop_x, 0.5*envelop_y, 0.5*envelop_z)
        lEnvelop = G4LogicalVolume(sEnvelop, envelop_mat, "Envelop")
        pEnvelop = G4PVPlacement (None, G4ThreeVector(), lEnvelop, "Envelop", lWorld, True, 0, checkOverlaps)

        sSphere1 = G4Orb("Skullbones", sphere_rad1)

        sSphere2 = G4Orb("WaterHead", sphere_rad2)
        
        sCutSphere = G4SubtractionSolid ("Skullbones-WaterHead", sSphere1, sSphere2)
        lSphere3 = G4LogicalVolume (sSphere2, mat2, "Water")
        lSphere4 = G4LogicalVolume (sCutSphere, mat1, "BoneSurface")
        
        G4PVPlacement (None, G4ThreeVector(), lSphere4, "BoneSurface", lEnvelop, True, 0, checkOverlaps)
        G4PVPlacement (None, G4ThreeVector(), lSphere3, "Water", lSphere4, True, 0, checkOverlaps)

        sEllipsoid1 = G4Ellipsoid ("Acetone", x_axis, y_axis, z_axis)
       
        sEllipsoid2 = G4Ellipsoid("Benzene", x_axis2, y_axis2, z_axis2)
                
        shift = -1*y_axis2
        zTrans = G4ThreeVector(0, shift, 0)
        sCutBrain = G4SubtractionSolid("Brain", sEllipsoid1, sEllipsoid2, G4RotationMatrix(), zTrans)
        lLowerBrain = G4LogicalVolume (sEllipsoid2, mat4, "LowerBrain")
        lUpperBrain = G4LogicalVolume (sCutBrain, mat3, "UpperBrain")

        G4PVPlacement (None, -0.5*zTrans, lUpperBrain, "UpperBrain", lSphere3, True, 0, checkOverlaps)
        G4PVPlacement (None, 0.5*zTrans, lLowerBrain, "LowerBrain", lSphere3, True, 0, checkOverlaps)

        self.fScoringVolume = lSphere4
 
        return pWorld

ui = None
if len(sys.argv) == 1:
    ui = G4UIExecutive(len(sys.argv), sys.argv)

# Optionally: choose a different Random engine...
# G4Random.setTheEngine(MTwistEngine())

runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.Serial)
runManager.SetUserInitialization(X5DetectorConstruction())

# Physics list

physicsList = QBBC()
physicsList.SetVerboseLevel(1)
runManager.SetUserInitialization(physicsList)

# User action initialization

#runManager.SetUserInitialization(XXActionInitialization())
visManager = G4VisExecutive()

# G4VisExecutive can take a verbosity argument - see /vis/verbose guidance.
# visManager = G4VisExecutive("Quiet")

visManager.Initialize()

# Get the User Interface manager

UImanager = G4UImanager.GetUIpointer()

# # Process macro or start UI session

if ui == None:

   # batch mode

   command = "/control/execute "
   fileName = sys.argv[1]
   UImanager.ApplyCommand(command + fileName)
else:

   # interactive mode

   UImanager.ApplyCommand("/control/execute init_vis.mac")
   ui.SessionStart()
