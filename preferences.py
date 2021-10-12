import bpy

from bpy.props import StringProperty
from bpy.types import AddonPreferences


class Preferences(AddonPreferences):
    bl_idname = "energy"

    processor_properties = [
        "atk_processor_number",
        "atk_processor_first_name",
        "atk_processor_last_name",
        "atk_processor_street",
        "atk_processor_house_number",
        "atk_processor_zip_code",
        "atk_processor_city",
        "atk_processor_country",
        "atk_processor_email",
    ]

    atk_processor_number: StringProperty(
        name="Number",
        description="Processor number")

    atk_processor_first_name: StringProperty(
        name="First name",
        description="Processor first name")

    atk_processor_last_name: StringProperty(
        name="Last name",
        description="Processor last name")

    atk_processor_street: StringProperty(
        name="Street",
        description="Processor street")

    atk_processor_house_number: StringProperty(
        name="House n°",
        description="Processor house number")

    atk_processor_zip_code: StringProperty(
        name="Zip code",
        description="Processor zip code")

    atk_processor_city: StringProperty(
        name="City",
        description="Processor city")

    atk_processor_country: StringProperty(
        name="Country",
        description="Processor country")

    atk_processor_email: StringProperty(
        name="E-mail",
        description="Processor e-mail")

    def draw(self, context):
        for prop in self.processor_properties:
            self.layout.prop(self, prop)
