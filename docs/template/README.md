[![Download the latest release](docs/img/download-button.png)](https://github.com/peter88213/nv_aeon2/raw/main/dist/nv_aeon2_v0.99.0.pyzw)
[![Changelog](docs/img/changelog-button.png)](docs/changelog.md)
[![News](docs/img/news-button.png)](https://github.com/peter88213/novelibre/discussions/1)
[![Online help](docs/img/help-button.png)](https://peter88213.github.io/nvhelp-en/nv_aeon2/)


# ![A](icons/aLogo32.png) nv_aeon2

The [novelibre](https://github.com/peter88213/novelibre/) Python program helps authors organize novels.  

The *nv_aeon2* plugin synchronizes novelibre projects with Aeon Timeline 2.

![Screenshot](docs/Screenshots/screen01.png)

## Features

### Create a new novelibre project from a timeline

- Transfer "Narrative" sections with date, time, duration, description, tags, and relationships.
- Create characters, locations, items, and arcs are created.

### Update an existing novelibre project from a timeline

- Update section date, time, duration, description, tags, and relationships.
- Missing sections, characters, locations, and items are created.
- Sections are marked "unused" if the associated event is deleted in Aeon.

### Update an existing timeline from a novelibre project

- Update event date, time, duration, description, tags, and relationships.
- Entity types "Arc", "Character", "Location", and "Item", and a *Narrative* arc are created, if missing.
- Event properties "Description" and "Notes" are created, if missing.
- Missing events, characters, locations, and items are created.
- "Narrative" events are removed if the associated section is deleted in novelibre.

### Create a new timeline from a novelibre project

- Just update an empty timeline from a novelibre project.

### Add/update moon phase data

- For each event in the timeline, the moon phase can be added as a property.


## Requirements

- Aeon Timeline 2 
- [novelibre](https://github.com/peter88213/novelibre/) version 4.4+

## Download and install

### Default: Executable Python zip archive

Download the latest release [nv_aeon2_v0.99.0.pyzw](https://github.com/peter88213/nv_aeon2/raw/main/dist/nv_aeon2_v0.99.0.pyzw)

- Launch *nv_aeon2_v0.99.0.pyzw* by double-clicking (Windows/Linux desktop),
- or execute `python nv_aeon2_v0.99.0.pyzw` (Windows), resp. `python3 nv_aeon2_v0.99.0.pyzw` (Linux) on the command line.

### Alternative: Zip file

The package is also available in zip format: [nv_aeon2_v0.99.0.zip](https://github.com/peter88213/nv_aeon2/raw/main/dist/nv_aeon2_v0.99.0.zip)

- Extract the *nv_aeon2_v0.99.0* folder from the downloaded zipfile "nv_aeon2_v0.99.0.zip".
- Move into this new folder and launch *setup.pyw* by double-clicking (Windows/Linux desktop), 
- or execute `python setup.pyw` (Windows), resp. `python3 setup.pyw` (Linux) on the command line.

---

[Changelog](docs/changelog.md)

## Usage and conventions

See the [online manual](https://peter88213.github.io/nvhelp-en/nv_aeon2/)

---

## Credits

- The logo is made using the free *Pusab* font by Ryoichi Tsunekawa, [Flat-it](http://flat-it.com/).

## License

This is Open Source software, and the *nv_aeon2* plugin is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/nv_aeon2/blob/main/LICENSE) file.

