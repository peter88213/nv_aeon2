[Project home page](../) > Changelog

------------------------------------------------------------------------

## Changelog


### Version 5.5.0

- Update for novelibre 5.43.

API: 5.43
Based on novelibre 5.43.3


### Version 5.4.3

- Aborting the conversion/synchronisation if the timeline has no "Narrative" arc.
- Translated error message.

API: 5.35
Based on novelibre 5.42.0


### Version 5.4.0

- Under Linux, the *idle3* package is no longer needed for displaying tooltips.

API: 5.35
Based on novelibre 5.35.1


### Version 5.3.1

- Added icon to menu entries.
- Reformatted the code according to PEP-8.

API: 5.18
Based on novelibre 5.29.2 (5.30.0)


### Version 5.2.4

- Updated the HELP_URL link address.

API: 5.18
Based on novelibre 5.23.0


### Version 5.2.3

- Fix a bug where the **File > New > Create from Aeon Timeline 2...** command cannot be properly aborted.

API: 5.18
Based on novelibre 5.18.0


### Version 5.2.2

- Updated the messaging.

API: 5.17
Based on novelibre 5.17.3


### Version 5.2.0

- Updated the messaging.

API: 5.17
Based on novelibre 5.17.0


### Version 5.1.2

- Refactored the code for better maintainability.

API: 5.9
Based on novelibre 5.16.1


### Version 5.1.1

- Fixed the order of the module imports.

API: 5.9
Based on novelibre 5.11.2


### Version 5.1.0

- Making backup copies when saving timeline or novx files.

API: 5.9
Based on novelibre 5.9.1


### Version 5.0.4

Library update:
- Refactor the code for better maintainability.
- Fix a bug where project cannot be optionally locked on opening the timeline.

API: 5.0
Based on novelibre 5.0.28

### Version 4.9.0

- Fix a bug where changes in duration are not applied to the timeline if zero.
- Refactor and revise the code for better maintainability.
- Release the dependency on the novxlib library.

Compatibility: novelibre 4.17 API

### Version 4.8.1

- Change the message window title.
- Refactor, replacing global constants with class constants.

Compatibility: novelibre 4.11 API
Based on novxlib 5.0.0

### Version 4.8.0

- Add a tooltip to the toolbar button.

Compatibility: novelibre 4.11 API
Based on novxlib 4.6.4

### Version 4.7.3

- Refactor: Change import order for a quick start.

Compatibility: novelibre 4.4 API
Based on novxlib 4.6.3

### Version 4.7.2

Library update:
- Rejecting malformed .novx files.
- Stripping illegal xml characters during post-processing.
- Refactor for future Python versions

Compatibility: novelibre 4.4 API
Based on novxlib 4.6.3

### Version 4.7.1

- Refactor localization.

Compatibility: novelibre 4.4 API
Based on novxlib 4.4.0

### Version 4.7.0

- Move the **Aeon Timeline 2** submenu from the main menu to the **Tools** menu.
- Add an "Aeon Timeline 2" button to the button bar.

Compatibility: novelibre 4.4 API
Based on novxlib 4.4.0

### Version 4.6.0

- Generate standardized GUIDs according to RFC 4122.

Compatibility: novelibre 4.4 API
Based on novxlib 4.3.0

### Version 4.5.0

Refactor
- Move the moonphase module to novxlib 4.3.0.
- Use the novelibre 4.4 service for moonphase calculation.

Compatibility: novelibre 4.4 API
Based on novxlib 4.3.0

### Version 4.4.0

- Use Unicode moon phase characters for display.

Compatibility: novelibre 4.3 API
Based on novxlib 4.2.3

### Version 4.3.2

- Fix a bug where the "desc" property is not created if missing.
- Add separate methods for character/item/location json roles creation.
- Fix a bug where newly created events get "None" properties
  because the JSON template is completed too late in the process.
  
Compatibility: novelibre 4.3 API
Based on novxlib 4.2.3

### Version 4.3.1

- Fix a bug where sections without a specific date are given a wrong default 
  date during conversion to aeon.
- Provide a fully translated template in German.  
  
Compatibility: novelibre 4.3 API
Based on novxlib 4.2.3

### Version 4.3.0

- Make the "Arc" type and role names customizable.

Compatibility: novelibre 4.3 API
Based on novxlib 4.2.3

### Version 4.2.2

- Update the German translation.

Compatibility: novelibre 4.3 API
Based on novxlib 4.2.3

### Version 4.2.1

- Refactor the code for future API update,
  making the prefs argument of the Plugin.install() method optional.

Compatibility: novelibre 4.3 API
Based on novxlib 4.1.0

### Version 4.2.0

- Refactor the code for better maintainability.

Compatibility: novelibre 4.3 API
Based on novxlib 4.1.0

### Version 4.1.2

- Do not reopen the project after updating from the timeline failed.

Compatibility: novelibre 4.1 API
Based on novxlib 4.1.0

### Version 4.1.1

- Fix the installation directory path.

Compatibility: novelibre 4.1 API
Based on novxlib 4.1.0

### Version 4.1.0

- Library update. Now reading and writing *.novx* version 1.4 files.
- Refactor: split the JsonTimeline2 read() and write() methods.
- Use factory methods and getters from the model's NvService object.

Compatibility: novelibre 4.1 API
Based on novxlib 4.0.1

### Version 3.3.3

- Do not unnecessarily save the project when updating the timeline.

Based on novxlib 3.5.3

### Version 3.3.2

- Indent the novx files up to the content paragraph level, but not
inline elements within paragraphs.
- Set the default locale when creating a new project.

Based on novxlib 3.5.2

### Version 3.3.1

- Fix a bug where single spaces between emphasized text in section content are lost when writing novx files.

Based on novxlib 3.5.0

### Version 3.3.0

- Add "property_moonphase" setting for the moon phase label.
- Add "lock_on_export" option.

Based on novxlib 3.3.0
Compatibility: novelibre 3.6 API

### Version 3.2.0

- Library update. Now reading *.novx* version 1.3 files.

Based on novxlib 3.3.0
Compatibility: novelibre 3.6 API

### Version 3.1.0

- Library update. Now reading *.novx* version 1.2 files.

Based on novxlib 3.2.0
Compatibility: novelibre 3.5 API

### Version 3.0.2

- Fix a regression from version 3.0.0 where Aeon arcs are not processed the right way.

Based on novxlib 3.0.1
Compatibility: novelibre 3.0 API

### Version 3.0.1

- Show localized file date/time instead of ISO-formatted date/time.

Based on novxlib 3.0.1
Compatibility: novelibre 3.0 API

### Version 3.0.0

- Refactor the code for v3.0 API.
- Enable the online help in German.

Based on novxlib 2.0.0
Compatibility: novelibre 3.0 API

### Version 2.1.0

Update for "novelibre".

Based on novxlib 1.1.0

### Version 2.0.0

Preparations for renaming the application:
- Refactor the code for v2.0 API.
- Change the installation directory in the setup script.

Based on novxlib 1.1.0
Compatibility: novelibre 2.0 API

### Version 1.2.0

- Re-structure the website; adjust links.

Based on novxlib 1.1.0
Compatibility: noveltree 1.8 API

### Version 1.1.0

Synchronize birth dates and death dates.

Based on novxlib 1.0.1
Compatibility: noveltree 1.0 API

### Version 1.0.1

- Switch the online help to https://peter88213.github.io/noveltree-help/.

Based on novxlib 1.0.0
Compatibility: noveltree 1.0 API

### Version 1.0.0

- Release under the GPLv3 license.

Based on novxlib 1.0.0
Compatibility: noveltree 1.0 API
