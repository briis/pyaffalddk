# Changelog for pyaffalddk

Rudersdal - Material type [Farligt affald, distrikt A] is not defined in the system for Genbrug #289

## [2.5.2] - `2025-05-13`

### Changes

* Rudersdal - Material type [Farligt affald, distrikt A] is not defined in the system for Genbrug #289


## [2.5.1] - `2025-05-12`

### Changes

* Høje Taastrup, mangler Haveaff,Papir- Plast/Mad- og Drikkekartoner og Metal/glas affalddk#280
* Haveaffald Esbjerg affalddk#277
* "Pap", "Papir, pap & glas", "Plast & Metal", "Rest- og madaffald" virker ikke i 2.40beta3 for Gentofte Kommune affalddk#275
* Hjørring kommune affalddk#265
* Removed the following Municipalities, as they cannot be supported with the current API:
  * Frederiksberg
  * Hedensted
  * Ringsted

## [2.5.0] - `2025-05-10`

### Added

* Added smoketests for getting fraction names and to make sure we don't break old fixes
* Added and/or changed Fractions for the following Municipalities_
  * Mariagerfjord
  * Aalborg
  * Egedal
  * Svendborg
  * Glostrup
  * Lyngby-Taarbaek
  * Esbjerg
  * Randers
  * Sønderborg
  * Kerteminde
  * Næstved
  * Jammerbugt
  * Rudersdal
  * Rødovre

### Changes

* Cleanup for get_garbage_data() on all apis
* Re-sorting all the const lists and consolidating the municpality list to the Munipality File
* Changed address_id to the new naming uid, to avoid unique_id issues.
* Updated local cli tool for easy adding new data to the smoketests
* Make sure to always log a warning or raise a RuntimeError when failing to find fraction name

## [2.4.0] - `2025-05-06`

### Added
* Adding interface for the affaldsportalen / renoweb.servicegh

## [2.3.1] - `2025-05-04`

### Added
* Small change to get municipality ids in the pip package

## [2.3.0] - `2025-05-04`

### Added
* Adding interface for Perfect Waste. Thank you @ttopholm for the help.

## [2.2.2] - `2025-04-30`

### Added
* Fixing wrong pickup date for KK - again, due to conversion to UTC

## [2.2.1] - `2025-04-24` [YANKED]

### Added
* Support for **Københavns Kommune** added. Thank you to @TermeHansen for implementing this
* Fixing wrong pickup date for KK, due to conversion to UTC - Did not work, came 1 day ahead

## [2.2.0] - `2025-04-24`

### Added
* Support for **Københavns Kommune** added. Thank you to @TermeHansen for implementing this

## [2.1.7] - `2025-03-19`

### What's Changed

* Fixing Missing Material in Egedal Kommune. Closing [AffaldDK #221](https://github.com/briis/affalddk/issues/221)
* Fixing Missing Material in Gladsaxe Kommune. Closing [AffaldDK #238](https://github.com/briis/affalddk/issues/238)
* Fixing Missing Material in Gribskov Kommune. Closing [AffaldDK #242](https://github.com/briis/affalddk/issues/242)
* Added function to find a date based on Weekday and Odd or Even week. Closing [AffaldDK #226](https://github.com/briis/affalddk/issues/226)
* Removed Sorø Kommune as they no longer have en open API.
* Bump `pyaffalddk` to V2.1.7

## [2.1.6] - `2024-01-07`

### What's Changed

* Removed the Last Update field as this causes blocking IO issues with Home Assistant
* Fixing missing DAYLIGHT information in iCal data. Closing [AffaldDK #205](https://github.com/briis/affalddk/issues/205)
* Fixing missing containers in Køge after renaming. Closing [AffaldDK #207](https://github.com/briis/affalddk/issues/207)
* Bump `pyaffalddk` to V2.1.6

## [2.1.3] - `2024-01-05`

### What's Changed

* Fixing missing DAYLIGHT information in iCal data. Closing [AffaldDK #205](https://github.com/briis/affalddk/issues/205)
* Fixing missing containers in Køge after renaming. Closing [AffaldDK #207](https://github.com/briis/affalddk/issues/207)
* Bump `pyaffalddk` to V2.1.3

## [2.1.2] - `2024-12-09`

### What's Changed

* Fixing renamed containers in Egedal kommune. Closing [AffaldDK #194](https://github.com/briis/affalddk/issues/194)
* Bump `pyaffalddk` to V2.1.2

## [2.1.1] - `2024-11-25`

### What's Changed

* Adding the option to use iCalendar file as input source for Calendar data.
* Adding Odense Kommune to the list of supported municipalities
* Adding Århus Kommune to the list of supported municipalities
* Added new Material Type `Genbrugsspand, 240L (2-delt) (1 stk.)`. Closing [AffaldDK #186](https://github.com/briis/affalddk/issues/186)
* Bump `pyaffalddk` to V2.1.1

## [2.0.44] - `2024-11-18`

### What's Changed

* Fixing issue where there is a weekday present but next pick-up is undefined. Typically occurs around New Years time. Closing [AffaldDK #179](https://github.com/briis/affalddk/issues/179)
* Added December 31st of next year, if a Pickup Type is valid, but no current date is given.
* Bump `pyaffalddk` to V2.0.44

## [2.0.41] - `2024-10-16`

### What's Changed

* Added new Material Type `juletrae` and also added new image. Closing [AffaldDK #165](https://github.com/briis/affalddk/issues/165)
* Bump `pyaffalddk` to V2.0.41

## [2.0.40] - `2024-10-03`

### What's Changed

* Start Fixing issues, after Bornholm has changed naming of many un its. Contributing to [AffaldDK #159](https://github.com/briis/affalddk/issues/159)
* Bump `pyaffalddk` to V2.0.40

## [2.0.39] - `2024-09-23`

### What's Changed

* Fixing missing Types in Svendborg. Closing [AffaldDK #151](https://github.com/briis/affalddk/issues/151)
* Fixing missing Types in Horsens. Closing [pyaffalddk #14](https://github.com/briis/pyaffalddk/issues/14)
* Bump `pyaffalddk` to V2.0.39

## [2.0.38] - `2024-08-16`

### What's Changed

* Fixing missing Types in Solrød. Closing [AffaldDK #139](https://github.com/briis/affalddk/issues/139)
* Fixing missing Types in Egedal. Closing [AffaldDK #142](https://github.com/briis/affalddk/issues/142)
* Bump `pyaffalddk` to V2.0.38

## [2.0.37] - `2024-08-13`

### What's Changed

* Fixing missing Types in Vordingborg. Closing [AffaldDK #136](https://github.com/briis/affalddk/issues/136)
* Bump `pyaffalddk` to V2.0.37

## [2.0.36] - `2024-07-29`

### What's Changed

* Fixing missing Types in Ringsted. Closing [AffaldDK #133](https://github.com/briis/affalddk/issues/133)
* Bump `pyaffalddk` to V2.0.36

## [2.0.35] - `2024-07-29`

### What's Changed

* Fixing missing Types in Albertslund. Closing [AffaldDK #129](https://github.com/briis/affalddk/issues/129)
* Bump `pyaffalddk` to V2.0.35


## [2.0.34] - `2024-07-05`

### What's Changed

* Fixing missing containers in Esbjerg. Closing [AffaldDK #117](https://github.com/briis/affalddk/issues/117)
* Fixing missing containers in Gribskov. Closing [AffaldDK #118](https://github.com/briis/affalddk/issues/118)
* Bump `pyaffalddk` to V2.0.34

## [2.0.33] - `2024-06-29`

### What's Changed

* Adding Bornholm as new Municipality. I have limited test data to go on, but some data is being returned. If anything is missing, please report back. Closing [AffaldDK #114](https://github.com/briis/affalddk/issues/114)
* Bump `pyaffalddk` to V2.0.33

* Fixing missing details for Faxe. Closing #4
* Fixing missing details for Lyngby-Taarbæk. Cloising [AffaldDK #105](https://github.com/briis/affalddk/issues/105)
* Bump `pyaffalddk` to V2.0.31

## [2.0.30] - `2024-05-27`

### What's Changed

* Fixing missing details for Slagelse. Closing #97
* Bump `pyaffalddk` to V2.0.30

## [2.0.29] - `2024-05-12`

### What's Changed

* Fixing missing details for Vejen and Randers. Closing #87
- Bump `pyaffalddk` to V2.0.29

# [2.0.28] - `2024-05-04`

### What's Changed

- Fixed missing containers for Solrød Kommune.
- Fixed missing containers for Egedal Kommune. Closing #84
- Fixed missing containers for Lyngby-Taarbæk Kommune. Closing #83
- Fixed missing containers for Glostrup Kommune. Closing #79
- Added two new Categories: `restaffald` and `madaffald`. These are new as separat containers.

## [2.0.26] - `2024-04-22`

### What's Changed

- Modified change from 2.0.25, as it caused problems for many with the category Storskrald. It will now work for all, including Gladsaxe.
- Added more details to warning if category not found. Makes it easier to debug when people report errors.

## [2.0.25] - `2024-04-19`

### What's Changed

- Added new category Plast, MDK, Glas & Metal.
- Added missing containers for Varde kommune. Closing #75
- Added missing storskrald for Solrød

## [2.0.23] - `2024-04-16`

### What's Changed

- Added `|` as separator to Next Pickup sensor, to easier identify items.
- Added missing containers for Papir & Plast and Metal & Glas for Faxe kommune. Closing #71

## [2.0.22] - `2024-04-07`

### What's Changed

- Added missing container for Svendborg kommune. Closing [#68](https://github.com/briis/affalddk/issues/68)
- Added missing container for Mariagerfjord kommune. Closing [#67](https://github.com/briis/affalddk/issues/67)
- Exporting danish `WEEKDAYS` and the short form `WEEKDAYS_SHORT` so that it can be used in other programs

## [2.0.21] - `2024-04-05`

### What's Changed

- Re-added `Miljøboks` for Gentofte kommune. Closing [#64](https://github.com/briis/affalddk/issues/64)

## [2.0.20] - `2024-04-02`

### What's Changed

- Converted last_updated value to a UTC Datetime object
- Added `Miljøboks` for Gentofte kommune. Closing [#64](https://github.com/briis/affalddk/issues/64)

## [2.0.19] - `2024-03-29`

### What's Changed

- Converted last_updated value to a Datetime string
- Added missing categories to PickupEvents Dataclass

## [2.0.18]- `2024-03-29`

### What's Changed

- The API Wrapper module is now renamed to `pyaffalddk`, as the plan is to support more than RenoWeb in the future. So even though this is V2.0.18, this is basically the first version, and contains the same functionality as `pyrenoweb` V2.0.17, just with new function and procedure names.

## [2.0.17] - `2024-03-26`

### What's Changed

- Fixed categories for Sorø kommune

## [2.0.16] - `2024-03-26`

### What's Changed

- Removed Furesø kommune as they are no longer using Renoweb.
- Added Lejre kommune, that was left out in the initial release.
- Fixed categories for Solrød kommune

## [2.0.15] - `2024-03-23`

### What's Changed

- Placing Textil correctly for Roskilde, Aalborg (and possible other Municipalities).
- Adding new category `papirglasmetalplast`. **Note** You need to download the image files again.
- Fixing missing containers for Lyngby-Taarbæk
- Fixing occasionally wrong address id being returned.

## [2.0.14] - `2024-03-22`

### What's Changed

- Adding support for the `Next Pickup` sensor, to display data for all containers being picked up that day.
- Fixing missing containers for Vordingborg Kommune


## [2.0.13] - `2024-03-22`

### What's Changed

- Fixing datetime to date conversion

## [2.0.12] - `2024-03-22`

### What's Changed

- see release notes for V2.0.5 of https://github.com/briis/affalddk as alle changes here are reflected there.

## [2.0.11] - `2024-03-12`

### What's Changed

- Fixing the Genbrug category for Kerteminde kommune

## [2.0.10] - `2024-03-10`

### What's Changed

- Fixing the Genbrug category for Hvidovre kommune
- Fixing the Genbrug category for Greve kommune
- Fixing the Genbrug category for Egedal kommune
- Fixing the Genbrug category for Rudersdal kommune
- Fixing the Genbrug category for Høje-Taastrup kommune

## [2.0.9] - `2024-03-09`

### What's Changed
- `Genbrug` is used for many different types of Containers, so there is now a new function that can handle these type of containers more generic, instead of by Municipality.
- Adding more material details to identify containers


  ## [2.0.8] - `2024-03-09`

  ### What's Changed
  - `Genbrug` is used for many different types of Containers, so there is now a new function that can handle these type of containers more generic, instead of by Municipality.
  - Reverting the 2.0.7 implementation of embedded images, as size was too big for HA. Will be reimplemented, once I find a way to reduce the size.

  ## [2.0.6] - `2024-03-07`

  ### What's Changed

  - Added Allerød to the list of Municipalities that need special handling of the `Genbrug` container.

  ## [2.0.5] - `2024-03-07`

  ### What's Changed

  - Added handling of Special cases where Municipalities use the same Type for several Containers. For the identified Municipalities, we now do a second validation on other fields to place the Container in the right type.
  - Handling the case where the same Road exists more than once in a Municipality. There is now a requirement to enter the Zipcode of the Address when setting up a new entity in Home Assistant.
  - Fixing missing containers in Aalborg. Closing https://github.com/briis/affalddk/issues/11
  - Added Rudersdal back to the list as they do work with this Integration. Closing https://github.com/briis/affalddk/issues/8

  ## [2.0.4] - `2024-03-02`

  ### Changes

* Removed the following Municipalities as they are not supported:
  * Balleup
  * Billund
  * Fanø
  * Favrskov
  * Fredericia
  * Frederikshavn
  * Guldborgsund
  * Haderslev
  * Herning
  * Holbæk
  * Holstebro
  * Ikast-Brande
  * Ishøj - They use the API, but do not supply dates, only textual descriptions, which cannot be converted to dates.
  * Kalundborg
  * Kolding
  * Læsø
  * Lolland
  * Middelfart
  * Morsø
  * Norddjurs
  * Nordfyns
  * Nyborg
  * Odder
  * Odense
  * Silkeborg
  * Skanderborg
  * Skive
  * Struer
  * Syddjurs
  * Thisted
  * Vejle
  * Vesthimmerland
  * Viborg
  * Tønder - They use the API in a Non-Standard way. Still under investigation if I can retrieve the data
  * Vallensbæk

* Added new function to support Municipalities that only supply weekdays. (Albertslund, Furesø).
* Added new garbage type `plastmetalmadmdk` which holds *Plast, Metal, Mad & Drikkekartoner*
* Added new garbage type `pappapir` which holds *Pap & Papir*
* Added new garbage type `tekstil` which holds *Tekstilaffald*
* Added new garbage type `glasplast` which holds *Glas, Plast & Madkartoner*
* Added new garbage type `plastmetalpapir` which holds *Plast, Metal & Papir*
* Fixed bug when Garbage Type could be in more than pickup type. Happens when partial strings are the same.

</details>
