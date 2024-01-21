[Project homepage](https://peter88213.github.io/noveltree_aeon2) > Instructions for use

--- 

A [noveltree](https://peter88213.github.io/noveltree/) plugin providing synchronization with Aeon Timeline 2. 

---

# Installation

- Unzip the downloaded zipfile into a new folder.
- Move into this new folder and launch **setup.pyw**. This installs the plugin.

*Note: If you install noveltree at a later time, you can always install the plugin afterwards by running the noveltree_aeon2 setup script again.*

The plugin adds an **Aeon Timeline 2** entry to the *noveltree* **Tools** menu, and an **Aeon 2 plugin Online Help** entry to the **Help** menu. 

---


# Operation

---

## Command reference

---

### Timeline > Information 

- Show information about an existing Timeline project, if any. Timeline and noveltree file dates are compared.

---

### Aeon Timeline 2 > Update the timeline

If a timeline exists, update it from noveltree, otherwise  createa new timeline.

---

### Aeon Timeline 2 > Update the project

Update the noveltree project from the timeline, if existing. 

---

### Aeon Timeline 2 > Add or update moon phase data

The moon phase calculation is based on a 'do it in your head' algorithm by John Conway. 
In its current form, it's only valid for the 20th and 21st centuries.

---

### Aeon Timeline 2 > Edit the timeline

Open the project's timeline, if existing, with the Timeline application. Lock the project.

---

### File > New > Create from Aeon Timeline 2...

Open a file dialog to select a timeline. If no noveltree project with the timeline's file name exists, create a new one from the timeline.

---

## Control conversion

---

### Prepare your timeline for export

The included installation script installs a "noveltree" template in the *noveltree_aeon2* configuration folder. 
The easiest way is to create new timelines based on this template. It provides the entities and event properties that are converted to noveltree by default.

For existing timelines you have two choices:

- Option 1: Add or rename the required entities and event properties in the Timeline settings.
- Option 2: Customize the *noveltree_aeon2* configuration to fit your timeline, see [Custom configuration](#custom-configuration).

---

## Synchronization in detail

---

### Known limitations

- "Narrative" events that begin before 0001-01-01 in the timeline, will not be synchronized with noveltree, because noveltree can not handle these dates.
- The same applies to the section duration in this case, i.e. the event duration in Timeline and the section duration in noveltree may differ.

---

### Conversion rules for newly created noveltree projects

The names/column labels refer to timelines based on the "yWriter" template. 

- If an Aeon event title occurs more than once, the program aborts with an error message.
- Events assigned to the "Narrative" arc are converted to regular sections.
- New sections are put into a new chapter named "New sections". 
- All sections are sorted chronologically. 
- The section status is "Outline". 
- The event title is used as section title (*).
- The start date is used as section date/time, if the start year is 1 or above.
- The section duration is calculated, if the start year is 1 or above.
- Event tags are converted to section tags, if any (*).
- "Descriptions" are imported as section descriptions, if any (*).
- "Notes" are used as section notes, if any (*).
- "Participants" are imported as characters, if any (*).
- "Locations" are imported, if any (*).
- "Items" are imported, if any (*).

---

### Update rules for existing noveltree projects

- Only sections that have the same title as an event are updated.
- If an Aeon event title occurs more than once, the converter aborts with an error message.
- If a noveltree section title occurs more than once, the converter aborts with an error message.
- Sections are marked "unused" if the associated event is deleted in Aeon.
- Section date, section time, and section duration are updated.
- Non-empty section description and section tags are updated.
- Notes of events with a matching title are appended to the section notes.
- The start date is overwritten, if the start year is 1 or above.
- The section duration is overwritten, if the start year is 1 or above.
- New "Normal" type sections are created from "Narrative" events, if missing.
- New sections are put into a new chapter named "New sections". 
- New arcs, characters, locations, and items are added, if assigned to "Narrative" events.
- Arc, character, location, and item relationships are updated, if the entity names match.
- When processing unspecific "day/hour/minute" information, the default date from the noveltree project is used. f there is no default date set, "today" is used.

---

### Update rules for Aeon Timeline 2 projects

- If an Aeon event title occurs more than once, the converter aborts with an error message.
- If a noveltree section title occurs more than once, the converter aborts with an error message.
- Event date/time and event span are updated, if the start year is 1 or above.
- Updated event span is specified in days/hours/minutes as in noveltree.
- Non-empty event description and event tags are updated.
- Event properties "Description" and "Notes" are created, if missing.
- Events created or updated from "Normal" sections are assigned to the *Narrative* arc.
- "Narrative" events are removed if the associated section is deleted in noveltree.
- Entity types "Arc", "Character", "Location", and "Item" are created, if missing.
- A "Narrative" arc is created, if missing.
- A "Storyline" arc role is created, if missing.
- New arcs, characters, locations, and items are added, if assigned to sections.
- Arc, character, location, and item relationships are updated, if the entity names match.
- When creating events from sections without date/time, they get the actual date and are sorted in reading order.
- When creating events from sections without any date/time information, they get the default date from the noveltree project, and are sorted in reading order. If there is no default date set, "today" is used.
- When processing unspecific "day/hour/minute" information, the default date from the noveltree project is used. f there is no default date set, "today" is used.

---

## Custom configuration

You can override the default settings by providing a configuration file. Be always aware that faulty entries may cause program errors. 

---

### Global configuration

An optional global configuration file can be placed in the configuration directory in your user profile. It is applied to any project. Its entries override noveltree_aeon2's built-in constants. This is the path:
`c:\Users\<user name>\.noveltree\config\aeon2nv.ini`
  
---

### Local project configuration

An optional project configuration file named `aeon2nv.ini` can be placed in your project directory, i.e. the folder containing your noveltree and Aeon Timeline project files. It is only applied to this project. Its entries override aeon2nv's built-in constants as well as the global configuration, if any.

---

### How to provide/modify a configuration file

The noveltree_aeon2 distribution comes with a sample configuration file located in the `sample` subfolder. It contains noveltree_aeon2's default settings and options. This file is also automatically copied to the global configuration folder during installation. You best make a copy and edit it.

- The SETTINGS section mainly refers to custom property, role, and type names. 
- Comment lines begin with a `#` number sign. In the example, they refer to the code line immediately above.

This is the configuration explained: 

```
[SETTINGS]

narrative_arc = Narrative

# Name of the user-defined "Narrative" arc.

property_description = Description

# Name of the user-defined section description property.

property_notes = Notes

# Name of the user-defined section notes property.

role_location = Location

# Name of the user-defined role for section locations.

role_item = Item

# Name of the user-defined role for items in a section.

role_character = Participant

# Name of the user-defined role for characters in a section.

type_character = Character

# Name of the user-defined "Character" type

type_location = Location

# Name of the user-defined "Location" type

type_item = Item

# Name of the user-defined "Item" type

color_section = Red

# Color of new section events

color_event = Yellow

# Color of new non-section events

[OPTIONS]

add_moonphase = No

# Yes: Add the moon phase to the event properties.
# No: Update moon phase, if already defined as event property.
```

Note: Your custom configuration file does not have to contain all the entries listed above. 
The changed entries are sufficient. 

---

# License

This is Open Source software, and the *noveltree_aeon2* plugin is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/noveltree_aeon2/blob/main/LICENSE) file.

