bl_info = {
    "name": "Armature Copy",
    "author": "Mike Miller",
    "version": (2, 0),
    "blender": (2, 70, 0),
    "location": "View3D > Object > ",
    "description": "Copies from one armature to another",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}

import bpy

      
class BoneCopyOperator(bpy.types.Operator):
    """Copies new bones in the selected armature to the active armature. Bones that already exist in the active armature are not changed."""
    bl_idname = "armature_copy.bone_copy_operator"
    bl_label = "Bone Copy Operator"
    bl_options = {'REGISTER'}

    
    def execute(self, context):
        #check to make sure the user has made valid selections
        if len(bpy.context.selected_objects) != 2:
            self.report({'ERROR'}, 'Select TWO armatures!')
            print('You have to select two armatures for this operation. The active armature will be the destination and the other will be the source.')
            return {'FINISHED'}
        toarmature = bpy.context.scene.objects.active
        if toarmature.type != 'ARMATURE':
            self.report({'ERROR'}, 'Destination object not a armature!')
            print('The destination object is not a armature-type object.')
            return {'FINISHED'}
        for obj in bpy.context.selected_objects:
            if obj.name != toarmature.name:
                fromarmature = obj
        if fromarmature.type != 'ARMATURE':
            self.report({'ERROR'}, 'Source object not a armature!')
            print('The source object is not a armature-type object.')
            return {'FINISHED'}
        '''Make a copy of the source amature. This copy will then
        be modified to match the geometry of the destination armature. 
        Then the destination armature is replaced by the copy.'''
        allobjects = bpy.context.scene.objects.keys()
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[fromarmature.name].select = True 
        bpy.ops.object.duplicate()
        newarmature = None
        for i in bpy.context.scene.objects.keys():
            if i not in allobjects:
                newarmature = bpy.context.scene.objects[i]

        edit_rig(toarmature.name)
        bonelocations = {}
        for b in toarmature.data.edit_bones:
            bonelocations[b.name]=[b.head.xyz, b.tail.xyz, b.roll]
        edit_rig(newarmature.name)
        for b in bonelocations:
            if b in newarmature.data.bones.keys():
                newarmature.data.edit_bones[b].head = bonelocations[b][0]
                newarmature.data.edit_bones[b].tail = bonelocations[b][1]
                newarmature.data.edit_bones[b].roll = bonelocations[b][2]
        #to do: transfer all children from toarmature to newarmature
        newname = toarmature.name
        bpy.data.objects.remove(toarmature, True)
        newarmature.name = newname

        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

def edit_rig(rigname):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    bpy.data.objects[rigname].select = True 
    bpy.context.scene.objects.active = bpy.data.objects[rigname]
    bpy.ops.object.mode_set(mode='EDIT')
        
def draw(self, context):
    layout = self.layout
    col = layout.column(align=True)
    active = bpy.context.active_object
    scn = bpy.context.scene

    if active:
        if active.type == 'ARMATURE' and bpy.context.mode == 'OBJECT':
            col.operator(BoneCopyOperator.bl_idname, text = "Copy Additional Bones")


def register():
    bpy.utils.register_class(BoneCopyOperator)
    bpy.types.VIEW3D_PT_tools_object.append(draw)

def unregister():
    bpy.utils.unregister_class(BoneCopyOperator)
    bpy.types.VIEW3D_PT_tools_object.remove(draw)
    
if __name__ == "__main__":
    register()