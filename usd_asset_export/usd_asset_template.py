import hou
import os

class UsdAssetTemplate():
    def __init__(self, asset_path):
        self.asset_path = asset_path
        self.name = os.path.basename(self.asset_path).split(".")[0].replace("-", "_")
    
    def createTemplate(self):
        root = hou.node("/stage")

        prim = root.createNode("primitive", self.name)
        prim.parm("primkind").set("component")

        sop = root.createNode("sopcreate", self.name + "_components")
        self.createSopAssetPrepNet(sop)

        graft = root.createNode("graftstages", "graftstages")
        graft.parm("primkind").set("subcomponent")
        graft.setInput(0, prim)
        graft.setNextInput(sop)

        mats = root.createNode("materiallibrary", "materiallibrary")
        mats.parm("matpathprefix").set(f"/{self.name}/materials/")
        self.createMaterialsNet(graft, mats)
        mats.setInput(0, graft)

        usdexport = root.createNode("usd_rop", "usd_rop")
        usdexport.parm("lopoutput").set(f"{os.path.dirname(self.asset_path)}/usd_exports/{self.name}/{self.name}.usd")
        usdexport.setInput(0, mats)

        root.layoutChildren()

    def createSopAssetPrepNet(self, sopcreate):
        root = sopcreate.node("./sopnet/create")
        
        file = root.createNode("file", "file")
        file.parm("file").set(self.asset_path)

        primwrangle = root.createNode("attribwrangle", "attribwrangle")
        primwrangle.parm("class").set("primitive")
        primwrangle.parm("snippet").set("s@path = \"/\" + replace(s@shop_materialpath, \"Wolf3D_\", \"\") + \"_geo\";")
        primwrangle.setInput(0, file)

        attribdel = root.createNode("attribdelete", "attribdelete")
        attribdel.parm("ptdel").set("fbx_rotation fbx_scale fbx_translation")
        attribdel.parm("primdel").set("shop_materialpath name")
        attribdel.setInput(0, primwrangle)

        out = root.createNode("output", "output")
        out.setInput(0, attribdel)

        root.layoutChildren()
    
    def createMaterialsNet(self, usdstage, matlib):
        matpath = self.asset_path.replace(".fbx", ".fbm")
        matlist = os.listdir(matpath)

        comps = [p.GetPath().pathString for p in usdstage.stage().GetPseudoRoot().GetChild(self.name).GetChild(self.name + "_components").GetChildren()]

        matlib.parm("materials").set(len(comps))
        for idx, c in enumerate(comps):
            matName = c.split("/")[-1].replace("_geo", "")

            matlib.parm("matnode" + str(idx + 1)).set(matName)
            matlib.parm("assign" + str(idx + 1)).set(1)
            matlib.parm("geopath" + str(idx + 1)).set(c)

            newMat = matlib.createNode("subnet", matName)
            newMat.setMaterialFlag(True)

            mtlxSurf = newMat.createNode("mtlxstandard_surface", "mtlxstandard_surface")
            
            matFilter = matName.split("_")
            matmaps = [m for m in matlist if all([f.lower() in m.lower() for f in matFilter])]

            if len(matmaps) == 0 and matName == "Eye":
                text = newMat.createNode("usduvtexture::2.0", "usduvtexture")
                text.parm("file").set(matpath + "/baseColor")
                mtlxSurf.setNamedInput("base_color", text, "rgb")
            elif len(matmaps) > 0:
                for m in matmaps:
                    text = newMat.createNode("usduvtexture::2.0", "usduvtexture")
                    text.parm("file").set(matpath + "/" + m)

                    if "C" in m:
                        mtlxSurf.setNamedInput("base_color", text, "rgb")
                    elif "N" in m:
                        mtlxSurf.setNamedInput("normal", text, "rgb")
                    elif "R" in m:
                        mtlxSurf.setNamedInput("specular_color", text, "rgb")

            newMat.node("suboutput1").setNextInput(mtlxSurf)
            newMat.layoutChildren()

        matlib.layoutChildren()

def test():
    assetpath = "C:/Users/pprez/Desktop/repos/Py4Prod/usd_asset_export/assets/pp-avatar/pp-avatar.fbx"
    newAssetTemp = UsdAssetTemplate(assetpath)
    newAssetTemp.createTemplate()

if __name__=='__main__':
    print("Hello from UsdAssetTemplate")