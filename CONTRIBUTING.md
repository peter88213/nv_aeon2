# Contributing

## General

- Unless you use *novelibre* yourself, it seems rather unlikely to me 
  that you could contribute anything meaningful.

- Before contributing to this project, consider going to the 
  [novelibre "Discussions" forum](https://github.com/peter88213/novelibre/discussions) 
  first to discuss your idea. 
  If you're considering implementing a new feature, the preferred approach is to create a plugin. 

- If you want to pick up an issue, please contact me before creating a pull request. 
  To do so, just leave a comment on the relevant issue.

- The proper way to contribute code is forking the repository 
  and implementing your solution in a thread other than `main`.  
  Then create a pull request. 
  Any code sent via email attachments etc. may be considered as spam and rejected.

- Offers of code in exchange for payment will be discarded as spam. 
 
- Before you start coding, familiarize yourself with the design of *novelibre*, 
  particularly the implementation of the MVC pattern and the plugin API. 
  User interaction should be handled through this API and use the notification 
  mechanisms of the novelibre GUI. 


## AI policy

I consider code to be creative work, and I have a strong preference for 
contributions designed by actual humans over the average and 
mediocre output of agentic and generative AI.

In general, so-called vibe coding does not meet my code quality requirements, 
so this project is not suitable for such contributions in any case. 
The licensing implications around generated code are also unclear, 
as AI models are trained on material without consent or concern for original licensing.

No AI automation or agentic tools are used anywhere in this project. 
Do not use your AI agents on your contributions either. 
Commits listed in any way as authored by, signed off by, or assisted by, 
AI tools are explicitly not allowed. 
Pull requests containing such commits will be rejected. 
You should also not commit AI-specific files into the code repository. 


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
	 │   └── nvaeon2/
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


