# nv_aeon2

The [noveltree](https://peter88213.github.io/noveltree/) Python program helps authors organize novels.  

The *nv_aeon2* plugin synchronizes noveltree projects with Aeon Timeline 2.

![Screenshot](Screenshots/screen01.png)

## Features

### Create a new noveltree project from a timeline

- Transfer "Narrative" sections with date, time, duration, description, tags, and relationships.
- Create characters, locations, items, and arcs are created.

### Update an existing noveltree project from a timeline

- Update section date, time, duration, description, tags, and relationships.
- Missing sections, characters, locations, and items are created.
- Sections are marked "unused" if the associated event is deleted in Aeon.

### Update an existing timeline from a noveltree project

- Update event date, time, duration, description, tags, and relationships.
- Entity types "Arc", "Character", "Location", and "Item", and a *Narrative* arc are created, if missing.
- Event properties "Description" and "Notes" are created, if missing.
- Missing events, characters, locations, and items are created.
- "Narrative" events are removed if the associated section is deleted in noveltree.

### Create a new timeline from a noveltree project

- Just update an empty timeline from a noveltree project.

### Add/update moon phase data

- For each event in the timeline, the moon phase can be added as a property.


## Requirements

- Aeon Timeline 2 
- [noveltree](https://peter88213.github.io/noveltree/) version 1.0+

## Download and install

[Download the latest release (version 0.99.0)](https://github.com/peter88213/nv_aeon2/raw/main/dist/nv_aeon2_v0.99.0.zip)

- Extract the "nv_aeon2_v0.99.0" folder from the downloaded zipfile "nv_aeon2_v0.99.0.zip".
- Move into this new folder and launch **setup.pyw**. This installs the plugin for the local user.

---

[Changelog](changelog)

## Usage and conventions

See the [instructions for use](usage)


## License

This is Open Source software, and the *nv_aeon2* plugin is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/nv_aeon2/blob/main/LICENSE) file.


 




