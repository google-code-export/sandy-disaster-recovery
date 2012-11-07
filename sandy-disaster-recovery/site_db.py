# System libraries.
import datetime
import wtforms.ext.dateutil.fields
import wtforms.fields
from google.appengine.ext import db
from wtforms.ext.appengine.db import model_form

# Local libraries.
import organization

class Site(db.Model):
  # Data about the site itself.
  name = db.StringProperty(required = True)
  reported_by = db.ReferenceProperty(organization.Organization,
                                     collection_name="reported_site_set")
  claimed_by = db.ReferenceProperty(organization.Organization,
                                    collection_name="claimed_site_set")
  request_date = db.DateTimeProperty(auto_now_add=True)
  address = db.StringProperty(required = True)
  city = db.StringProperty()
  county = db.StringProperty()
  state = db.StringProperty()
  zip_code = db.StringProperty()
  cross_street = db.StringProperty()
  landmark = db.StringProperty()
  phone1 = db.StringProperty()
  phone2 = db.StringProperty()
  time_to_call = db.StringProperty()
  rent_or_own = db.StringProperty(choices=["Rent", "Own"])
  work_without_resident = db.BooleanProperty()
  older_than_60 = db.BooleanProperty()
  disabled = db.BooleanProperty()
  special_needs = db.StringProperty(multiline=True)
  electricity = db.BooleanProperty()
  standing_water = db.BooleanProperty()
  tree_damage = db.BooleanProperty()
  tree_damage_details = db.StringProperty(multiline=True)
  habitable = db.BooleanProperty()
  work_requested = db.StringProperty(multiline=True)
  others_help = db.StringProperty(multiline=True)
  debris_removal_only = db.BooleanProperty()
  work_type = db.StringProperty(choices=["Flood", "Trees", "Other"])
  flood_height = db.StringProperty()
  floors_affected = db.StringProperty(choices=[
      "Basement Only",
      "Basement and Ground Floor",
      "Ground Floor Only"])
  carpet_removal = db.BooleanProperty()
  drywall_removal = db.BooleanProperty()
  heavy_item_removal = db.BooleanProperty()
  standing_water = db.BooleanProperty()
  pump_needed = db.BooleanProperty()
  num_trees_down = db.IntegerProperty(
      choices = [0, 1, 2, 3, 4, 5], default = 0)
  num_wide_trees = db.IntegerProperty(
      choices = [0, 1, 2, 3, 4, 5], default = 0)
  roof_damage = db.BooleanProperty()
  tarps_needed = db.IntegerProperty(default = 0)
  goods_and_services = db.StringProperty(multiline = True)

  tree_diameter = db.StringProperty()
  electrical_lines = db.BooleanProperty()
  cable_lines = db.BooleanProperty()
  cutting_cause_harm = db.BooleanProperty()
  other_hazards = db.StringProperty(multiline = True)
  insurance = db.StringProperty(multiline = True)
  notes = db.TextProperty()
  latitude = db.FloatProperty(default = 0.0)
  longitude = db.FloatProperty(default = 0.0)
  # Priority assigned by organization (1 is highest).
  priority = db.IntegerProperty(choices=[1, 2, 3, 4, 5], default = 3)
  # Name of org. rep (e.g. "Jill Smith")
  inspected_by = db.StringProperty()

  # Metadata
  status = db.StringProperty(choices=[
      "Open, unassigned",
      "Open, assigned",
      "Open, partially completed",
      "Open, needs follow-up",
      "Closed, completed",
      "Closed, incomplete",
      "Closed, out of scope",
      "Closed, done by others",
      "Closed, no help wanted",
      "Closed, rejected",
      "Closed, duplicate",
      ],
      default="Open, unassigned")

  date_closed = db.DateTimeProperty()
  # Number of volunteers who helped.
  total_volunteers = db.FloatProperty()
  # Number of hours that each volunteer worked.
  # There's apparently an assumption that all volunteers worked the same amount
  # of time, since total time for the project is calculated as
  # total_volunteers * hours_worked_per_volunteer.
  hours_worked_per_volunteer = db.FloatProperty()

SiteForm2 = model_form(Site)

def ChoicesWithBlank(choices):
  """Converts a list items into choices suitable for a wtforms choices list.
  Prepends a blank value to the list to ensure that a user has to purposefully
  choose all values.
  """
  return [('', '')] + [(choice, choice) for choice in choices]

class SiteForm(SiteForm2):
  priority = wtforms.fields.RadioField(
      choices = [(5, ""), (4, ""), (3, ""), (2, ""), (1, "")],
      coerce = int,
      default = 3)
  num_trees_down = wtforms.fields.SelectField(
      choices = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, "5+")],
      coerce = int,
      default = 0)
  num_wide_trees = wtforms.fields.SelectField(
      choices = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, "5+")],
      coerce = int,
      default = 0)
  request_date = wtforms.ext.dateutil.fields.DateTimeField(
      default = datetime.datetime.now())

  floors_affected = wtforms.fields.SelectField(
      choices=ChoicesWithBlank(Site.floors_affected.choices))
  rent_or_own = wtforms.fields.SelectField(
      choices=ChoicesWithBlank(Site.rent_or_own.choices))
  work_type = wtforms.fields.SelectField(
      choices=ChoicesWithBlank(Site.work_type.choices))

"""def __init__(self, *args, **kwargs):
    SiteForm2.__init__(self, *args, **kwargs)

    self.priority.choices[4] = (5, "5 (lowest)")
    self.priority.coerce = int
    self.num_trees_down.choices[5] = (5, "5+")
    self.num_wide_trees.choices[5] = (5, "5+")"""

# SiteForm = SiteForm2
