# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import bpy_extras.io_utils as io_utils
from . import livi_export
from . import livi_calc
from . import livi_display

class SCENE_LiVi_Export_UI(bpy.types.Panel):
    bl_label = "LiVi Export"    
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        scene = bpy.context.scene
        layout = self.layout
        row = layout.row()
        col = row.column()
        col.label(text = 'Animation:')
        row.prop(scene, "livi_anim")
        row = layout.row()
        
        if int(scene.livi_anim) != 1:
            col = row.column()
            col.label(text = 'Period Type:')
            row.prop(scene, "livi_export_time_type")
            
            if scene.livi_export_time_type == "0":
                row = layout.row()
                col = row.column()
                col.label(text = 'Sky type:')
                row.prop(scene, "livi_export_sky_type")
                sky_type = int(scene.livi_export_sky_type)
               
                if sky_type < 3:
                    row = layout.row()
                    row.prop(scene, "livi_export_latitude")
                    row.prop(scene, "livi_export_longitude")
                    row = layout.row()
                    row.prop(scene, "livi_export_summer_enable")
                    row.prop(scene, "livi_export_summer_meridian") if scene.livi_export_summer_enable else row.prop(scene, "livi_export_standard_meridian")
                    row = layout.row()
                    row.label(text = 'Time:') if int(scene.livi_anim) != "1" else row.label(text = 'Start:')
                    row.prop(scene, "livi_export_start_hour")
                    if scene.livi_export_start_month == "2":
                        row.prop(scene, "livi_export_start_day28")
                    elif scene.livi_export_start_month in (4, 6, 9, 11):
                        row.prop(scene, "livi_export_start_day30")
                    else:
                        row.prop(scene, "livi_export_start_day")
                    row.prop(scene, "livi_export_start_month")    
                    
                elif sky_type == 4:
                    row = layout.row()
                    row.operator(SCENE_LiVi_HDR_Select.bl_idname, text="Select HDR file")
                    row.prop(scene, "livi_export_hdr_name")
                    
                elif sky_type == 5: 
                    row = layout.row()
                    row.operator(SCENE_LiVi_RAD_Select.bl_idname, text="Select Radiance sky file")
                    row.prop(scene, "livi_export_rad_name")
            else:
                row = layout.row()
                row.operator(SCENE_LiVi_EPW_Select.bl_idname, text="Select EPW File")
                row.prop(scene, "livi_export_epw_name")
        else:
            col = row.column()
            col.label(text = 'Sky type:')
            row.prop(scene, "livi_export_sky_type_period")
            sky_type = int(scene.livi_export_sky_type_period)
            row = layout.row()
            row.label(text = 'Start:')
            row.prop(scene, "livi_export_start_hour")
            if scene.livi_export_start_month == "2":
                row.prop(scene, "livi_export_start_day28")
            elif scene.livi_export_start_month in (4, 6, 9, 11):
                row.prop(scene, "livi_export_start_day30")
            else:
                row.prop(scene, "livi_export_start_day")
            row.prop(scene, "livi_export_start_month")    
            
            row = layout.row()
            row.label(text = 'End:')
            row.prop(scene, "livi_export_end_hour")
            if scene.livi_export_end_month == "2":
                row.prop(scene, "livi_export_end_day28")
            elif scene.livi_export_end_month in ("4", "6", "9", "11"):
                row.prop(scene, "livi_export_end_day30")
            else:
                row.prop(scene, "livi_export_end_day")
            
            row.prop(scene, "livi_export_end_month")    
            row = layout.row()
            row.label(text = 'Interval (Hours)')
            row.prop(scene, "livi_export_interval")
            
        row = layout.row()
        col = row.column()
        col.label(text = 'Calculation Points:')
        row.prop(scene, "livi_export_calc_points")
        row = layout.row()
        row.operator("scene.livi_export", text="Export")

class SCENE_LiVi_HDR_Select(bpy.types.Operator, io_utils.ImportHelper):
    bl_idname = "scene.livi_hdr_select"
    bl_label = "Select HDR image"
    bl_description = "Select the angmap format HDR image file"
    filename = ""
    filename_ext = ".hdr; .HDR"
    filter_glob = bpy.props.StringProperty(default="*.hdr; *.HDR", options={'HIDDEN'})
    bl_register = True
    bl_undo = True

    def draw(self,context):
        layout = self.layout
        row = layout.row()
        row.label(text="Import HDR File with FileBrowser", icon='WORLD_DATA')
         
    def execute(self, context):
        scene = context.scene
        if ".hdr" in self.filepath or ".HDR" in self.filepath and " " not in self.filepath:
            scene.livi_export_hdr_name = self.filepath
        elif " " in self.filepath:
            self.report({'ERROR'}, "There is a space either in the HDR filename or its directory location. Remove this space and retry opening the file.")
        else:
            self.report({'ERROR'},"The HDR must be in Radiance RGBE format (*.hdr). Use Luminance-hdr to convert EXR to HDR.")
        return {'FINISHED'}

    def invoke(self,context,event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class SCENE_LiVi_RAD_Select(bpy.types.Operator, io_utils.ImportHelper):
    bl_idname = "scene.livi_rad_select"
    bl_label = "Select radiance sky file"
    bl_description = "Select the Radiance format sky file"
    filename = ""
    filename_ext = ".rad"
    filter_glob = bpy.props.StringProperty(default="*.rad", options={'HIDDEN'})
    bl_register = True
    bl_undo = True

    def draw(self,context):
        layout = self.layout
        row = layout.row()
        row.label(text="Import a Radiance sky with the file browser", icon='WORLD_DATA')
         
    def execute(self, context):
        scene = context.scene
        scene.livi_export_rad_name = self.filepath
        return {'FINISHED'}

    def invoke(self,context,event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
        
        
class SCENE_LiVi_EPW_Select(bpy.types.Operator, io_utils.ImportHelper):
    bl_idname = "scene.livi_epw_select"
    bl_label = "Select EPW file"
    bl_description = "Select the EnergyPlus weather file"
    filename = ""
    filename_ext = ".HDR;.hdr;.epw;.EPW;"
    filter_glob = bpy.props.StringProperty(default="*.HDR;*.hdr;*.epw;*.EPW;", options={'HIDDEN'})
    bl_register = True
    bl_undo = True
    
    def draw(self,context):
        layout = self.layout
        row = layout.row()
        row.label(text="Import EPW File with FileBrowser", icon='WORLD_DATA')
        row = layout.row()

    def execute(self, context):
        scene = context.scene
        if self.filepath.split(".")[-1] in ("epw", "EPW", "HDR", "hdr"):
            scene.livi_export_epw_name = self.filepath
        if " " in self.filepath:
            self.report({'ERROR'}, "There is a space either in the EPW filename or its directory location. Remove this space and retry opening the file.")
        return {'FINISHED'}

    def invoke(self,context,event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
        
class SCENE_LiVi_VEC_Select(bpy.types.Operator, io_utils.ImportHelper):
    bl_idname = "scene.livi_mtx_select"
    bl_label = "Select MTX file"
    bl_description = "Select the generated MTX file"
    filename = ""
    filename_ext = ".mtx"
    filter_glob = bpy.props.StringProperty(default="*.mtx", options={'HIDDEN'})
    bl_register = True
    bl_undo = True
    
    def draw(self,context):
        layout = self.layout
        row = layout.row()
        row.label(text="Import MTX file with fileBrowser", icon='WORLD_DATA')
        row = layout.row()

    def execute(self, context):
        scene = context.scene
        if  self.filepath.split(".")[-1] in ("mtx"):
            scene.livi_calc_mtx_name = self.filepath
        if " " in self.filepath:
            self.report({'ERROR'}, "There is a space either in the MTX filename or its directory location. Remove this space and retry opening the file.")
        return {'FINISHED'}

    def invoke(self,context,event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class SCENE_LiVi_Export(bpy.types.Operator, io_utils.ExportHelper):
    bl_idname = "scene.livi_export"
    bl_label = "Export"
    bl_description = "Export the scene to the Radiance file format"
    bl_register = True
    bl_undo = True
    
    def invoke(self, context, event):
        global lexport
        if bpy.data.filepath:
            scene = context.scene
            if scene.livi_export_time_type == "0" or scene.livi_anim == "1":
                scene['skytype'] = int(scene.livi_export_sky_type_period) if scene.livi_anim == "1" else int(scene.livi_export_sky_type)
                if scene.livi_export_start_month == 2:
                    startD = scene.livi_export_start_day28
                elif scene.livi_export_start_month in (4, 6, 9, 11):
                    startD = scene.livi_export_start_day30
                else:
                    startD = scene.livi_export_start_day        
                if scene.livi_export_summer_enable == True:
                    TZ = scene.livi_export_summer_meridian
                else:
                    TZ = scene.livi_export_standard_meridian
                    
            elif scene.livi_export_time_type == "1":
                startD = 1
                TZ = 0
                scene['skytype'] = 6
                if scene.livi_export_epw_name == "":
                    self.report({'ERROR'},"Select an EPW weather file.")
                    return {'FINISHED'}

            scene['cp'] = int(scene.livi_export_calc_points)

            if bpy.context.object:
                if bpy.context.object.type == 'MESH' and bpy.context.object.hide == False and bpy.context.object.layers[0] == True:
                    bpy.ops.object.mode_set(mode = 'OBJECT')
            if " " not in bpy.data.filepath:
                lexport = livi_export.LiVi_e(bpy.data.filepath, scene, startD, TZ, self)   

                lexport.scene.livi_display_legend = -1
            else:    
                self.report({'ERROR'},"The directory path or Blender filename has a space in it. Please save again without any spaces")
                return {'FINISHED'}
            
            return {'FINISHED'}
        else:
            self.report({'ERROR'},"Save the Blender file before exporting")
            return {'FINISHED'} 
        
class SCENE_LiVi_Calc_UI(bpy.types.Panel):
    bl_label = "LiVi Calculator"    
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"       
    
    def draw(self, context):
        scene = context.scene
        try:        
            if lexport.export == 1 and 'skytype' in scene:
                layout = self.layout
                row = layout.row()
                col = row.column()
                col.label(text = 'Simulation Metric:')
                if scene.livi_export_time_type == "0" or scene.livi_anim == "1":
                    if scene['skytype'] < 3 or scene['skytype'] in (4,5):
                        row.prop(scene, "livi_metric")
                        lexport.metric = scene.livi_metric
                    elif lexport.sky_type == 3:
                        row.prop(scene, "livi_metricdf")
                        lexport.metric = scene.livi_metricdf
                else:
                    row.prop(scene, "livi_metricdds")
                    lexport.metric = scene.livi_metricdds
                    
                if lexport.metric == "4" and lexport.scene.livi_export_time_type == "1":
                    if  scene.livi_export_epw_name.split(".")[-1] in ("hdr"):
                        row = layout.row()
                        row.operator(SCENE_LiVi_VEC_Select.bl_idname, text="Select MTX File")
                        row.prop(scene, "livi_calc_mtx_name")
                    row = layout.row()
                    row.label(text = 'DA Occupancy:')
                    row.prop(scene, "livi_calc_da_weekdays")
                    row = layout.row()
                    row.label(text = 'Start Hour:')
                    row.prop(scene, "livi_calc_dastart_hour")
                    row = layout.row()
                    row.label(text = 'End Hour:')
                    row.prop(scene, "livi_calc_daend_hour")
                    row = layout.row()
                    row.label(text = 'Threshold Lux:')
                    row.prop(scene, "livi_calc_min_lux")
                row = layout.row()
                col = row.column()                
                col.label(text = 'Simulation Accuracy:')
                row.prop(scene, "livi_calc_acc") 
                if scene.livi_calc_acc == "3":
                    row = layout.row()
                    row.prop(scene, "livi_calc_custom_acc")
    
                row = layout.row()
                row.operator("scene.livi_rad_preview", text="Radiance Preview")
                row.operator("scene.livi_rad_calculate", text="Simulate")
                
        except Exception as e:
            if str(e) != "global name 'lexport' is not defined":
                print(e)

class SCENE_LiVi_Preview(bpy.types.Operator):
    bl_idname = "scene.livi_rad_preview"
    bl_label = "Radiance Preview"
    bl_description = "Preview the scene with Radiance"
    bl_register = True
    bl_undo = True
    
    def invoke(self, context, event):
        lprev = livi_calc.LiVi_c(lexport, self)
        return {'FINISHED'}

class SCENE_LiVi_Calculator(bpy.types.Operator):
    bl_idname = "scene.livi_rad_calculate"
    bl_label = "Radiance Calculation"
    bl_description = "Calculate values at the sensor points with Radiance"
    bl_register = True
    bl_undo = True
    
    def invoke(self, context, event):
        global lcalc
        scene = context.scene
        scene['metric'] = lexport.metric
        lcalc = livi_calc.LiVi_c(lexport, self)   
        scene['unit'] = lcalc.unit[int(scene['metric'])]
        livi_display.rendview(0)
        lexport.scene.livi_display_legend = -1
        return {'FINISHED'}

class SCENE_LiVi_Disp_UI(bpy.types.Panel):
    bl_label = "LiVi Display"    
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"    
    
    def draw(self, context):
        view = context.space_data
        scene = context.scene
          
        if scene.livi_display_panel == 1:
            layout = self.layout
            row = layout.row()
            row.operator("scene.livi_rad_display", text="Radiance Display")
            row.prop(view, "show_only_render")
            row.prop(scene, "livi_disp_3d")
            if int(context.scene.livi_disp_3d) == 1:
                row = layout.row()
                row.prop(scene, "livi_disp_3dlevel")
            try:
                if ldisplay.rp_display == False:
                    pass
                else:
                    if context.mode == "OBJECT":
                        row = layout.row()
                        row.label(text="{:-<48}".format("Point visualisation "))
                        row = layout.row()
                        row.prop(scene, "livi_display_respoints")
                        row.prop(context.scene, "livi_display_sel_only")
                        row.prop(context.scene, "livi_display_rp_fs")
                        row = layout.row()
                        row.label(text="{:-<60}".format(""))
            except:
                pass
        
class SCENE_LiVi_Display(bpy.types.Operator):
    bl_idname = "scene.livi_rad_display"
    bl_label = "Radiance Results Display"
    bl_description = "Display the results on the sensor surfaces"
    bl_register = True
    bl_undo = True
       
    def invoke(self, context, event):
        global ldisplay
        try:
            ldisplay = livi_display.LiVi_d()
            bpy.ops.view3d.data_display()
        except:
            self.report({'ERROR'},"No results available for display. Try re-running the calculation.")
            raise
        return {'FINISHED'}
 
class VIEW3D_OT_data_display(bpy.types.Operator):
    '''Display results legend and stats in the 3D View'''
    bl_idname = "view3d.data_display"
    bl_label = "Display results legend and stats in the 3D View"
    bl_options = {'REGISTER'}
    
    def modal(self, context, event):
        context.area.tag_redraw()
        if context.scene.livi_display_legend == -1:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle_leg, 'WINDOW')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle_stat, 'WINDOW')
            bpy.types.SpaceView3D.draw_handler_remove(self._handle_pointres, 'WINDOW')
            ldisplay.rp_display = False
            return {'CANCELLED'}
        return {'PASS_THROUGH'}        
          
    def execute(self, context):
        from . import livi_display
        if context.area.type == 'VIEW_3D':
            self._handle_leg = bpy.types.SpaceView3D.draw_handler_add(livi_display.rad_3D_legend, (self, context), 'WINDOW', 'POST_PIXEL')
            self._handle_stat = bpy.types.SpaceView3D.draw_handler_add(livi_display.res_stat, (self, context), 'WINDOW', 'POST_PIXEL')
            self._handle_pointres = bpy.types.SpaceView3D.draw_handler_add(livi_display.respoint_visualiser, (self, context, ldisplay), 'WINDOW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)
            context.scene.livi_display_legend = 0
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

class SCENE_LiVi_framechange(bpy.types.Operator):
    '''Display the results statistics in the 3D view'''
    bl_idname = "scene.livi_framechange"
    bl_label = "Display result statistics in the 3D View"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        from . import livi_display
        livi_display.cyfc(self, context)

class IESPanel(bpy.types.Panel):
    bl_label = "LiVi IES file"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    
    @classmethod
    def poll(cls, context):
        if context.lamp or 'lightarray' in context.object.name:
            return True

    def draw(self, context):
        layout = self.layout
        lamp = bpy.context.active_object
        layout.operator("livi.ies_select") 
        layout.prop(lamp, "ies_name")
        row = layout.row()
        row.prop(lamp, "ies_unit")
        row = layout.row()
        row.prop(lamp, "ies_strength")

class IES_Select(bpy.types.Operator, io_utils.ImportHelper):
    bl_idname = "livi.ies_select"
    bl_label = "Select IES file"
    bl_description = "Select the lamp IES file"
    filename = ""
    filename_ext = ".ies; .IES"
    filter_glob = bpy.props.StringProperty(default="*.ies; *.IES", options={'HIDDEN'})
    bl_register = True
    bl_undo = True

    def draw(self,context):
        layout = self.layout
        row = layout.row()
        row.label(text="Open an IES File with the file browser", icon='WORLD_DATA')
         
    def execute(self, context):
        lamp = bpy.context.active_object
        lamp['ies_name'] = self.filepath if " " not in self.filepath else self.report({'ERROR'}, "There is a space either in the IES filename or directory location. Rename or move the file.")
        return {'FINISHED'}

    def invoke(self,context,event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
        
   
