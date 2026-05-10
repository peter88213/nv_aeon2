# Contributing

## How to provide translations

Translations and help texts for this plugin are intended to be part 
of a central *novelibre* language pack. 
See the [novelibre CONTRIBUTING page](https://github.com/peter88213/novelibre/blob/main/CONTRIBUTING.md). 


## Development

### Mandatory directory structure for building the plugin package

```
.
├── novelibre/
│   ├── i18n/
│   ├── src/
│   └── tools/ 
│       ├── msgfmt.py
│       ├── inliner.py
│       ├── package_builder.py
│       ├── pgettext.py
│       ├── translate_de.py
│       └── translations.py
└── nv_aeon2/
    ├── i18n/
    ├── src/
	 │   └── nvaeon2lib/
    └── tools/ 
        └── build.py
```

### Conventions

See https://github.com/peter88213/novelibre/blob/main/docs/conventions.md

## Development tools

- [Python](https://python.org) version 3.12.
- **build.py** starts the building and packaging process.

### Optional IDE
- [Eclipse IDE](https://eclipse.org) with [PyDev](https://pydev.org) and *EGit*.
- Apache Ant can be used for starting the **build.py** script.


