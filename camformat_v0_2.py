# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 3
#  of the License.
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


bl_info = {  
 "name": "CamFormat",  
 "author": "Samy Tichadou (tonton)",  
 "version": (0, 2),  
 "blender": (2, 7, 9),  
 "location": "Properties > Camera > Output Format",  
 "description": "Store Output Format Settings per Camera",  
 "warning": "Beta Version, save your work before using",
  "wiki_url": "https://github.com/samytichadou/CamFormat_blender_addon/wiki",  
 "tracker_url": "https://github.com/samytichadou/CamFormat_blender_addon/issues/new",  
 "category": "Camera"}

import bpy
from bpy.app.handlers import persistent


#######################################################################
### addon preferences ###
#######################################################################

class CamFormatAddonPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    camformat_auto_update_from_cam = bpy.props.BoolProperty(
            name="CamFormat Auto-Update from Camera",
            description="If enabled, changing active scene camera will load its output settings",
            default=True
            )
            
    camformat_live_update_from_cam = bpy.props.BoolProperty(
            name="CamFormat Live Update from Camera",
            description="If enabled, changing active scene camera settings change scene output settings",
            default=True
            )
            
    camformat_create_cam_scene_settings = bpy.props.BoolProperty(
            name="CamFormat Camera Creation with Scene settings",
            description="If enabled, when a new camera is created, it will copy scene output settings\nIf disabled, it will take the default camformat settings",
            default=True
            )
    
    camformat_dimension_settings = bpy.props.BoolProperty(
            name="Store Dimensions settings",
            description="If enabled, Dimensions settings will be stored in Cameras",
            default=True
            )
    
    camformat_mblur_settings = bpy.props.BoolProperty(
            name="Store Motion Blur settings",
            description="If enabled, Motion Blur settings will be stored in Cameras",
            default=True
            )
    
    camformat_output_settings = bpy.props.BoolProperty(
            name="Store Output settings",
            description="If enabled, Output settings will be stored in Cameras",
            default=True
            )
            
    camformat_default_cam_display = bpy.props.BoolProperty(default=False)
    
    #Default cam Props 
    
    #UI props
    camformatD_ui_menu = bpy.props.EnumProperty(items = \
        (('dimensions', "Dimensions", "Dimensions Settings"),
        ('motionblur', "Motion Blur", "Motion Blur Settings"),
        ('output', "Output", "Output Settings"),
        ),
        default = 'dimensions',
        )
    
    #Dimension props
    camformatD_res_x = bpy.props.IntProperty(default=1920, min=4, max=65536)
    camformatD_res_y = bpy.props.IntProperty(default=1080, min=4, max=65536) 
    camformatD_start_frame = bpy.props.IntProperty(default=1, min=0, max=1048574)
    camformatD_end_frame = bpy.props.IntProperty(default=250, min=0, max=1048574)
    camformatD_res_pct = bpy.props.IntProperty(default=50, min=1, max=32767, subtype='PERCENTAGE')
    camformatD_frame_step = bpy.props.IntProperty(default=1, min=1, max=100)
    camformatD_ratio_x = bpy.props.FloatProperty(default=1, min=1, max=200, step=10, precision=3)
    camformatD_ratio_y = bpy.props.FloatProperty(default=1, min=1, max=200, step=10, precision=3)
    camformatD_fps = bpy.props.IntProperty(default=25, min=1, max=120)
    camformatD_fps_base = bpy.props.FloatProperty(default=1, min=0.1, max=120, step=10, precision=3)
    camformatD_border = bpy.props.BoolProperty(default=False)
    camformatD_crop = bpy.props.BoolProperty(default=False)
    camformatD_border_min_x = bpy.props.FloatProperty(default=0, min=0, max=1, step=10, precision=3)
    camformatD_border_min_y = bpy.props.FloatProperty(default=0, min=0, max=1, step=10, precision=3)
    camformatD_border_max_x = bpy.props.FloatProperty(default=1, min=0, max=1, step=10, precision=3)
    camformatD_border_max_y = bpy.props.FloatProperty(default=1, min=0, max=1, step=10, precision=3)
    camformatD_frame_map_old = bpy.props.IntProperty(default=100, min=1, max=900)
    camformatD_frame_map_new = bpy.props.IntProperty(default=100, min=1, max=900)
    
    #Output props
    camformatD_render_filepath = bpy.props.StringProperty(
        default="//",
        subtype='FILE_PATH')
    camformatD_overwrite = bpy.props.BoolProperty(default=True)
    camformatD_file_extensions = bpy.props.BoolProperty(default=True)
    camformatD_placeholders = bpy.props.BoolProperty(default=False)
    camformatD_cache_result = bpy.props.BoolProperty(default=False)
    camformatD_file_format = bpy.props.EnumProperty(items = \
        (('BMP', "BMP", "Bitmap", 'IMAGE_DATA', 0),
        ('IRIS', "Iris", "SGI Iris", 'IMAGE_DATA', 1),
        ('PNG', "PNG", "Portable Network Graphics", 'IMAGE_DATA', 3),
        ('JPEG', "JPEG", "Joint Photographic Experts Group", 'IMAGE_DATA', 4),
        ('JPEG2000', "JPEG 2000", "Joint Photographic Experts Group 2000", 'IMAGE_DATA', 5),
        ('TARGA', "Targa", "Truevision Targa", 'IMAGE_DATA', 6),
        ('TARGA_RAW', "Targa Raw", "Truevision Targa Raw", 'IMAGE_DATA', 7),
        ('CINEON', "Cineon", "Cineon Image File", 'IMAGE_DATA', 8),
        ('DPX', "DPX", "Digital Picture Exchange", 'IMAGE_DATA', 9),
        ('OPEN_EXR_MULTILAYER', "OpenEXR Multilayer", "OpenEXR Multilayer", 'IMAGE_DATA', 10),
        ('OPEN_EXR', "OpenEXR", "OpenEXR", 'IMAGE_DATA', 11),
        ('HDR', "Radiance HDR", "Radiance High Dynamic Range File", 'IMAGE_DATA', 12),
        ('TIFF', "TIFF", "Tagged Image File Format", 'IMAGE_DATA', 13),
        ('AVI_JPEG', "AVI JPEG", "AVI JPEG Movie", 'FILE_MOVIE', 14),
        ('AVI_RAW', "AVI Raw", "AVI Raw Movie", 'FILE_MOVIE', 15),
        ('FRAMESERVER', "Frame Server", "Frame Server", 'FILE_SCRIPT', 16),
        ('FFMPEG', "FFmpeg video", "FFmpeg Movie", 'FILE_MOVIE', 17),
        ),
        name = 'Output Format',
        default = 'PNG')
    camformatD_color_mode_simple = bpy.props.EnumProperty(items = \
        (('BW', "BW", "Black and White"),
        ('RGB', "RGB", "Red Green Blue"),
        ),
        name = 'Color Mode',
        default = 'RGB')
    camformatD_color_mode = bpy.props.EnumProperty(items = \
        (('BW', "BW", "Black and White"),
        ('RGB', "RGB", "Red Green Blue"),
        ('RGBA', "RGBA", "Red Green Blue Alpha"),
        ),
        name = 'Color Mode',
        default = 'RGB')
    camformatD_color_depth_pngtiff = bpy.props.EnumProperty(items = \
        (('8', "8", "8 bits"),
        ('16', "16", "16 bits"),
        ),
        name = 'Color Depth',
        default = '8')
    camformatD_color_depth_jpeg2000 = bpy.props.EnumProperty(items = \
        (('8', "8", "8 bits"),
        ('12', "12", "12 bits"),
        ('16', "16", "16 bits"),
        ),
        name = 'Color Depth',
        default = '8')
    camformatD_color_depth_dpx = bpy.props.EnumProperty(items = \
        (('8', "8", "8 bits"),
        ('10', "10", "10 bits"),
        ('12', "12", "12 bits"),
        ('16', "16", "16 bits"),
        ),
        name = 'Color Depth',
        default = '8')
    camformatD_color_depth_oexr = bpy.props.EnumProperty(items = \
        (('16', "Float (Half)", "Float (Half)"),
        ('32', "Float (Full)", "Float (Full)"),
        ),
        name = 'Color Depth',
        default = '16')
    camformatD_quality = bpy.props.IntProperty(default=90, min=0, max=100, subtype='PERCENTAGE')
    camformatD_compression = bpy.props.IntProperty(default=15, min=0, max=100, subtype='PERCENTAGE')
        #jpeg 2000
    camformatD_jpeg2k_codec = bpy.props.EnumProperty(items = \
        (('J2K', "J2K", ""),
        ('JP2', "JP2", ""),
        ),
        name = 'JPEG 2000 Codec',
        default = 'J2K')
    camformatD_jpeg2k_cinema = bpy.props.BoolProperty(default=False)
    camformatD_jpeg2k_cinema48 = bpy.props.BoolProperty(default=False)
    camformatD_jpeg2k_ycc = bpy.props.BoolProperty(default=False)
        #DPX
    camformatD_dpx_log = bpy.props.BoolProperty(default=False)
        #OEXR
    camformatD_oexr_codec = bpy.props.EnumProperty(items = \
        (('NONE', "None", ""),
        ('PXR24', "Pxr24 (lossy)", ""),
        ('ZIP', "ZIP (lossless)", ""),
        ('PIZ', "PIZ (lossless)", ""),
        ('RLE', "RLE (lossless)", ""),
        ('ZIPS', "ZIPS (lossless)", ""),
        ('DWAA', "DWAA (lossless)", "")
        ),
        name = 'Open EXR Codec',
        default = 'NONE')
    camformatD_oexr_zbuffer = bpy.props.BoolProperty(default=False)
    camformatD_oexr_preview = bpy.props.BoolProperty(default=False)
        #TIFF
    camformatD_tiff_compression = bpy.props.EnumProperty(items = \
        (('NONE', "None", ""),
        ('DEFLATE', "Deflate", ""),
        ('LZW', "LZW", ""),
        ('PACKBITS', "Pack Bits", "")
        ),
        name = 'TIFF Compression',
        default = 'NONE')
    #Motion blur props
    camformatD_mblur_onoff = bpy.props.BoolProperty(default=False)
    camformatD_mblur_shutter = bpy.props.FloatProperty(default=0.5, min=0.01, max=2, step=1, precision=2)
        #internal
    camformatD_internal_mblur_samples = bpy.props.IntProperty(default=1, min=1, max=32)
        #cycles
    camformatD_cycles_mblur_position = bpy.props.EnumProperty(items = \
        (('START', "Start on Frame", ""),
        ('CENTER', "Center on Frame", ""),
        ('END', "End on Frame", ""),
        ),
        name = 'Motion Blur Position',
        default = 'CENTER')
    camformatD_cycles_mblur_shutter_type = bpy.props.EnumProperty(items = \
        (('NONE', "None", ""),
        ('TOP', "Top-Bottom", ""),
        ),
        name = 'Shutter Type',
        default = 'NONE')
    camformatD_cycles_mblur_rolling_shutter_duration = bpy.props.FloatProperty(default=0.1, min=0, max=1, step=3, precision=2)
    
            
    def draw(self, context):
        layout = self.layout
        
        box=layout.box()
        box.label('Settings', icon='SCRIPTWIN')
        row=box.row()
        row.prop(self, 'camformat_auto_update_from_cam')
        row.prop(self, 'camformat_live_update_from_cam')
        row=box.row()
        row.prop(self, 'camformat_create_cam_scene_settings')
        row=box.row()
        row.label('Properties to Store :')
        if self.camformat_dimension_settings==False and self.camformat_mblur_settings==False and self.camformat_output_settings==False:
            row.label('No Properties Stored !', icon='ERROR')
        row=box.row()
        row.prop(self, 'camformat_dimension_settings')
        row.prop(self, 'camformat_mblur_settings')
        row.prop(self, 'camformat_output_settings')
        
        box=layout.box()
        row=box.row()
        if self.camformat_default_cam_display==False:
            row.prop(self, 'camformat_default_cam_display', text='', icon='TRIA_RIGHT', emboss=False)
        else:
            row.prop(self, 'camformat_default_cam_display', text='', icon='TRIA_DOWN', emboss=False)
        row.label('Default Camera Settings', icon='CAMERA_DATA')
        if self.camformat_create_cam_scene_settings==True:
            row=box.row()
            row.label('Camera Creation with Scene settings enabled, Default Camera Settings will not apply', icon='ERROR')
            
        if self.camformat_default_cam_display==True:
            box.prop(self, 'camformatD_ui_menu', text='')
        
            
            if self.camformatD_ui_menu=='dimensions':
                split=box.split()
                
                col=split.column(align=True)
                col.label("Resolution:")
                col.prop(self, 'camformatD_res_x', text='X')
                col.prop(self, 'camformatD_res_y', text='Y')
                col.prop(self, 'camformatD_res_pct', text='', slider=True)
                
                col=split.column(align=True)
                col.label("Frame Range:")
                col.prop(self, 'camformatD_start_frame', text='Start Frame')
                col.prop(self, 'camformatD_end_frame', text='End Frame')
                col.prop(self, 'camformatD_frame_step', text='Frame Step')
                
                split=box.split()
                col=split.column(align=True)
                col.label("Aspect Ratio:")
                col.prop(self, 'camformatD_ratio_x', text='X')
                col.prop(self, 'camformatD_ratio_y', text='Y')
                
                col=split.column(align=True)
                col.label("Frame Rate:")
                col.prop(self, 'camformatD_fps', text='FPS')
                col.prop(self, 'camformatD_fps_base', text='/')
                
                split=box.split()
                
                col=split.column(align=True)
                col.label("Border:")
                row=col.row(align=True)
                row.prop(self, 'camformatD_border', text='Border')
                row.prop(self, 'camformatD_crop', text='Crop')
                row=col.row(align=True)
                row.label("Min")
                row.label("Max")
                row=col.row(align=True)
                row.prop(self, 'camformatD_border_min_x', text='X', slider=True)
                row.prop(self, 'camformatD_border_max_x', text='X', slider=True)
                row=col.row(align=True)
                row.prop(self, 'camformatD_border_min_y', text='Y', slider=True)
                row.prop(self, 'camformatD_border_max_y', text='Y', slider=True)
                
                col=split.column(align=True)
                col.label("Time Remapping:")
                col.prop(self, 'camformatD_frame_map_old', text='Old')
                col.prop(self, 'camformatD_frame_map_new', text='New')
                
            elif self.camformatD_ui_menu=='output':
                box.prop(self, 'camformatD_render_filepath', text='')
                
                split=box.split()
                col=split.column()
                col.prop(self, 'camformatD_overwrite', text='Overwrite')
                col.prop(self, 'camformatD_placeholders', text='Placeholders')
                col.prop(self, 'camformatD_file_format', text='')
                                
                col=split.column()
                col.prop(self, 'camformatD_file_extensions', text='File Extensions')
                col.prop(self, 'camformatD_cache_result', text='Cache result')
                if self.camformatD_file_format in {'IRIS', 'PNG', 'JPEG2000', 'TARGA', 'TARGA_RAW', 'DPX', 'OPEN_EXR','OPEN_EXR_MULTILAYER', 'TIFF'}:
                    col.prop(self, 'camformatD_color_mode', text='')
                else:
                    col.prop(self, 'camformatD_color_mode_simple', text='')
                
                if self.camformatD_file_format in {'PNG','TIFF'}:
                    box.prop(self, 'camformatD_color_depth_pngtiff', text='Color Depth')
                elif self.camformatD_file_format == 'JPEG2000':
                    box.prop(self, 'camformatD_color_depth_jpeg2000', text='Color Depth')
                elif self.camformatD_file_format == 'DPX':
                    box.prop(self, 'camformatD_color_depth_dpx', text='Color Depth')
                elif self.camformatD_file_format in {'OPEN_EXR','OPEN_EXR_MULTILAYER'}:
                    box.prop(self, 'camformatD_color_depth_oexr', text='Color Depth')
                    
                if self.camformatD_file_format == 'PNG':
                    box.prop(self, 'camformatD_compression', text='Compression', slider=True)
                if self.camformatD_file_format in {'JPEG','JPEG2000','AVI_JPEG'}:
                    box.prop(self, 'camformatD_quality', text='Quality', slider=True)
                
                if self.camformatD_file_format == 'JPEG2000':
                    box.prop(self, 'camformatD_jpeg2k_codec', text='Codec')
                    row=box.row()
                    row.prop(self, 'camformatD_jpeg2k_cinema', text='Cinema')
                    row.prop(self, 'camformatD_jpeg2k_cinema48', text='Cinema (48)')
                    row=box.row()
                    row.prop(self, 'camformatD_jpeg2k_ycc', text='YCC')
                    
                if self.camformatD_file_format == 'DPX':
                    box.prop(self, 'camformatD_dpx_log', text='Log')
                    
                if self.camformatD_file_format in {'OPEN_EXR', 'OPEN_EXR_MULTILAYER'}:
                    box.prop(self, 'camformatD_oexr_codec', text='Codec')
                    
                if self.camformatD_file_format == 'OPEN_EXR':
                    row=box.row()
                    row.prop(self, 'camformatD_oexr_zbuffer', text='Z Buffer')
                    row.prop(self, 'camformatD_oexr_preview', text='Preview')
                    
                if self.camformatD_file_format == 'TIFF':
                    box.prop(self, 'camformatD_tiff_compression', text='Compression')
                    
            elif self.camformatD_ui_menu=='motionblur':
                box.prop(self, 'camformatD_mblur_onoff', text='Motion Blur')
                box2=box.box()
                box2.label('Blender Render')
                                
                split=box2.split()
                
                col=split.column(align=True)
                col.prop(self, 'camformatD_internal_mblur_samples', text='Motion Samples')
                
                col=split.column(align=True)
                col.prop(self, 'camformatD_mblur_shutter', text='Shutter')
                
                box3=box.box()
                box3.label('Cycles Render')
                
                col=box3.column()
                col.prop(self, 'camformatD_cycles_mblur_position', text='Position')
                col.prop(self, 'camformatD_mblur_shutter', text='Shutter')
                col.separator()
                col.prop(self, 'camformatD_cycles_mblur_shutter_type', text='Shutter Type')
                row=col.row()
                if self.camformatD_cycles_mblur_shutter_type == 'NONE':
                    row.enabled = False # gray out button
                    row.prop(self, 'camformatD_cycles_mblur_rolling_shutter_duration', text='Rolling Shutter Duration')
                else:
                    row.prop(self, 'camformatD_cycles_mblur_rolling_shutter_duration', text='Rolling Shutter Duration')
        
        

# get addon preferences
def get_addon_preferences():
    addon_preferences = bpy.context.user_preferences.addons[__name__].preferences
    return addon_preferences


#######################################################################
### Update functions ###
#######################################################################

#update copy from cam for live edit
def update_copy_from_cam(self, context):
    addon_preferences = get_addon_preferences()
    live = addon_preferences.camformat_live_update_from_cam
    scene=bpy.context.scene
    active=bpy.context.active_object
    
    if live==True and active.type=='CAMERA':
        if scene.camera.name==active.name:
            bpy.ops.camformat.copy_from_cam()


#######################################################################
### Operators ###
#######################################################################

#copy render data
class CamFormatCopyFromRender(bpy.types.Operator):
    bl_idname = "camformat.copy_from_render"
    bl_label = "Copy from Render data"
    bl_description = "Copy Camera Format data from current Render data"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object.type=='CAMERA'
    
    def execute(self, context):
        addon_preferences = get_addon_preferences()
        live = addon_preferences.camformat_live_update_from_cam
        
        camname=context.active_object.name
        cam=context.active_object.data
        scene=bpy.context.scene
        render=scene.render
        
        chk_live=0
        
        if live==True:
            addon_preferences.camformat_live_update_from_cam=False
            chk_live=1
        
        if addon_preferences.camformat_dimension_settings==True:
            #Dimensions
            cam.camformat_res_x=render.resolution_x
            cam.camformat_res_y=render.resolution_y
            cam.camformat_start_frame=scene.frame_start
            cam.camformat_end_frame=scene.frame_end
            cam.camformat_res_pct=render.resolution_percentage
            cam.camformat_frame_step=scene.frame_step
            cam.camformat_ratio_x=render.pixel_aspect_x
            cam.camformat_ratio_y=render.pixel_aspect_y
            cam.camformat_fps=render.fps
            cam.camformat_fps_base=render.fps_base
            cam.camformat_border=render.use_border
            cam.camformat_crop=render.use_crop_to_border
            cam.camformat_border_min_x=render.border_min_x
            cam.camformat_border_min_y=render.border_min_y
            cam.camformat_border_max_x=render.border_max_x
            cam.camformat_border_max_y=render.border_max_y
            cam.camformat_frame_map_old=render.frame_map_old
            cam.camformat_frame_map_new=render.frame_map_new
        
        if addon_preferences.camformat_output_settings==True:
            #Output
            cam.camformat_render_filepath=render.filepath
            cam.camformat_overwrite=render.use_overwrite
            cam.camformat_file_extensions=render.use_file_extension
            cam.camformat_placeholders=render.use_placeholder
            cam.camformat_cache_result=render.use_render_cache
            cam.camformat_file_format=render.image_settings.file_format
            if render.image_settings.file_format in {'IRIS', 'PNG', 'JPEG2000', 'TARGA', 'TARGA_RAW', 'DPX', 'OPEN_EXR','OPEN_EXR_MULTILAYER', 'TIFF'}:
                cam.camformat_color_mode=render.image_settings.color_mode
            else:
                cam.camformat_color_mode_simple=render.image_settings.color_mode
                cam.camformat_color_mode=render.image_settings.color_mode
            if render.image_settings.file_format in {'PNG','TIFF'}:
                cam.camformat_color_depth_pngtiff=render.image_settings.color_depth
            elif render.image_settings.file_format == 'JPEG2000':
                cam.camformat_color_depth_jpeg2000=render.image_settings.color_depth
            elif render.image_settings.file_format == 'DPX':
                cam.camformat_color_depth_dpx=render.image_settings.color_depth
            elif render.image_settings.file_format in {'OPEN_EXR','OPEN_EXR_MULTILAYER'}:
                cam.camformat_color_depth_oexr=render.image_settings.color_depth
            cam.camformat_quality=render.image_settings.quality
            cam.camformat_compression=render.image_settings.compression
            cam.camformat_jpeg2k_codec=render.image_settings.jpeg2k_codec
            cam.camformat_jpeg2k_cinema=render.image_settings.use_jpeg2k_cinema_preset
            cam.camformat_jpeg2k_cinema48=render.image_settings.use_jpeg2k_cinema_48
            cam.camformat_jpeg2k_ycc=render.image_settings.use_jpeg2k_ycc
            cam.camformat_dpx_log=render.image_settings.use_cineon_log
            cam.camformat_oexr_codec=render.image_settings.exr_codec
            cam.camformat_oexr_zbuffer=render.image_settings.use_zbuffer
            cam.camformat_oexr_preview=render.image_settings.use_preview
            cam.camformat_tiff_compression=render.image_settings.tiff_codec
        
        if addon_preferences.camformat_mblur_settings==True:
            #Motion Blur
            cam.camformat_mblur_onoff=render.use_motion_blur
            cam.camformat_mblur_shutter=render.motion_blur_shutter
                #cycles
            cam.camformat_cycles_mblur_position=scene.cycles.motion_blur_position
            cam.camformat_cycles_mblur_shutter_type=scene.cycles.rolling_shutter_type
            cam.camformat_cycles_mblur_rolling_shutter_duration=scene.cycles.rolling_shutter_duration
                #internal
            cam.camformat_internal_mblur_samples=render.motion_blur_samples
        
        if chk_live==1:
            addon_preferences.camformat_live_update_from_cam=True
        
        print('CamFormat --- Data copied from Scene to '+camname)
        
        return {'FINISHED'}
    
#copy cam data
class CamFormatCopyFromCam(bpy.types.Operator):
    bl_idname = "camformat.copy_from_cam"
    bl_label = "Copy to Render data"
    bl_description = "Copy Camera Format data to current Render data"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object.type=='CAMERA'
    
    def execute(self, context):
        addon_preferences = get_addon_preferences()
        camname=context.active_object.name
        cam=context.active_object.data
        scene=bpy.context.scene
        render=scene.render
        
        if addon_preferences.camformat_dimension_settings==True:
            #Dimensions
            render.resolution_x=cam.camformat_res_x
            render.resolution_y=cam.camformat_res_y
            scene.frame_start=cam.camformat_start_frame
            scene.frame_end=cam.camformat_end_frame
            render.resolution_percentage=cam.camformat_res_pct
            scene.frame_step=cam.camformat_frame_step
            render.pixel_aspect_x=cam.camformat_ratio_x
            render.pixel_aspect_y=cam.camformat_ratio_y
            render.fps=cam.camformat_fps
            render.fps_base=cam.camformat_fps_base
            render.use_border=cam.camformat_border
            render.use_crop_to_border=cam.camformat_crop
            render.border_min_x=cam.camformat_border_min_x
            render.border_min_y=cam.camformat_border_min_y
            render.border_max_x=cam.camformat_border_max_x
            render.border_max_y=cam.camformat_border_max_y
            render.frame_map_old=cam.camformat_frame_map_old
            render.frame_map_new=cam.camformat_frame_map_new
        
        if addon_preferences.camformat_output_settings==True:
            #Output
            render.filepath=cam.camformat_render_filepath
            render.use_overwrite=cam.camformat_overwrite
            render.use_file_extension=cam.camformat_file_extensions
            render.use_placeholder=cam.camformat_placeholders
            render.use_render_cache=cam.camformat_cache_result
            render.image_settings.file_format=cam.camformat_file_format
            if cam.camformat_file_format in {'IRIS', 'PNG', 'JPEG2000', 'TARGA', 'TARGA_RAW', 'DPX', 'OPEN_EXR','OPEN_EXR_MULTILAYER', 'TIFF'}:
                render.image_settings.color_mode=cam.camformat_color_mode
            else:
                render.image_settings.color_mode=cam.camformat_color_mode_simple
            if cam.camformat_file_format in {'PNG','TIFF'}:
                render.image_settings.color_depth=cam.camformat_color_depth_pngtiff
            elif cam.camformat_file_format == 'JPEG2000':
                render.image_settings.color_depth=cam.camformat_color_depth_jpeg2000
            elif cam.camformat_file_format == 'DPX':
                render.image_settings.color_depth=cam.camformat_color_depth_dpx
            elif cam.camformat_file_format in {'OPEN_EXR','OPEN_EXR_MULTILAYER'}:
                render.image_settings.color_depth=cam.camformat_color_depth_oexr
            render.image_settings.quality=cam.camformat_quality
            render.image_settings.compression=cam.camformat_compression
            render.image_settings.jpeg2k_codec=cam.camformat_jpeg2k_codec
            render.image_settings.use_jpeg2k_cinema_preset=cam.camformat_jpeg2k_cinema
            render.image_settings.use_jpeg2k_cinema_48=cam.camformat_jpeg2k_cinema48
            render.image_settings.use_jpeg2k_ycc=cam.camformat_jpeg2k_ycc
            render.image_settings.use_cineon_log=cam.camformat_dpx_log
            render.image_settings.exr_codec=cam.camformat_oexr_codec
            render.image_settings.use_zbuffer=cam.camformat_oexr_zbuffer
            render.image_settings.use_preview=cam.camformat_oexr_preview
            render.image_settings.tiff_codec=cam.camformat_tiff_compression
        
        if addon_preferences.camformat_mblur_settings==True:
            #Motion Blur
            render.use_motion_blur=cam.camformat_mblur_onoff
            render.motion_blur_shutter=cam.camformat_mblur_shutter
                #cycles
            scene.cycles.motion_blur_position=cam.camformat_cycles_mblur_position
            scene.cycles.rolling_shutter_type=cam.camformat_cycles_mblur_shutter_type
            scene.cycles.rolling_shutter_duration=cam.camformat_cycles_mblur_rolling_shutter_duration
                #internal
            render.motion_blur_samples=cam.camformat_internal_mblur_samples
        
        #print('CamFormat --- Data copied from '+camname+' to Scene')
        
        return {'FINISHED'}
    
    
#copy from default prefs
class CamFormatCopyFromPrefs(bpy.types.Operator):
    bl_idname = "camformat.copy_from_prefs"
    bl_label = ""
    
    @classmethod
    def poll(cls, context):
        return context.active_object.type=='CAMERA'
    
    def execute(self, context):
        addon = get_addon_preferences()
        live = addon.camformat_live_update_from_cam
        
        camname=context.active_object.name
        cam=context.active_object.data
        scene=bpy.context.scene
        render=scene.render
        
        chk_live=0
        
        if live==True:
            addon.camformat_live_update_from_cam=False
            chk_live=1
        
        if addon.camformat_dimension_settings==True:
            #Dimensions
            cam.camformat_res_x=addon.camformatD_res_x
            cam.camformat_res_y=addon.camformatD_res_y
            cam.camformat_start_frame=addon.camformatD_start_frame
            cam.camformat_end_frame=addon.camformatD_end_frame
            cam.camformat_res_pct=addon.camformatD_res_pct
            cam.camformat_frame_step=addon.camformatD_frame_step
            cam.camformat_ratio_x=addon.camformatD_ratio_x
            cam.camformat_ratio_y=addon.camformatD_ratio_y
            cam.camformat_fps=addon.camformatD_fps
            cam.camformat_fps_base=addon.camformatD_fps_base
            cam.camformat_border=addon.camformatD_border
            cam.camformat_crop=addon.camformatD_crop
            cam.camformat_border_min_x=addon.camformatD_border_min_x
            cam.camformat_border_min_y=addon.camformatD_border_min_y
            cam.camformat_border_max_x=addon.camformatD_border_max_x
            cam.camformat_border_max_y=addon.camformatD_border_max_y
            cam.camformat_frame_map_old=addon.camformatD_frame_map_old
            cam.camformat_frame_map_new=addon.camformatD_frame_map_new
        
        if addon.camformat_output_settings==True:
            #Output
            cam.camformat_render_filepath=addon.camformatD_render_filepath
            cam.camformat_overwrite=addon.camformatD_overwrite
            cam.camformat_file_extensions=addon.camformatD_file_extensions
            cam.camformat_placeholders=addon.camformatD_placeholders
            cam.camformat_cache_result=addon.camformatD_cache_result
            cam.camformat_file_format=addon.camformatD_file_format
            cam.camformat_color_mode=addon.camformatD_color_mode
            cam.camformat_color_mode_simple=addon.camformatD_color_mode_simple
            cam.camformat_color_depth_pngtiff=addon.camformatD_color_depth_pngtiff
            cam.camformat_color_depth_jpeg2000=addon.camformatD_color_depth_jpeg2000
            cam.camformat_color_depth_dpx=addon.camformatD_color_depth_dpx
            cam.camformat_color_depth_oexr=addon.camformatD_color_depth_oexr
            cam.camformat_quality=addon.camformatD_quality
            cam.camformat_compression=addon.camformatD_compression
            cam.camformat_jpeg2k_codec=addon.camformatD_jpeg2k_codec
            cam.camformat_jpeg2k_cinema=addon.camformatD_jpeg2k_cinema
            cam.camformat_jpeg2k_cinema48=addon.camformatD_jpeg2k_cinema48
            cam.camformat_jpeg2k_ycc=addon.camformatD_jpeg2k_ycc
            cam.camformat_dpx_log=addon.camformatD_dpx_log
            cam.camformat_oexr_codec=addon.camformatD_oexr_codec
            cam.camformat_oexr_zbuffer=addon.camformatD_oexr_zbuffer
            cam.camformat_oexr_preview=addon.camformatD_oexr_preview
            cam.camformat_tiff_compression=addon.camformatD_tiff_compression
        
        if addon.camformat_mblur_settings==True:
            #Motion Blur
            cam.camformat_mblur_onoff=addon.camformatD_mblur_onoff
            cam.camformat_mblur_shutter=addon.camformatD_mblur_shutter
                #cycles
            cam.camformat_cycles_mblur_position=addon.camformatD_cycles_mblur_position
            cam.camformat_cycles_mblur_shutter_type=addon.camformatD_cycles_mblur_shutter_type
            cam.camformat_cycles_mblur_rolling_shutter_duration=addon.camformatD_cycles_mblur_rolling_shutter_duration
                #internal
            cam.camformat_internal_mblur_samples=addon.camformatD_internal_mblur_samples
        
        if chk_live==1:
            addon.camformat_live_update_from_cam=True
        
        print('CamFormat --- Data copied from Prefs to '+camname)
        
        return {'FINISHED'}
    

#######################################################################
### GUI ###
#######################################################################

# Draw camera panel
class CamFormatPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_label = "Output Format"
    
    @classmethod
    def poll(cls, context):
        return context.active_object.type=='CAMERA'

    def draw(self, context):
        addon_preferences = get_addon_preferences()
        dim=addon_preferences.camformat_dimension_settings
        mbl=addon_preferences.camformat_mblur_settings
        out=addon_preferences.camformat_output_settings
        
        scene=context.scene
        cam=context.active_object.data
        render=bpy.context.scene.render.engine
        
        layout = self.layout
                
        row=layout.row()
        row.label(icon='MODIFIER')
        row.operator("camformat.copy_from_render")
        row.operator("camformat.copy_from_cam")
        menu=''
        
        row=layout.row(align=True)
        if scene.camformat_ui_detail==False:
            row.prop(scene, 'camformat_ui_detail', text='', icon='TRIA_RIGHT', emboss=False)
            row.label("Details")
        else:
            row.prop(scene, 'camformat_ui_detail', text='', icon='TRIA_DOWN', emboss=False)
            row.label("Details")
            
            if dim==True and mbl==True and out==True:
                layout.prop(scene, 'camformat_ui_menu_full', expand=True)
                menu=scene.camformat_ui_menu_full
            elif dim==True and mbl==True:
                layout.prop(scene, 'camformat_ui_menu_D_MB', expand=True)
                menu=scene.camformat_ui_menu_D_MB
            elif dim==True and out==True:
                layout.prop(scene, 'camformat_ui_menu_D_O', expand=True)
                menu=scene.camformat_ui_menu_D_O
            elif mbl==True and out==True:
                layout.prop(scene, 'camformat_ui_menu_MB_O', expand=True)
                menu=scene.camformat_ui_menu_MB_O
            
            
            if menu=='dimensions' or menu=='' and dim==True:
                split=layout.split()
                
                col=split.column(align=True)
                col.label("Resolution:")
                col.prop(cam, 'camformat_res_x', text='X')
                col.prop(cam, 'camformat_res_y', text='Y')
                col.prop(cam, 'camformat_res_pct', text='', slider=True)
                
                col=split.column(align=True)
                col.label("Frame Range:")
                col.prop(cam, 'camformat_start_frame', text='Start Frame')
                col.prop(cam, 'camformat_end_frame', text='End Frame')
                col.prop(cam, 'camformat_frame_step', text='Frame Step')
                
                split=layout.split()
                col=split.column(align=True)
                col.label("Aspect Ratio:")
                col.prop(cam, 'camformat_ratio_x', text='X')
                col.prop(cam, 'camformat_ratio_y', text='Y')
                
                col=split.column(align=True)
                col.label("Frame Rate:")
                col.prop(cam, 'camformat_fps', text='FPS')
                col.prop(cam, 'camformat_fps_base', text='/')
                
                split=layout.split()
                
                col=split.column(align=True)
                col.label("Border:")
                row=col.row(align=True)
                row.prop(cam, 'camformat_border', text='Border')
                row.prop(cam, 'camformat_crop', text='Crop')
                row=col.row(align=True)
                row.label("Min")
                row.label("Max")
                row=col.row(align=True)
                row.prop(cam, 'camformat_border_min_x', text='X', slider=True)
                row.prop(cam, 'camformat_border_max_x', text='X', slider=True)
                row=col.row(align=True)
                row.prop(cam, 'camformat_border_min_y', text='Y', slider=True)
                row.prop(cam, 'camformat_border_max_y', text='Y', slider=True)
                
                col=split.column(align=True)
                col.label("Time Remapping:")
                col.prop(cam, 'camformat_frame_map_old', text='Old')
                col.prop(cam, 'camformat_frame_map_new', text='New')
                
            elif menu=='output' or menu=='' and out==True:
                layout.separator()
                layout.prop(cam, 'camformat_render_filepath', text='')
                
                split=layout.split()
                col=split.column()
                col.prop(cam, 'camformat_overwrite', text='Overwrite')
                col.prop(cam, 'camformat_placeholders', text='Placeholders')
                col.prop(cam, 'camformat_file_format', text='')
                                
                col=split.column()
                col.prop(cam, 'camformat_file_extensions', text='File Extensions')
                col.prop(cam, 'camformat_cache_result', text='Cache result')
                if cam.camformat_file_format in {'IRIS', 'PNG', 'JPEG2000', 'TARGA', 'TARGA_RAW', 'DPX', 'OPEN_EXR','OPEN_EXR_MULTILAYER', 'TIFF'}:
                    col.prop(cam, 'camformat_color_mode', text='')
                else:
                    col.prop(cam, 'camformat_color_mode_simple', text='')
                
                if cam.camformat_file_format in {'PNG','TIFF'}:
                    layout.prop(cam, 'camformat_color_depth_pngtiff', text='Color Depth', expand=True)
                elif cam.camformat_file_format == 'JPEG2000':
                    layout.prop(cam, 'camformat_color_depth_jpeg2000', text='Color Depth', expand=True)
                elif cam.camformat_file_format == 'DPX':
                    layout.prop(cam, 'camformat_color_depth_dpx', text='Color Depth', expand=True)
                elif cam.camformat_file_format in {'OPEN_EXR','OPEN_EXR_MULTILAYER'}:
                    layout.prop(cam, 'camformat_color_depth_oexr', text='Color Depth', expand=True)
                    
                if cam.camformat_file_format == 'PNG':
                    layout.prop(cam, 'camformat_compression', text='Compression', slider=True)
                if cam.camformat_file_format in {'JPEG','JPEG2000','AVI_JPEG'}:
                    layout.prop(cam, 'camformat_quality', text='Quality', slider=True)
                
                if cam.camformat_file_format == 'JPEG2000':
                    layout.prop(cam, 'camformat_jpeg2k_codec', text='Codec')
                    row=layout.row()
                    row.prop(cam, 'camformat_jpeg2k_cinema', text='Cinema')
                    row.prop(cam, 'camformat_jpeg2k_cinema48', text='Cinema (48)')
                    row=layout.row()
                    row.prop(cam, 'camformat_jpeg2k_ycc', text='YCC')
                    
                if cam.camformat_file_format == 'DPX':
                    layout.prop(cam, 'camformat_dpx_log', text='Log')
                    
                if cam.camformat_file_format in {'OPEN_EXR', 'OPEN_EXR_MULTILAYER'}:
                    layout.prop(cam, 'camformat_oexr_codec', text='Codec')
                    
                if cam.camformat_file_format == 'OPEN_EXR':
                    row=layout.row()
                    row.prop(cam, 'camformat_oexr_zbuffer', text='Z Buffer')
                    row.prop(cam, 'camformat_oexr_preview', text='Preview')
                    
                if cam.camformat_file_format == 'TIFF':
                    layout.prop(cam, 'camformat_tiff_compression', text='Compression')
                    
            elif menu=='motionblur' or menu=='' and mbl==True:
                if render == 'BLENDER_RENDER':
                    layout.separator()
                    layout.prop(cam, 'camformat_mblur_onoff', text='Sampled Motion Blur')
                    
                    split=layout.split()
                    
                    col=split.column(align=True)
                    col.prop(cam, 'camformat_internal_mblur_samples', text='Motion Samples')
                    
                    col=split.column(align=True)
                    col.prop(cam, 'camformat_mblur_shutter', text='Shutter')
                elif render == 'CYCLES':
                    layout.separator()
                    layout.prop(cam, 'camformat_mblur_onoff', text='Motion Blur')
                    
                    col=layout.column()
                    col.prop(cam, 'camformat_cycles_mblur_position', text='Position')
                    col.prop(cam, 'camformat_mblur_shutter', text='Shutter')
                    col.separator()
                    col.prop(cam, 'camformat_cycles_mblur_shutter_type', text='Shutter Type')
                    row=col.row()
                    if cam.camformat_cycles_mblur_shutter_type == 'NONE':
                        row.enabled = False # gray out button
                        row.prop(cam, 'camformat_cycles_mblur_rolling_shutter_duration', text='Rolling Shutter Duration')
                    else:
                        row.prop(cam, 'camformat_cycles_mblur_rolling_shutter_duration', text='Rolling Shutter Duration')
                    
                    
#######################################################################
### handlers ###
#######################################################################

@persistent
def cam_update(context):
    #get addon prefs
    addon_preferences = get_addon_preferences()
    
    #set scene output from cameras
    auto_change = addon_preferences.camformat_auto_update_from_cam
    if auto_change==True:
        if bpy.context.scene.camera is not None:
            if bpy.context.scene.camformat_last_cam != bpy.context.scene.camera.name:
                bpy.context.scene.camformat_last_cam = bpy.context.scene.camera.name
                bpy.ops.camformat.copy_from_cam()
    
    #set camera when created
    settings_creation = addon_preferences.camformat_create_cam_scene_settings
    obj=bpy.context.scene.objects
    cams=bpy.data.cameras
    if bpy.context.scene.camformat_last_obj_number!=len(obj):
        bpy.context.scene.camformat_last_obj_number=len(obj)
        if bpy.context.scene.camformat_last_cam_number!=len(cams):
            bpy.context.scene.camformat_last_cam_number=len(cams)
            if bpy.context.active_object.type=='CAMERA':
                if settings_creation==True:
                    bpy.ops.camformat.copy_from_render()
                else:
                    bpy.ops.camformat.copy_from_prefs()
                
        

#######################################################################
### reg/unreg ###
#######################################################################
            
def register():
    bpy.utils.register_class(CamFormatAddonPrefs)
    bpy.utils.register_class(CamFormatCopyFromRender)
    bpy.utils.register_class(CamFormatCopyFromCam)
    bpy.utils.register_class(CamFormatCopyFromPrefs)
    bpy.utils.register_class(CamFormatPanel)
    
    #check for lasts obj props
    bpy.types.Scene.camformat_last_cam = bpy.props.StringProperty()
    bpy.types.Scene.camformat_last_obj_number = bpy.props.IntProperty()
    bpy.types.Scene.camformat_last_cam_number = bpy.props.IntProperty()
    #UI props
    bpy.types.Scene.camformat_ui_detail = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.camformat_ui_menu_full = bpy.props.EnumProperty(items = \
        (('dimensions', "Dimensions", "Dimensions Settings"),
        ('motionblur', "Motion Blur", "Motion Blur Settings"),
        ('output', "Output", "Output Settings"),
        ),
        default = 'dimensions',
        )
    bpy.types.Scene.camformat_ui_menu_D_MB = bpy.props.EnumProperty(items = \
        (('dimensions', "Dimensions", "Dimensions Settings"),
        ('motionblur', "Motion Blur", "Motion Blur Settings"),
        ),
        default = 'dimensions',
        )
    bpy.types.Scene.camformat_ui_menu_D_O = bpy.props.EnumProperty(items = \
        (('dimensions', "Dimensions", "Dimensions Settings"),
        ('output', "Output", "Output Settings"),
        ),
        default = 'dimensions',
        )
    bpy.types.Scene.camformat_ui_menu_MB_O = bpy.props.EnumProperty(items = \
        (('motionblur', "Motion Blur", "Motion Blur Settings"),
        ('output', "Output", "Output Settings"),
        ),
        default = 'motionblur',
        )
        
    #Dimension props
    bpy.types.Camera.camformat_res_x = bpy.props.IntProperty(default=1920, min=4, max=65536, update=update_copy_from_cam)
    bpy.types.Camera.camformat_res_y = bpy.props.IntProperty(default=1080, min=4, max=65536, update=update_copy_from_cam) 
    bpy.types.Camera.camformat_start_frame = bpy.props.IntProperty(default=1, min=0, max=1048574, update=update_copy_from_cam)
    bpy.types.Camera.camformat_end_frame = bpy.props.IntProperty(default=250, min=0, max=1048574, update=update_copy_from_cam)
    bpy.types.Camera.camformat_res_pct = bpy.props.IntProperty(default=50, min=1, max=32767, subtype='PERCENTAGE', update=update_copy_from_cam)
    bpy.types.Camera.camformat_frame_step = bpy.props.IntProperty(default=1, min=1, max=100, update=update_copy_from_cam)
    bpy.types.Camera.camformat_ratio_x = bpy.props.FloatProperty(default=1, min=1, max=200, step=10, precision=3, update=update_copy_from_cam)
    bpy.types.Camera.camformat_ratio_y = bpy.props.FloatProperty(default=1, min=1, max=200, step=10, precision=3, update=update_copy_from_cam)
    bpy.types.Camera.camformat_fps = bpy.props.IntProperty(default=25, min=1, max=120, update=update_copy_from_cam)
    bpy.types.Camera.camformat_fps_base = bpy.props.FloatProperty(default=1, min=0.1, max=120, step=10, precision=3, update=update_copy_from_cam)
    bpy.types.Camera.camformat_border = bpy.props.BoolProperty(default=False, update=update_copy_from_cam)
    bpy.types.Camera.camformat_crop = bpy.props.BoolProperty(default=False, update=update_copy_from_cam)
    bpy.types.Camera.camformat_border_min_x = bpy.props.FloatProperty(default=0, min=0, max=1, step=10, precision=3, update=update_copy_from_cam)
    bpy.types.Camera.camformat_border_min_y = bpy.props.FloatProperty(default=0, min=0, max=1, step=10, precision=3, update=update_copy_from_cam)
    bpy.types.Camera.camformat_border_max_x = bpy.props.FloatProperty(default=1, min=0, max=1, step=10, precision=3, update=update_copy_from_cam)
    bpy.types.Camera.camformat_border_max_y = bpy.props.FloatProperty(default=1, min=0, max=1, step=10, precision=3, update=update_copy_from_cam)
    bpy.types.Camera.camformat_frame_map_old = bpy.props.IntProperty(default=100, min=1, max=900, update=update_copy_from_cam)
    bpy.types.Camera.camformat_frame_map_new = bpy.props.IntProperty(default=100, min=1, max=900, update=update_copy_from_cam)
    
    #Output props
    bpy.types.Camera.camformat_render_filepath = bpy.props.StringProperty(
        default="//",
        subtype='FILE_PATH',
        update=update_copy_from_cam)
    bpy.types.Camera.camformat_overwrite = bpy.props.BoolProperty(default=True, update=update_copy_from_cam)
    bpy.types.Camera.camformat_file_extensions = bpy.props.BoolProperty(default=True, update=update_copy_from_cam)
    bpy.types.Camera.camformat_placeholders = bpy.props.BoolProperty(default=False, update=update_copy_from_cam)
    bpy.types.Camera.camformat_cache_result = bpy.props.BoolProperty(default=False, update=update_copy_from_cam)
    bpy.types.Camera.camformat_file_format = bpy.props.EnumProperty(items = \
        (('BMP', "BMP", "Bitmap", 'IMAGE_DATA', 0),
        ('IRIS', "Iris", "SGI Iris", 'IMAGE_DATA', 1),
        ('PNG', "PNG", "Portable Network Graphics", 'IMAGE_DATA', 3),
        ('JPEG', "JPEG", "Joint Photographic Experts Group", 'IMAGE_DATA', 4),
        ('JPEG2000', "JPEG 2000", "Joint Photographic Experts Group 2000", 'IMAGE_DATA', 5),
        ('TARGA', "Targa", "Truevision Targa", 'IMAGE_DATA', 6),
        ('TARGA_RAW', "Targa Raw", "Truevision Targa Raw", 'IMAGE_DATA', 7),
        ('CINEON', "Cineon", "Cineon Image File", 'IMAGE_DATA', 8),
        ('DPX', "DPX", "Digital Picture Exchange", 'IMAGE_DATA', 9),
        ('OPEN_EXR_MULTILAYER', "OpenEXR Multilayer", "OpenEXR Multilayer", 'IMAGE_DATA', 10),
        ('OPEN_EXR', "OpenEXR", "OpenEXR", 'IMAGE_DATA', 11),
        ('HDR', "Radiance HDR", "Radiance High Dynamic Range File", 'IMAGE_DATA', 12),
        ('TIFF', "TIFF", "Tagged Image File Format", 'IMAGE_DATA', 13),
        ('AVI_JPEG', "AVI JPEG", "AVI JPEG Movie", 'FILE_MOVIE', 14),
        ('AVI_RAW', "AVI Raw", "AVI Raw Movie", 'FILE_MOVIE', 15),
        ('FRAMESERVER', "Frame Server", "Frame Server", 'FILE_SCRIPT', 16),
        ('FFMPEG', "FFmpeg video", "FFmpeg Movie", 'FILE_MOVIE', 17),
        ),
        name = 'Output Format',
        default = 'PNG',
        update=update_copy_from_cam)
    bpy.types.Camera.camformat_color_mode_simple = bpy.props.EnumProperty(items = \
        (('BW', "BW", "Black and White"),
        ('RGB', "RGB", "Red Green Blue"),
        ),
        name = 'Color Mode',
        default = 'RGB',
        update=update_copy_from_cam)
    bpy.types.Camera.camformat_color_mode = bpy.props.EnumProperty(items = \
        (('BW', "BW", "Black and White"),
        ('RGB', "RGB", "Red Green Blue"),
        ('RGBA', "RGBA", "Red Green Blue Alpha"),
        ),
        name = 'Color Mode',
        default = 'RGB',
        update=update_copy_from_cam)
    bpy.types.Camera.camformat_color_depth_pngtiff = bpy.props.EnumProperty(items = \
        (('8', "8", "8 bits"),
        ('16', "16", "16 bits"),
        ),
        name = 'Color Depth',
        default = '8',
        update=update_copy_from_cam)
    bpy.types.Camera.camformat_color_depth_jpeg2000 = bpy.props.EnumProperty(items = \
        (('8', "8", "8 bits"),
        ('12', "12", "12 bits"),
        ('16', "16", "16 bits"),
        ),
        name = 'Color Depth',
        default = '8',
        update=update_copy_from_cam)
    bpy.types.Camera.camformat_color_depth_dpx = bpy.props.EnumProperty(items = \
        (('8', "8", "8 bits"),
        ('10', "10", "10 bits"),
        ('12', "12", "12 bits"),
        ('16', "16", "16 bits"),
        ),
        default = '8',
        update=update_copy_from_cam)
    bpy.types.Camera.camformat_color_depth_oexr = bpy.props.EnumProperty(items = \
        (('16', "Float (Half)", "Float (Half)"),
        ('32', "Float (Full)", "Float (Full)"),
        ),
        name = 'Color Depth',
        default = '16',
        update=update_copy_from_cam)
    bpy.types.Camera.camformat_quality = bpy.props.IntProperty(default=90, min=0, max=100, subtype='PERCENTAGE', update=update_copy_from_cam)
    bpy.types.Camera.camformat_compression = bpy.props.IntProperty(default=15, min=0, max=100, subtype='PERCENTAGE', update=update_copy_from_cam)
        #jpeg 2000
    bpy.types.Camera.camformat_jpeg2k_codec = bpy.props.EnumProperty(items = \
        (('J2K', "J2K", ""),
        ('JP2', "JP2", ""),
        ),
        name = 'JPEG 2000 Codec',
        default = 'J2K',
        update=update_copy_from_cam)
    bpy.types.Camera.camformat_jpeg2k_cinema = bpy.props.BoolProperty(default=False, update=update_copy_from_cam)
    bpy.types.Camera.camformat_jpeg2k_cinema48 = bpy.props.BoolProperty(default=False, update=update_copy_from_cam)
    bpy.types.Camera.camformat_jpeg2k_ycc = bpy.props.BoolProperty(default=False, update=update_copy_from_cam)
        #DPX
    bpy.types.Camera.camformat_dpx_log = bpy.props.BoolProperty(default=False, update=update_copy_from_cam)
        #OEXR
    bpy.types.Camera.camformat_oexr_codec = bpy.props.EnumProperty(items = \
        (('NONE', "None", ""),
        ('PXR24', "Pxr24 (lossy)", ""),
        ('ZIP', "ZIP (lossless)", ""),
        ('PIZ', "PIZ (lossless)", ""),
        ('RLE', "RLE (lossless)", ""),
        ('ZIPS', "ZIPS (lossless)", ""),
        ('DWAA', "DWAA (lossless)", "")
        ),
        name = 'Open EXR Codec',
        default = 'NONE',
        update=update_copy_from_cam)
    bpy.types.Camera.camformat_oexr_zbuffer = bpy.props.BoolProperty(default=False, update=update_copy_from_cam)
    bpy.types.Camera.camformat_oexr_preview = bpy.props.BoolProperty(default=False, update=update_copy_from_cam)
        #TIFF
    bpy.types.Camera.camformat_tiff_compression = bpy.props.EnumProperty(items = \
        (('NONE', "None", ""),
        ('DEFLATE', "Deflate", ""),
        ('LZW', "LZW", ""),
        ('PACKBITS', "Pack Bits", "")
        ),
        name = 'TIFF Codec',
        default = 'NONE',
        update=update_copy_from_cam)
        
    #Motion blur props
    bpy.types.Camera.camformat_mblur_onoff = bpy.props.BoolProperty(default=False, update=update_copy_from_cam)
    bpy.types.Camera.camformat_mblur_shutter = bpy.props.FloatProperty(default=0.5, min=0.01, max=2, step=1, precision=2, update=update_copy_from_cam)
        #internal
    bpy.types.Camera.camformat_internal_mblur_samples = bpy.props.IntProperty(default=1, min=1, max=32, update=update_copy_from_cam)
        #cycles
    bpy.types.Camera.camformat_cycles_mblur_position = bpy.props.EnumProperty(items = \
        (('START', "Start on Frame", ""),
        ('CENTER', "Center on Frame", ""),
        ('END', "End on Frame", ""),
        ),
        name = 'Motion Blur Position',
        default = 'CENTER',
        update=update_copy_from_cam)
    bpy.types.Camera.camformat_cycles_mblur_shutter_type = bpy.props.EnumProperty(items = \
        (('NONE', "None", ""),
        ('TOP', "Top-Bottom", ""),
        ),
        name = 'Shutter Type',
        default = 'NONE',
        update=update_copy_from_cam)
    bpy.types.Camera.camformat_cycles_mblur_rolling_shutter_duration = bpy.props.FloatProperty(default=0.1, min=0, max=1, step=3, precision=2, update=update_copy_from_cam)
        
    #handler
    bpy.app.handlers.scene_update_post.append(cam_update)
                     
def unregister():
    bpy.utils.unregister_class(CamFormatAddonPrefs)
    bpy.utils.unregister_class(CamFormatCopyFromRender)
    bpy.utils.unregister_class(CamFormatCopyFromCam)
    bpy.utils.unregister_class(CamFormatCopyFromPrefs)
    bpy.utils.unregister_class(CamFormatPanel)
    
    #check for lasts obj props
    del bpy.types.Scene.camformat_last_cam
    del bpy.types.Scene.camformat_last_obj_number
    del bpy.types.Scene.camformat_last_cam_number
    #UI props
    del bpy.types.Scene.camformat_ui_detail
    del bpy.types.Scene.camformat_ui_menu_full
    del bpy.types.Scene.camformat_ui_menu_D_MB
    del bpy.types.Scene.camformat_ui_menu_D_O
    del bpy.types.Scene.camformat_ui_menu_MB_O
    
    #Dimension props
    del bpy.types.Camera.camformat_res_x
    del bpy.types.Camera.camformat_res_y
    del bpy.types.Camera.camformat_start_frame
    del bpy.types.Camera.camformat_end_frame
    del bpy.types.Camera.camformat_res_pct
    del bpy.types.Camera.camformat_frame_step
    del bpy.types.Camera.camformat_ratio_x
    del bpy.types.Camera.camformat_ratio_y
    del bpy.types.Camera.camformat_fps
    del bpy.types.Camera.camformat_fps_base
    del bpy.types.Camera.camformat_border
    del bpy.types.Camera.camformat_crop
    del bpy.types.Camera.camformat_border_min_x
    del bpy.types.Camera.camformat_border_max_x
    del bpy.types.Camera.camformat_border_min_y
    del bpy.types.Camera.camformat_border_max_y
    del bpy.types.Camera.camformat_frame_map_old
    del bpy.types.Camera.camformat_frame_map_new
    
    #Output Props
    del bpy.types.Camera.camformat_render_filepath
    del bpy.types.Camera.camformat_overwrite
    del bpy.types.Camera.camformat_file_extensions
    del bpy.types.Camera.camformat_placeholders
    del bpy.types.Camera.camformat_cache_result
    del bpy.types.Camera.camformat_file_format
    del bpy.types.Camera.camformat_color_mode_simple
    del bpy.types.Camera.camformat_color_mode
    del bpy.types.Camera.camformat_color_depth_pngtiff
    del bpy.types.Camera.camformat_color_depth_jpeg2000
    del bpy.types.Camera.camformat_color_depth_dpx
    del bpy.types.Camera.camformat_color_depth_oexr
    del bpy.types.Camera.camformat_quality
    del bpy.types.Camera.camformat_compression
        #JPEG 2000
    del bpy.types.Camera.camformat_jpeg2k_codec
    del bpy.types.Camera.camformat_jpeg2k_cinema
    del bpy.types.Camera.camformat_jpeg2k_cinema48
    del bpy.types.Camera.camformat_jpeg2k_ycc
        #DPX
    del bpy.types.Camera.camformat_dpx_log
        #OEXR
    del bpy.types.Camera.camformat_oexr_codec
    del bpy.types.Camera.camformat_oexr_zbuffer
    del bpy.types.Camera.camformat_oexr_preview
        #TIFF
    del bpy.types.Camera.camformat_tiff_compression
    
    #motion blur props
    del bpy.types.Camera.camformat_mblur_onoff
    del bpy.types.Camera.camformat_mblur_shutter
        #internal
    del bpy.types.Camera.camformat_internal_mblur_samples
        #cycles
    del bpy.types.Camera.camformat_cycles_mblur_position
    del bpy.types.Camera.camformat_cycles_mblur_shutter_type
    del bpy.types.Camera.camformat_cycles_mblur_rolling_shutter_duration
    
        
    #handler
    bpy.app.handlers.scene_update_post.remove(cam_update)
    
if __name__ == "__main__":
    register()