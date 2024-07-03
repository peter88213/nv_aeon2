[Project home page](../) > Changelog

------------------------------------------------------------------------

## Changelog

### v4.6.0

- Generate standardized GUIDs according to RFC 4122.

Compatibility: novelibre v4.4 API
Based on novxlib v4.3.0

### v4.5.0

Refactor
- Move the moonphase module to novxlib v4.3.0.
- Use the novelibre 4.4 service for moonphase calculation.

Compatibility: novelibre v4.4 API
Based on novxlib v4.3.0

### v4.4.0

- Use Unicode moon phase characters for display.

Compatibility: novelibre v4.3 API
Based on novxlib v4.2.3

### v4.3.2

- Fix a bug where the "desc" property is not created if missing.
- Add separate methods for character/item/location json roles creation.
- Fix a bug where newly created events get "None" properties
  because the JSON template is completed too late in the process.
  
Compatibility: novelibre v4.3 API
Based on novxlib v4.2.3

### v4.3.1

- Fix a bug where sections without a specific date are given a wrong default 
  date during conversion to aeon.
- Provide a fully translated template in German.  
  
Compatibility: novelibre v4.3 API
Based on novxlib v4.2.3

### v4.3.0

- Make the "Arc" type and role names customizable.

Compatibility: novelibre v4.3 API
Based on novxlib v4.2.3

### v4.2.2

- Update the German translation.

Compatibility: novelibre v4.3 API
Based on novxlib v4.2.3

### v4.2.1

- Refactor the code for future API update,
  making the prefs argument of the Plugin.install() method optional.

Compatibility: novelibre v4.3 API
Based on novxlib v4.1.0

### v4.2.0

- Refactor the code for better maintainability.

Compatibility: novelibre v4.3 API
Based on novxlib v4.1.0

### v4.1.2

- Do not reopen the project after updating from the timeline failed.

Compatibility: novelibre v4.1 API
Based on novxlib v4.1.0

### v4.1.1

- Fix the installation directory path.

Compatibility: novelibre v4.1 API
Based on novxlib v4.1.0

### v4.1.0

- Library update. Now reading and writing *.novx* version 1.4 files.
- Refactor: split the JsonTimeline2 read() and write() methods.
- Use factory methods and getters from the model's NvService object.

Compatibility: novelibre v4.1 API
Based on novxlib v4.0.1

### v3.3.3

- Do not unnecessarily save the project when updating the timeline.

Based on novxlib v3.5.3

### v3.3.2

- Indent the novx files up to the content paragraph level, but not
inline elements within paragraphs.
- Set the default locale when creating a new project.

Based on novxlib v3.5.2

### v3.3.1

- Fix a bug where single spaces between emphasized text in section content are lost when writing novx files.

Based on novxlib v3.5.0

### v3.3.0

- Add "property_moonphase" setting for the moon phase label.
- Add "lock_on_export" option.

Based on novxlib v3.3.0
Compatibility: novelibre v3.6 API

### v3.2.0

- Library update. Now reading *.novx* version 1.3 files.

Based on novxlib v3.3.0
Compatibility: novelibre v3.6 API

### v3.1.0

- Library update. Now reading *.novx* version 1.2 files.

Based on novxlib v3.2.0
Compatibility: novelibre v3.5 API

### v3.0.2

- Fix a regression from v3.0.0 where Aeon arcs are not processed the right way.

Based on novxlib v3.0.1
Compatibility: novelibre v3.0 API

### v3.0.1

- Show localized file date/time instead of ISO-formatted date/time.

Based on novxlib v3.0.1
Compatibility: novelibre v3.0 API

### v3.0.0

- Refactor the code for v3.0 API.
- Enable the online help in German.

Based on novxlib v2.0.0
Compatibility: novelibre v3.0 API

### v2.1.0

Update for "novelibre".

Based on novxlib v1.1.0

### v2.0.0

Preparations for renaming the application:
- Refactor the code for v2.0 API.
- Change the installation directory in the setup script.

Based on novxlib v1.1.0
Compatibility: novelibre v2.0 API

### v1.2.0

- Re-structure the website; adjust links.

Based on novxlib v1.1.0
Compatibility: noveltree v1.8 API

### v1.1.0

Synchronize birth dates and death dates.

Based on novxlib v1.0.1
Compatibility: noveltree v1.0 API

### v1.0.1

- Switch the online help to https://peter88213.github.io/noveltree-help/.

Based on novxlib v1.0.0
Compatibility: noveltree v1.0 API

### v1.0.0

- Release under the GPLv3 license.

Based on novxlib v1.0.0
Compatibility: noveltree v1.0 API
