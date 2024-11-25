# Changelog for pyaffalddk

## Version 2.1.1

**Date**: `2024-11-25`

### What's Changed

* Adding the option to use iCalendar file as input source for Calendar data.
* Adding Odense Kommune to the list of supported municipalities
* Added new Material Type `Genbrugsspand, 240L (2-delt) (1 stk.)`. Closing [AffaldDK #186](https://github.com/briis/affalddk/issues/186)
* Bump `pyaffalddk` to V2.1.0

<details>
  <summary><b>Previous Changes</b></summary>

## Version 2.0.44

**Date**: `2024-11-18`

### What's Changed

* Fixing issue where there is a weekday present but next pick-up is undefined. Typically occurs around New Years time. Closing [AffaldDK #179](https://github.com/briis/affalddk/issues/179)
* Added December 31st of next year, if a Pickup Type is valid, but no current date is given.
* Bump `pyaffalddk` to V2.0.44

## Version 2.0.41

**Date**: `2024-10-16`

### What's Changed

* Added new Material Type `juletrae` and also added new image. Closing [AffaldDK #165](https://github.com/briis/affalddk/issues/165)
* Bump `pyaffalddk` to V2.0.41

## Version 2.0.40

**Date**: `2024-10-03`

### What's Changed

* Start Fixing issues, after Bornholm has changed naming of many un its. Contributing to [AffaldDK #159](https://github.com/briis/affalddk/issues/159)
* Bump `pyaffalddk` to V2.0.40

## Version 2.0.39

**Date**: `2024-09-23`

### What's Changed

* Fixing missing Types in Svendborg. Closing [AffaldDK #151](https://github.com/briis/affalddk/issues/151)
* Fixing missing Types in Horsens. Closing [pyaffalddk #14](https://github.com/briis/pyaffalddk/issues/14)
* Bump `pyaffalddk` to V2.0.39

## Version 2.0.38

**Date**: `2024-08-16`

### What's Changed

* Fixing missing Types in Solrød. Closing [AffaldDK #139](https://github.com/briis/affalddk/issues/139)
* Fixing missing Types in Egedal. Closing [AffaldDK #142](https://github.com/briis/affalddk/issues/142)
* Bump `pyaffalddk` to V2.0.38

## Version 2.0.37

**Date**: `2024-08-13`

### What's Changed

* Fixing missing Types in Vordingborg. Closing [AffaldDK #136](https://github.com/briis/affalddk/issues/136)
* Bump `pyaffalddk` to V2.0.37

## Version 2.0.36

**Date**: `2024-07-29`

### What's Changed

* Fixing missing Types in Ringsted. Closing [AffaldDK #133](https://github.com/briis/affalddk/issues/133)
* Bump `pyaffalddk` to V2.0.36

## Version 2.0.35

**Date**: `2024-07-29`

### What's Changed

* Fixing missing Types in Albertslund. Closing [AffaldDK #129](https://github.com/briis/affalddk/issues/129)
* Bump `pyaffalddk` to V2.0.35


## Version 2.0.34

**Date**: `2024-07-05`

### What's Changed

* Fixing missing containers in Esbjerg. Closing [AffaldDK #117](https://github.com/briis/affalddk/issues/117)
* Fixing missing containers in Gribskov. Closing [AffaldDK #118](https://github.com/briis/affalddk/issues/118)
* Bump `pyaffalddk` to V2.0.34


## Version 2.0.31

**Date**: `2024-06-14`

### What's Changed

## Version 2.0.33

**Date**: `2024-06-29`

### What's Changed

* Adding Bornholm as new Municipality. I have limited test data to go on, but some data is being returned. If anything is missing, please report back. Closing [AffaldDK #114](https://github.com/briis/affalddk/issues/114)
* Bump `pyaffalddk` to V2.0.33

* Fixing missing details for Faxe. Closing #4
* Fixing missing details for Lyngby-Taarbæk. Cloising [AffaldDK #105](https://github.com/briis/affalddk/issues/105)
* Bump `pyaffalddk` to V2.0.31

## Version 2.0.30

**Date**: `2024-05-27`

### What's Changed

* Fixing missing details for Slagelse. Closing #97
* Bump `pyaffalddk` to V2.0.30

## Version 2.0.29

**Date**: `2024-05-12`

### What's Changed

* Fixing missing details for Vejen and Randers. Closing #87
- Bump `pyaffalddk` to V2.0.29

# Version 2.0.28

**Date**: `2024-05-04`

### What's Changed

- Fixed missing containers for Solrød Kommune.
- Fixed missing containers for Egedal Kommune. Closing #84
- Fixed missing containers for Lyngby-Taarbæk Kommune. Closing #83
- Fixed missing containers for Glostrup Kommune. Closing #79
- Added two new Categories: `restaffald` and `madaffald`. These are new as separat containers.

## Version 2.0.26

**Date**: `2024-04-22`

### What's Changed

- Modified change from 2.0.25, as it caused problems for many with the category Storskrald. It will now work for all, including Gladsaxe.
- Added more details to warning if category not found. Makes it easier to debug when people report errors.

## Version 2.0.25

**Date**: `2024-04-19`

### What's Changed

- Added new category Plast, MDK, Glas & Metal.
- Added missing containers for Varde kommune. Closing #75
- Added missing storskrald for Solrød

## Version 2.0.23

**Date**: `2024-04-16`

### What's Changed

- Added `|` as separator to Next Pickup sensor, to easier identify items.
- Added missing containers for Papir & Plast and Metal & Glas for Faxe kommune. Closing #71

## Version 2.0.22

**Date**: `2024-04-07`

### What's Changed

- Added missing container for Svendborg kommune. Closing [#68](https://github.com/briis/affalddk/issues/68)
- Added missing container for Mariagerfjord kommune. Closing [#67](https://github.com/briis/affalddk/issues/67)
- Exporting danish `WEEKDAYS` and the short form `WEEKDAYS_SHORT` so that it can be used in other programs

## Version 2.0.21

**Date**: `2024-04-05`

### What's Changed

- Re-added `Miljøboks` for Gentofte kommune. Closing [#64](https://github.com/briis/affalddk/issues/64)

## Version 2.0.20

**Date**: `2024-04-02`

### What's Changed

- Converted last_updated value to a UTC Datetime object
- Added `Miljøboks` for Gentofte kommune. Closing [#64](https://github.com/briis/affalddk/issues/64)

## Version 2.0.19

**Date**: `2024-03-29`

### What's Changed

- Converted last_updated value to a Datetime string
- Added missing categories to PickupEvents Dataclass

## Version 2.0.18

**Date**: `2024-03-29`

### What's Changed

- The API Wrapper module is now renamed to `pyaffalddk`, as the plan is to support more than RenoWeb in the future. So even though this is V2.0.18, this is basically the first version, and contains the same functionality as `pyrenoweb` V2.0.17, just with new function and procedure names.

## Version 2.0.17

**Date**: `2024-03-26`

### What's Changed

- Fixed categories for Sorø kommune

## Version 2.0.16

**Date**: `2024-03-26`

### What's Changed

- Removed Furesø kommune as they are no longer using Renoweb.
- Added Lejre kommune, that was left out in the initial release.
- Fixed categories for Solrød kommune

## Version 2.0.15

**Date**: `2024-03-23`

### What's Changed

- Placing Textil correctly for Roskilde, Aalborg (and possible other Municipalities).
- Adding new category `papirglasmetalplast`. **Note** You need to download the image files again.
- Fixing missing containers for Lyngby-Taarbæk
- Fixing occasionally wrong address id being returned.

## Version 2.0.14

**Date**: `2024-03-22`

### What's Changed

- Adding support for the `Next Pickup` sensor, to display data for all containers being picked up that day.
- Fixing missing containers for Vordingborg Kommune


## Version 2.0.13

**Date**: `2024-03-22`

### What's Changed

- Fixing datetime to date conversion

## Version 2.0.12

**Date**: `2024-03-22`

### What's Changed

- see release notes for V2.0.5 of https://github.com/briis/affalddk as alle changes here are reflected there.

## Version 2.0.11

**Date**: `2024-03-12`

### What's Changed

- Fixing the Genbrug category for Kerteminde kommune

## Version 2.0.10

**Date**: `2024-03-10`

### What's Changed

- Fixing the Genbrug category for Hvidovre kommune
- Fixing the Genbrug category for Greve kommune
- Fixing the Genbrug category for Egedal kommune
- Fixing the Genbrug category for Rudersdal kommune
- Fixing the Genbrug category for Høje-Taastrup kommune

## Version 2.0.9

**Date**: `2024-03-09`

### What's Changed
- `Genbrug` is used for many different types of Containers, so there is now a new function that can handle these type of containers more generic, instead of by Municipality.
- Adding more material details to identify containers


  ## Version 2.0.8

  **Date**: `2024-03-09`

  ### What's Changed
  - `Genbrug` is used for many different types of Containers, so there is now a new function that can handle these type of containers more generic, instead of by Municipality.
  - Reverting the 2.0.7 implementation of embedded images, as size was too big for HA. Will be reimplemented, once I find a way to reduce the size.

  ## Version 2.0.6

  **Date**: `2024-03-07`

  ### What's Changed

  - Added Allerød to the list of Municipalities that need special handling of the `Genbrug` container.

  ## Version 2.0.5

  **Date**: `2024-03-07`

  ### What's Changed

  - Added handling of Special cases where Municipalities use the same Type for several Containers. For the identified Municipalities, we now do a second validation on other fields to place the Container in the right type.
  - Handling the case where the same Road exists more than once in a Municipality. There is now a requirement to enter the Zipcode of the Address when setting up a new entity in Home Assistant.
  - Fixing missing containers in Aalborg. Closing https://github.com/briis/affalddk/issues/11
  - Added Rudersdal back to the list as they do work with this Integration. Closing https://github.com/briis/affalddk/issues/8

  ## Version 2.0.4

  **Date**: `2024-03-02`

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
