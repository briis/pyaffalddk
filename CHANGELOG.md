# Changelog for pyaffalddk

## Version 2.0.19

**Date**: `2024-03-29`

### What's Changed

- Converted last_updated value to a Datetime string
- Added missing categories to PickupEvents Dataclass

<details>
  <summary><b>Previous Changes</b></summary>

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
