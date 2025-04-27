![external-link](../img/external-link.png)
[Deutsch](../help_de/)

------------------------------------------------------------------------

#  User guide

This page refers to the latest
[nv_aeon2](https://github.com/peter88213/nv_aeon2/) release. You can
open it with **Help \> Aeon 2 plugin Online help**.

The plugin adds a **Timeline** entry to the *novelibre* **Tools** menu,
a **Create from Aeon Timeline 2\...** to the **File \> New** submenu,
and an **Aeon 2 plugin Online Help** entry to the **Help** menu. The
Toolbar gets a ![Timeline](images/aeon2.png) button.

## Installing the Aeon Timeline 2 custom template

After installation, you can copy a \"novelibre.xml\" template to the
*Aeon Timeline 2* custom template folder. The easiest way is to create
new timelines based on this template. It provides the entities and event
properties that are converted to *novelibre* by default.

You find the customized template in the *novelibre* installation
directory under

`c:\Users\<user name>\.novx\nv_aeon2_sample\`

Just copy it into

`AppData\Local\Scribble Code\Aeon Timeline 2\CustomTemplates`.

---

**Hint**


The `<your user name>\AppData` folder is hidden, so you might have to go
to the *Explorer* settings first to enable *Show hidden files*. Just
disable this again after successfully having installed the custom
template.

---

The next time you start *Aeon Timeline 2*, the new template appears in
the *Custom Templates* area.

## Command reference

### Tools \> Aeon Timeline 2 \> Information

Show information about an existing *Aeon Timeline 2* project, if any.
*Aeon Timeline 2* and *novelibre* file dates are compared.

### Tools \> Aeon Timeline 2 \> Update the timeline

If a timeline exists, update it from *novelibre*.

### Tools \> Aeon Timeline 2 \> Update the project

Update the *novelibre* project from the timeline, if existing.

### Tools \> Aeon Timeline 2 \> Add or update moon phase data

The \"Moon phase\" event property consists of:

-   the phase day (0 to 29, where 0=new moon, 15=full etc.),
-   the visible shape,
-   the fraction illuminated.

---

**Note**


The moon phase calculation is based on a 'do it in your head' algorithm
by John Conway. In its current form, it's only valid for the 20th and
21st centuries.

---

### Tools \> Aeon Timeline 2 \> Open Aeon Timeline 2

Same as clicking on the ![Timeline](images/aeon2.png) button on the
toolbar.

Open the project's timeline, if existing, with the *Aeon Timeline 2*
application. Depending on the configuration (see below), the project is
automatically locked.

### File \> New \> Create from Aeon Timeline 2\...

Open a file dialog to select a timeline. If no *novelibre* project with
the timeline's file name exists, create a new one from the timeline.

## Control conversion

### Prepare your timeline for export

After installation, you can copy a \"novelibre\" template to the *Aeon
Timeline 2* custom template folder. The easiest way is to create new
timelines based on this template. It provides the entities and event
properties that are converted to *novelibre* by default.

For existing timelines you have two choices:

-   Option 1: Add or rename the required entities and event properties
    in the Aeon Timeline 2 settings.
-   Option 2: Customize the *nv_aeon2* configuration to fit your
    timeline, see [Custom configuration](#custom-configuration).

## Synchronization in detail

### Known limitations

-   \"Narrative\" events that begin before 0001-01-01 in the timeline,
    will not be synchronized with *novelibre*, because *novelibre* can
    not handle these dates.
-   The same applies to the section duration in this case, i.e. the
    event duration in Timeline and the section duration in *novelibre*
    may differ.

### Conversion rules for newly created novelibre projects

The names/column labels refer to timelines based on the \"novelibre\"
template.

-   If an *Aeon* event title occurs more than once, the program aborts
    with an error message.
-   Events assigned to the \"Narrative\" arc are converted to regular
    sections.
-   New sections are put into a new chapter named \"New sections\".
-   All sections are sorted chronologically.
-   The section status is \"Outline\".
-   The event title is used as section title (\*).
-   The start date is used as section date/time, if the start year is 1
    or above.
-   The section duration is calculated, if the start year is 1 or above.
-   Event tags are converted to section tags, if any (\*).
-   \"Descriptions\" are imported as section descriptions, if any (\*).
-   \"Notes\" are used as section notes, if any (\*).
-   \"Participants\" are imported as characters, if any (\*).
-   \"Locations\" are imported, if any (\*).
-   \"Items\" are imported, if any (\*).

### Update rules for existing novelibre projects

-   Only sections that have the same title as an event are updated.
-   If an *Aeon* event title occurs more than once, the converter aborts
    with an error message.
-   If a *novelibre* section title occurs more than once, the converter
    aborts with an error message.
-   Sections are marked \"unused\" if the associated event is deleted in
    *Aeon*.
-   Section date, section time, and section duration are updated.
-   Non-empty section description and section tags are updated.
-   Notes of events with a matching title are appended to the section
    notes.
-   The start date is overwritten, if the start year is 1 or above.
-   The section duration is overwritten, if the start year is 1 or
    above.
-   New \"Normal\" type sections are created from \"Narrative\" events,
    if missing.
-   New sections are put into a new chapter named \"New sections\".
-   New plot lines, characters, locations, and items are added, if
    assigned to \"Narrative\" events.
-   Arc, character, location, and item relationships are updated, if the
    entity names match.
-   When processing unspecific \"day/hour/minute\" information, the
    default date from the *novelibre* project is used. f there is no
    default date set, \"today\" is used.

### Update rules for Aeon Timeline 2 projects

-   If an *Aeon* event title occurs more than once, the converter aborts
    with an error message.
-   If a *novelibre* section title occurs more than once, the converter
    aborts with an error message.
-   Event date/time and event span are updated, if the start year is 1
    or above.
-   Updated event span is specified in days/hours/minutes as in
    *novelibre*.
-   Non-empty event description and event tags are updated.
-   Event properties \"Description\" and \"Notes\" are created, if
    missing.
-   Events created or updated from \"Normal\" sections are assigned to
    the *Narrative* arc.
-   \"Narrative\" events are removed if the associated section is
    deleted in *novelibre*.
-   Entity types \"Arc\", \"Character\", \"Location\", and \"Item\" are
    created, if missing.
-   A \"Narrative\" arc is created, if missing.
-   A \"Storyline\" arc role is created, if missing.
-   New arcs, characters, locations, and items are added, if assigned to
    sections.
-   Arc, character, location, and item relationships are updated, if the
    entity names match.
-   When creating events from sections without any date/time
    information, they get the default date from the *novelibre* project,
    and are sorted in reading order. If there is no default date set,
    \"today\" is used.
-   When processing unspecific \"day/hour/minute\" information, the
    default date from the *novelibre* project is used for date
    calculation. If there is no default date set, \"today\" is used as
    reference date.

## Custom configuration

You can override the default settings by providing a configuration file.
Be always aware that faulty entries may cause program errors.

### Global configuration

An optional global configuration file named `nv_aeon2.ini` an be placed
in the configuration directory of the installation. It is applied to any
project. Its entries override nv_aeon2's built-in constants. This is the
path: `c:\Users\<user name>\.novx\config\nv_aeon2.ini`

### Local project configuration

An optional project configuration file named `nv_aeon2.ini` can be
placed in your project directory, i.e. the folder containing your
*novelibre* and *Aeon Timeline 2* project files. It is only applied to
this project. Its entries override aeon2nv's built-in constants as well
as the global configuration, if any.

### How to provide/modify a configuration file

You find the a sample configuration file with the *nv_aeon2* default
values in the *novelibre* installation directory under

`c:\Users\<user name>\.novx\nv_aeon2_sample\`

You best make a copy and edit it.

-   The SETTINGS section mainly refers to custom property, role, and
    type names.
-   Comment lines begin with a `#` number sign. In the example, they
    refer to the code line immediately above.

This is the configuration file explained:

```ini

[SETTINGS]

narrative_arc = Narrative

# Name of the user-defined "Narrative" arc.

property_description = Description

# Name of the user-defined section description property.

property_notes = Notes

# Name of the user-defined section notes property.

property_moonphase = Moon phase

# Name of the user-defined moon phase property.

type_arc = Arc

# Name of the user-defined "Arc" type

type_character = Character

# Name of the user-defined "Character" type

type_location = Location

# Name of the user-defined "Location" type

type_item = Item

# Name of the user-defined "Item" type

role_arc = Arc

# Name of the user-defined role for regular arcs.

role_plotline = Storyline

# Name of the user-defined role for plot line arcs.

role_character = Participant

# Name of the user-defined role for characters in a section.

role_location = Location

# Name of the user-defined role for section locations.

role_item = Item

# Name of the user-defined role for items in a section.

color_section = Red

# Color of new section events

color_event = Yellow

# Color of new non-section events


[OPTIONS]

add_moonphase = No

# Yes: Add the moon phase to the event properties.
# No: Update moon phase, if already defined as event property.

lock_on_export = No

# Yes: Lock the novelibre project when opening the timeline.
# No: Do not lock the novelibre project when opening the timeline.

```

---

**Note**

Your custom configuration file does not have to contain all the entries
listed above. The changed entries are sufficient.

---
