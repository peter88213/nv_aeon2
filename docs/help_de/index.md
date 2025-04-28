[Projekt-Homepage](https://github.com/peter88213/nv_aeon2) > [Index](../) > Help

![external-link](../img/external-link.png)[English](../help/)

------------------------------------------------------------------------

# nv_aeon2 Benutzerhandbuch

---

**Hinweis**

Die deutsche Übersetzung des *nv_aeon2*-Benutzerhandbuchs ist noch in
Arbeit. Im Zweifelsfall könnnen Sie von dieser Seite aus zur englischen
Version des Benutzerhandbuchs wechseln (Link oben).

---

Diese Seite gilt für die neueste Ausgabe von
[nv_aeon2](https://github.com/peter88213/nv_aeon2/). Sie können sie mit
**Hilfe \> Aeon 2-Plugin Online-Hilfe** öffnen.

Das Plugin fügt dem *novelibre*-**Extras**-Menü den Eintrag **Aeon
Timeline 2** hinzu, außerdem dem **Datei \> Neu**-Untermenü den Eintrag
**Aus Aeon Timeline 2 erzeugen\...**, und dem **Hilfe**-Menü den Eintrag
**Aeon 2-Plugin Online-Hilfe**. Die Werkzeugleiste erhält eine
![Timeline](images/aeon2.png) Schaltfläche.

## Die Aeon Timeline 2 Benutzervorlage installieren

Nach der Installation können Sie eine Vorlagendatei namens \"novelibre
German.xml\" in den Aeon 2-Ordner für Benutzervorlagen kopieren. Es ist
dann einfach, neue Zeitleisten aus dieser Vorlage zu erzeugen. Sie
stellt die Entities und Properties bereit, die standardmäßig mit
*novelibre* synchronisiert werden.

Sie finden die Benutzervorlage im *novelibre*-Installationsverzeichnis
unter

`c:\Users\<Benutzername>\.novx\nv_aeon2_sample\`

Kopieren Sie sie einfach in das folgende Verzeichnis:

`AppData\Local\Scribble Code\Aeon Timeline 2\CustomTemplates`.

---

**Hinweis**

Der Ordner `<Benutzername>\AppData` ist verborgen, deshalb müssen Sie
eventuell zuerst zu den *Explorer*-Einstellungen gehen und *Verborgene
Dateien anzeigen* erlauben. Nachdem Sie die Benutzervorlage erfolgreich
installiert haben, können Sie das wieder zurückstellen.

---

Wenn Sie *Aeon Timeline 2* das nächste Mal aufrufen, erscheint die
Benutzervorlage im Bereich *Custom Templates* zur Auswahl.

## Befehlsreferenz

### Extras \> Aeon Timeline 2 \> Information

Damit bekommen Sie Informationen über ein bestehendes *Aeon Timeline
2*-Projekt angezeigt, falls vorhanden. Das Dateidatum des *Aeon Timeline
2*- wird mit dem des *novelibre*-Projekts verglichen.

### Extras \> Aeon Timeline 2 \> Den Zeitstrahl aktualisieren

Damit wird ein existierender Zeitstrahl aus dem *novelibre*-Projekt
aktualisiert.

### Extras \> Aeon Timeline 2 \> Das Projekt aktualisieren

Damit wird das *novelibre*-Projekt aus einem existierenden Zeitstrahl
aktualisiert.

### Extras \> Aeon Timeline 2 \> Mondphasen hinzufügen oder aktualisieren

Die Ereigniseigenschaft \"Mondphase\" setzt sich zusammen aus:

-   dem Phasentag (0 bis 29, wobei 0=Neumond, 15=voll etc.),
-   der sichtbaren Form,
-   dem beleuchteten Bruchteil.

---

**Anmerkung**

Die Berechnung der Mondphase beruht auf einem überschlägigen Verfahren
von John Conway. In ihrer derzeitigen Ausführung ist sie nur für das 20.
und 21. Jahrhundert gültig.

---

### Extras \> Aeon Timeline 2 \> Aeon Timeline 2 öffnen

Oder in der Werkzeugleiste auf die die Schaltfläche
![Timeline](images/aeon2.png) klicken.

Den Zeitstrahl zum Projekt mit *Aeon Timeline 2* öffnen, falls
vorhanden. Je nach Konfiguration (siehe unten) wird das Projekt
automatisch gesperrt.

### Datei \> Neu \> Aus Aeon Timeline 2 erzeugen\...

Damit öffnen Sie einen Dateiauswahldialog, um eine *.aeonzip*-Datei
auszuwählen. Falls noch kein *novelibre*-Projekt mit dem gleichen
Dateinamen existiert, wird das aktuelle Projekt geschlossen und ein
neues aus dem Zeitstrahl erzeugt.

## Die Konvertierung steuern

### Den Zeitstrahl für den Export vorbereiten

Nach der Installation können Sie eine \"novelibre\"-Vorlage in das *Aeon
Timeline 2*-Benutzervorlagenverzeichnis kopieren. Es ist am einfachsten,
neue Zeitstrahlen mit Hilfe dieser Vorlage zu erzeugen. Sie stellt
diejenigen *Entities* und *Event Properties* bereit, die standardmäßig
mit *novelibre* synchronisiert werden.

für existierende Zeitstrahlen haben Sie zwei Möglichkeiten zur Auswahl:

-   Option 1: Fügen Sie in *Aeon Timeline 2* die erforderlichen
*Entities* und *Event Properties* hinzu oder benennen Sie sie um.
-   Option 2: Passen Sie die Konfiguration von *nv_aeon2* an, damit sie
zum Zeitstrahl passt, siehe [Benutzerdefinierte
Konfiguration](#benutzerdefinierte-konfiguration).

## Die Synchronisierung im Einzelnen

### Bekannte Einschränkungen

-   Ereignisse, die auf dem Zeitstrahl vor dem Datum 0001-01-01 liegen,
können nicht mit *novelibre* synchronisiert werden, weil *novelibre*
damit nicht umgehen kann.
-   Dasselbe gilt in diesem Fall für die Ereignisdauer, d.h. Die
Zeitdauer kann dann in *Aeon Timeline 2* und *novelibre*
unterschiedlich sein.

### Konvertierungsregeln für neu erzeugte novelibre-Projekte

The names/column labels refer to timelines based on the \"novelibre\"
template.

-   If an Aeon event title occurs more than once, the program aborts
with an error message.
-   Events assigned to the \"Narrative\" arc are converted to regular
sections.
-   New Sections are put into a neu chapter named \"Neue Abschnitte\".
-   All sections are sorted chronologically.
-   The section status is \"Gliederung\".
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

### Aktualisierungsregeln für bestehende novelibre-Projekte

-   Only sections that have the same title as an event are updated.
-   If an Aeon event title occurs more than once, the converter aborts
with an error message.
-   If a *novelibre* section title occurs more than once, the converter
aborts with an error message.
-   Sections are marked \"unused\" if the associated event is deleted in
Aeon.
-   Section date, section time, and section duration are updated.
-   Non-empty section description and section tags are updated.
-   Notizen of events with a matching title are appended to the section
notes.
-   The start date is overwritten, if the start year is 1 or above.
-   The section duration is overwritten, if the start year is 1 or
above.
-   New \"Normal\" type sections are generated from \"Narrative\"
events, if missing.
-   New Sections are put into a neu chapter named \"Neue Abschnitte\".
-   New plot lines, characters, locations, and items are added, if
assigned to \"Narrative\" events.
-   Arc, character, location, and item relationships are updated, if the
entity names match.
-   When processing unspecific \"day/hour/minute\" information, the
default date from the *novelibre* project is used. f there is no
default date set, \"today\" is used.

### Aktualisierungsregeln für Aeon Timeline 2-Projekte

-   If an Aeon event title occurs more than once, the converter aborts
with an error message.
-   If a *novelibre* section title occurs more than once, the converter
aborts with an error message.
-   Event date/time and event span are updated, if the start year is 1
or above.
-   Updated event span is specified in days/hours/minutes as in
*novelibre*.
-   Non-empty event description and event tags are updated.
-   Event properties \"Description\" and \"Notes\" are generated, if
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

## Benutzerdefinierte Konfiguration

Sie können die Voreinstellungen mit Hilfe einer Konfigurationsdatei
überschreiben. Denken Sie aber immer daran, dass fehlerhafte Einträge
den Programmablauf stören können.

### Globale Konfiguration

Sie können eine optionale globale Konfigurationsdatei namens
`nv_aeon2.ini` im Konfigurationsverzeichnis der Installation ablegen.
Sie wird auf jedes Projekt angewendet. Ihre Einträge überschreiben die
Voreinstellungen von *nv_aeon2*. Dies ist der Pfad unter Windows:
`c:\Users\<Benutzername>\.novx\config\nv_aeon2.ini`

### Lokale Projektkonfiguration

Sie können eine optionale Projekt-Konfigurationsdatei namens
`nv_aeon2.ini` in Ihrem Projektverzeichnis ablegen, d.h. in dem Ordner,
der Ihre *novelibre*- und *Aeon Timeline 2*-Projektdateien enthält. Sie
gilt dann nur für das Projekt. Ihre Einträge überschreiben sowohl die
Voreinstellungen von *nv_aeon2* als auch die globale Konfiguration,
falls vorhanden.

### Wie man eine Konfigurationsdatei erstellt oder anpasst

Sie finden eine Musterkonfigurationsdatei mit den voreingestellten
Werten von *nv_aeon2* im *novelibre*-Installationsverzeichnis unter

`c:\Users\<Benutzername>\.novx\nv_aeon2_sample\`

Am besten erstellen Sie eine Kopie und bearbeiten sie.

-   Der Abschnitt SETTINGS bezieht sich hauptsächlich auf die
benutzerdefinierten Bezeichnungen für Properties, Roles und Types.
-   Kommentarzeilen beginnen mit einem Rautenzeichen `#`. Im Beispiel
beziehen sie sich auf die unmittelbar darüberliegende Codezeile.

Das ist die Konfigurationsdatei mit Erklärungen:

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

**Anmerkung**


Ihre benutzerdefinierte Konfigurationsdatei muss nicht alle Einträge
enthalten, die oben aufgelistet sind. Es genügen die durch Sie
geänderten Einträge.

---

Copyright (c) 2025 by Peter Triesberger. All rights reserved.
