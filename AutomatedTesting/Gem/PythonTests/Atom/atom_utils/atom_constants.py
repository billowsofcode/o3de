"""
Copyright (c) Contributors to the Open 3D Engine Project.
For complete copyright and license terms please see the LICENSE at the root of this distribution.

SPDX-License-Identifier: Apache-2.0 OR MIT

Holds constants used across both hydra and non-hydra scripts.
"""

# Light type options for the Light component.
LIGHT_TYPES = {
    'unknown': 0,
    'sphere': 1,
    'spot_disk': 2,
    'capsule': 3,
    'quad': 4,
    'polygon': 5,
    'simple_point': 6,
    'simple_spot': 7,
}

# Intensity mode options for the Light component.
INTENSITY_MODE = {
    'Candela': 0,
    'Lumen': 1,
    'Ev100': 3,
    'Nit': 5,
}

# Attenuation Radius Mode options for the Light component.
ATTENUATION_RADIUS_MODE = {
    'explicit': 0,
    'automatic': 1,
}

# Shadow Map Size options for the Light component.
SHADOWMAP_SIZE = {
    'Size256': 256,
    'Size512': 512,
    'Size1024': 1024,
    'Size2048': 2048,
}

# Shadow filter method options for the Light component.
SHADOW_FILTER_METHOD = {
    'PCF': 1,
    'ESM': 2,
    'PCF+ESM': 3,
    'None': 0,
}

# Qualiity Level settings for Diffuse Global Illumination level component
GLOBAL_ILLUMINATION_QUALITY = {
    'Low': 0,
    'Medium': 1,
    'High': 2,
}

# Mesh LOD type
MESH_LOD_TYPE = {
    'default': 0,
    'screen coverage': 1,
    'specific lod': 2,
}

# Level list used in Editor Level Load Test
# WARNING: "Sponza" level is sandboxed due to an intermittent failure.
LEVEL_LIST = ["hermanubis", "hermanubis_high", "macbeth_shaderballs", "PbrMaterialChart", "ShadowTest"]


class AtomComponentProperties:
    """
    Holds Atom component related constants
    """

    @staticmethod
    def actor(property: str = 'name') -> str:
        """
        Actor component properties.
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Actor',
        }
        return properties[property]

    @staticmethod
    def bloom(property: str = 'name') -> str:
        """
        Bloom component properties. Requires PostFX Layer component.
          - 'requires' a list of component names as strings required by this component.
            Use editor_entity_utils EditorEntity.add_components(list) to add this list of requirements.\n
          - 'Enable Bloom' Toggle active state of the component True/False
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Bloom',
            'requires': [AtomComponentProperties.postfx_layer()],
            'Enable Bloom': 'Controller|Configuration|Enable Bloom',
        }
        return properties[property]

    @staticmethod
    def camera(property: str = 'name') -> str:
        """
        Camera component properties.
          - 'Field of view': Sets the value for the camera's FOV (Field of View) in degrees, i.e. 60.0
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Camera',
            'Field of view': 'Controller|Configuration|Field of view'
        }
        return properties[property]

    @staticmethod
    def decal(property: str = 'name') -> str:
        """
        Decal component properties.
          - 'Attenuation Angle' controls how much the angle between geometry and decal impacts opacity. 0-1 Radians
          - 'Opacity' where one is opaque and zero is transparent
          - 'Sort Key' 0-255 stacking z-sort like key to define which decal is on top of another
          - 'Material' the material Asset.id of the decal.
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Decal',
            'Attenuation Angle': 'Controller|Configuration|Attenuation Angle',
            'Opacity': 'Controller|Configuration|Opacity',
            'Sort Key': 'Controller|Configuration|Sort Key',
            'Material': 'Controller|Configuration|Material',
        }
        return properties[property]

    @staticmethod
    def deferred_fog(property: str = 'name') -> str:
        """
        Deferred Fog component properties. Requires PostFX Layer component.
          - 'requires' a list of component names as strings required by this component.
            Use editor_entity_utils EditorEntity.add_components(list) to add this list of requirements.\n
          - 'Enable Deferred Fog' Toggle active state of the component True/False
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Deferred Fog',
            'requires': [AtomComponentProperties.postfx_layer()],
            'Enable Deferred Fog': 'Controller|Configuration|Enable Deferred Fog',
        }
        return properties[property]

    @staticmethod
    def depth_of_field(property: str = 'name') -> str:
        """
        Depth of Field component properties. Requires PostFX Layer component.
          - 'requires' a list of component names as strings required by this component.
            Use editor_entity_utils EditorEntity.add_components(list) to add this list of requirements.\n
          - 'Camera Entity' an EditorEntity.id reference to the Camera component required for this effect.
            Must be a different entity than the one which hosts Depth of Field component.\n
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'DepthOfField',
            'requires': [AtomComponentProperties.postfx_layer()],
            'Camera Entity': 'Controller|Configuration|Camera Entity',
        }
        return properties[property]

    @staticmethod
    def diffuse_global_illumination(property: str = 'name') -> str:
        """
        Diffuse Global Illumination level component properties.
        Controls global settings for Diffuse Probe Grid components.
          - 'Quality Level' from atom_constants.py GLOBAL_ILLUMINATION_QUALITY
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Diffuse Global Illumination',
            'Quality Level': 'Controller|Configuration|Quality Level'
        }
        return properties[property]

    @staticmethod
    def diffuse_probe_grid(property: str = 'name') -> str:
        """
        Diffuse Probe Grid component properties. Requires one of 'shapes'.
          - 'shapes' a list of supported shapes as component names.
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Diffuse Probe Grid',
            'shapes': ['Axis Aligned Box Shape', 'Box Shape']
        }
        return properties[property]

    @staticmethod
    def directional_light(property: str = 'name') -> str:
        """
        Directional Light component properties.
          - 'Camera' an EditorEntity.id reference to the Camera component that controls cascaded shadow view frustum.
            Must be a different entity than the one which hosts Directional Light component.\n
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Directional Light',
            'Camera': 'Controller|Configuration|Shadow|Camera',
        }
        return properties[property]

    @staticmethod
    def display_mapper(property: str = 'name') -> str:
        """
        Display Mapper level component properties.
          - 'Enable LDR color grading LUT' toggles the use of LDR color grading LUT
          - 'LDR color Grading LUT' is the Low Definition Range (LDR) color grading for Look-up Textures (LUT) which is
            an Asset.id value corresponding to a lighting asset file.
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Display Mapper',
            'Enable LDR color grading LUT': 'Controller|Configuration|Enable LDR color grading LUT',
            'LDR color Grading LUT': 'Controller|Configuration|LDR color Grading LUT',
        }
        return properties[property]

    @staticmethod
    def entity_reference(property: str = 'name') -> str:
        """
        Entity Reference component properties.
          - 'EntityIdReferences' component container of entityId references. Initially empty.
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Entity Reference',
            'EntityIdReferences': 'Controller|Configuration|EntityIdReferences',
        }
        return properties[property]

    @staticmethod
    def exposure_control(property: str = 'name') -> str:
        """
        Exposure Control component properties. Requires PostFX Layer component.
          - 'requires' a list of component names as strings required by this component.
            Use editor_entity_utils EditorEntity.add_components(list) to add this list of requirements.\n
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Exposure Control',
            'requires': [AtomComponentProperties.postfx_layer()],
        }
        return properties[property]

    @staticmethod
    def global_skylight(property: str = 'name') -> str:
        """
        Global Skylight (IBL) component properties.
          - 'Diffuse Image' Asset.id for the cubemap image for determining diffuse lighting.
          - 'Specular Image' Asset.id for the cubemap image for determining specular lighting.
          - 'Exposure' Exposure setting for Global Skylight, value range is -5 to 5
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Global Skylight (IBL)',
            'Diffuse Image': 'Controller|Configuration|Diffuse Image',
            'Specular Image': 'Controller|Configuration|Specular Image',
            'Exposure': 'Controller|Configuration|Exposure',
        }
        return properties[property]

    @staticmethod
    def grid(property: str = 'name') -> str:
        """
        Grid component properties.
          - 'Grid Size': The size of the grid, default value is 32
          - 'Secondary Grid Spacing': The spacing value for the secondary grid, i.e. 1.0
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Grid',
            'Grid Size': 'Controller|Configuration|Grid Size',
            'Secondary Grid Spacing': 'Controller|Configuration|Secondary Grid Spacing',
        }
        return properties[property]

    @staticmethod
    def hdr_color_grading(property: str = 'name') -> str:
        """
        HDR Color Grading component properties. Requires PostFX Layer component.
          - 'requires' a list of component names as strings required by this component.
            Use editor_entity_utils EditorEntity.add_components(list) to add this list of requirements.\n
          - 'Enable HDR color grading' Toggle active state of the component True/False
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'HDR Color Grading',
            'requires': [AtomComponentProperties.postfx_layer()],
            'Enable HDR color grading': 'Controller|Configuration|Enable HDR color grading',
        }
        return properties[property]

    @staticmethod
    def hdri_skybox(property: str = 'name') -> str:
        """
        HDRi Skybox component properties.
          - 'Cubemap Texture': Asset.id for the cubemap texture to set.
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'HDRi Skybox',
            'Cubemap Texture': 'Controller|Configuration|Cubemap Texture',
        }
        return properties[property]

    @staticmethod
    def light(property: str = 'name') -> str:
        """
        Light component properties.
          - 'Light type' from atom_constants.py LIGHT_TYPES
          - 'Color' the RGBA value to set for the color of the light using azlmbr.math.Color tuple.
          - 'Intensity mode' from atom_constants.py INTENSITY_MODE
          - 'Intensity' the intensity of the light in the set photometric unit (float with no ceiling).
          - 'Attenuation radius Mode' from atom_constants.py ATTENUATION_RADIUS_MODE
          - 'Attenuation radius Radius' sets the distance at which the light no longer has effect.
          - 'Enable shadow' toggle for enabling shadows for the light.
          - 'Shadows Bias' how deep in shadow a surface must be before being affected by it (Range 0-100).
          - 'Normal Shadow Bias' reduces shadow acne (Range 0-10).
          - 'Shadowmap size' from atom_constants.py SHADOWMAP_SIZE
          - 'Shadow filter method' from atom_constants.py SHADOW_FILTER_METHOD
          - 'Filtering sample count' smooths/hardens shadow edges - specific to PCF & ESM+PCF (Range 4-64).
          - 'ESM exponent' smooths/hardens shadow edges - specific to ESM & ESM+PCF (Range 50-5000).
          - 'Enable shutters' toggle for enabling shutters for the light.
          - 'Inner angle' inner angle value for the shutters (in degrees) (Range 0.5-90).
          - 'Outer angle' outer angle value for the shutters (in degrees) (Range 0.5-90).
          - 'Both directions' Enables/Disables light emitting from both sides of a surface.
          - 'Fast approximation' Enables/Disables fast approximation of linear transformed cosines.
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Light',
            'Light type': 'Controller|Configuration|Light type',
            'Color': 'Controller|Configuration|Color',
            'Intensity mode': 'Controller|Configuration|Intensity mode',
            'Intensity': 'Controller|Configuration|Intensity',
            'Attenuation radius Mode': 'Controller|Configuration|Attenuation radius|Mode',
            'Attenuation radius Radius': 'Controller|Configuration|Attenuation radius|Radius',
            'Enable shadow': 'Controller|Configuration|Shadows|Enable shadow',
            'Shadows Bias': 'Controller|Configuration|Shadows|Bias',
            'Normal shadow bias': 'Controller|Configuration|Shadows|Normal Shadow Bias\n',
            'Shadowmap size': 'Controller|Configuration|Shadows|Shadowmap size',
            'Shadow filter method': 'Controller|Configuration|Shadows|Shadow filter method',
            'Filtering sample count': 'Controller|Configuration|Shadows|Filtering sample count',
            'ESM exponent': 'Controller|Configuration|Shadows|ESM exponent',
            'Enable shutters': 'Controller|Configuration|Shutters|Enable shutters',
            'Inner angle': 'Controller|Configuration|Shutters|Inner angle',
            'Outer angle': 'Controller|Configuration|Shutters|Outer angle',
            'Both directions': 'Controller|Configuration|Both directions',
            'Fast approximation': 'Controller|Configuration|Fast approximation',

        }
        return properties[property]

    @staticmethod
    def look_modification(property: str = 'name') -> str:
        """
        Look Modification component properties. Requires PostFX Layer component.
          - 'requires' a list of component names as strings required by this component.
            Use editor_entity_utils EditorEntity.add_components(list) to add this list of requirements.\n
          - 'Enable look modification' Toggle active state of the component True/False
          - 'Color Grading LUT' Asset.id for the LUT used for affecting level look.
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Look Modification',
            'requires': [AtomComponentProperties.postfx_layer()],
            'Enable look modification': 'Controller|Configuration|Enable look modification',
            'Color Grading LUT': 'Controller|Configuration|Color Grading LUT',
        }
        return properties[property]

    @staticmethod
    def material(property: str = 'name') -> str:
        """
        Material component properties. Requires one of Actor OR Mesh component.
          - 'requires' a list of component names as strings required by this component.
            Only one of these is required at a time for this component.\n
          - 'Material Asset': the material Asset.id of the material.
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Material',
            'requires': [AtomComponentProperties.actor(), AtomComponentProperties.mesh()],
            'Material Asset': 'Default Material|Material Asset',
        }
        return properties[property]

    @staticmethod
    def mesh(property: str = 'name') -> str:
        """
        Mesh component properties.
          - 'Mesh Asset' Asset.id of the mesh model.
          - 'Sort Key' dis-ambiguates which mesh renders in front of others (signed int 64)
          - 'Use ray tracing' Toggles interaction with ray tracing (bool)
          - 'Lod Type' options: default, screen coverage, specific lod
          - 'Exclude from reflection cubemaps' Toggles inclusion in generated cubemaps (bool)
          - 'Use Forward Pass IBL Specular' Toggles Forward Pass IBL Specular (bool)
          - 'Minimum Screen Coverage' portion of the screen at which the mesh is culled; 0 (never culled) to 1
          - 'Quality Decay Rate' rate at which the mesh degrades; 0 (never) to 1 (lowest quality imediately)
          - 'Lod Override' which specific LOD to always use; default or other named LOD
          - 'Add Material Component' the button to add a material; set True to add a material component
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        :rtype: str
        """
        properties = {
            'name': 'Mesh',
            'Mesh Asset': 'Controller|Configuration|Mesh Asset',
            'Sort Key': 'Controller|Configuration|Sort Key',
            'Use ray tracing': 'Controller|Configuration|Use ray tracing',
            'Lod Type': 'Controller|Configuration|Lod Type',
            'Exclude from reflection cubemaps': 'Controller|Configuration|Exclude from reflection cubemaps',
            'Use Forward Pass IBL Specular': 'Controller|Configuration|Use Forward Pass IBL Specular',
            'Minimum Screen Coverage': 'Controller|Configuration|Lod Configuration|Minimum Screen Coverage',
            'Quality Decay Rate': 'Controller|Configuration|Lod Configuration|Quality Decay Rate',
            'Lod Override': 'Controller|Configuration|Lod Configuration|Lod Override',
            'Add Material Component': 'Add Material Component',
        }
        return properties[property]

    @staticmethod
    def occlusion_culling_plane(property: str = 'name') -> str:
        """
        Occlusion Culling Plane component properties.
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Occlusion Culling Plane',
        }
        return properties[property]

    @staticmethod
    def physical_sky(property: str = 'name') -> str:
        """
        Physical Sky component properties.
        - 'Sky Intensity' float that determines sky intensity value, default value is 4.
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Physical Sky',
            'Sky Intensity': 'Controller|Configuration|Sky Intensity',
        }
        return properties[property]

    @staticmethod
    def postfx_layer(property: str = 'name') -> str:
        """
        PostFX Layer component properties.
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'PostFX Layer',
        }
        return properties[property]

    @staticmethod
    def postfx_gradient(property: str = 'name') -> str:
        """
        PostFX Gradient Weight Modifier component properties. Requires PostFX Layer component.
          - 'requires' a list of component names as strings required by this component.
            Use editor_entity_utils EditorEntity.add_components(list) to add this list of requirements.\n
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'PostFX Gradient Weight Modifier',
            'requires': [AtomComponentProperties.postfx_layer()],
        }
        return properties[property]

    @staticmethod
    def postfx_radius(property: str = 'name') -> str:
        """
        PostFX Radius Weight Modifier component properties. Requires PostFX Layer component.
          - 'requires' a list of component names as strings required by this component.
            Use editor_entity_utils EditorEntity.add_components(list) to add this list of requirements.\n
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'PostFX Radius Weight Modifier',
            'requires': [AtomComponentProperties.postfx_layer()],
        }
        return properties[property]

    @staticmethod
    def postfx_shape(property: str = 'name') -> str:
        """
        PostFX Shape Weight Modifier component properties. Requires PostFX Layer and one of 'shapes' listed.
          - 'requires' a list of component names as strings required by this component.
            Use editor_entity_utils EditorEntity.add_components(list) to add this list of requirements.\n
          - 'shapes' a list of supported shapes as component names. 'Tube Shape' is also supported but requires 'Spline'.
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'PostFX Shape Weight Modifier',
            'requires': [AtomComponentProperties.postfx_layer()],
            'shapes': ['Axis Aligned Box Shape', 'Box Shape', 'Capsule Shape', 'Compound Shape', 'Cylinder Shape',
                       'Disk Shape', 'Polygon Prism Shape', 'Quad Shape', 'Sphere Shape', 'Shape Reference'],
        }
        return properties[property]

    @staticmethod
    def reflection_probe(property: str = 'name') -> str:
        """
        Reflection Probe component properties. Requires one of 'shapes' listed.
          - 'shapes' a list of supported shapes as component names.
          - 'Baked Cubemap Path' Asset.id of the baked cubemap image generated by a call to 'BakeReflectionProbe' ebus.
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'Reflection Probe',
            'shapes': ['Axis Aligned Box Shape', 'Box Shape'],
            'Baked Cubemap Path': 'Cubemap|Baked Cubemap Path',
        }
        return properties[property]

    @staticmethod
    def ssao(property: str = 'name') -> str:
        """
        SSAO component properties. Requires PostFX Layer component.
          - 'requires' a list of component names as strings required by this component.
            Use editor_entity_utils EditorEntity.add_components(list) to add this list of requirements.\n
        :param property: From the last element of the property tree path. Default 'name' for component name string.
        :return: Full property path OR component name if no property specified.
        """
        properties = {
            'name': 'SSAO',
            'requires': [AtomComponentProperties.postfx_layer()],
        }
        return properties[property]