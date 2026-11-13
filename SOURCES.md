# Sources

<!-- Generated from data/sources.toml by `python -m grow_guide_qa.sources render`. Edit the manifest, not this file. -->

The corpus is 10 public guides on growing microgreens and indoor farming. Licenses were checked against each publication on 2026-11-13.

- **In repo:** the license allows redistribution, so the PDF is committed under `data/vendored/`.
- **Downloaded:** the PDF is fetched from the publisher at setup time into `data/raw/`, which git ignores. Run `python -m grow_guide_qa.sources fetch`.

Every file is checked against the SHA-256 checksum pinned in the manifest, so the corpus behind the evaluation results can be reproduced exactly.

| ID | Document | Publisher | Year | Topic | License | Copy |
| --- | --- | --- | --- | --- | --- | --- |
| `vt-spes-756` | [Introduction to Microgreen Production in Indoor Vertical Farms and Greenhouses](https://pubs.ext.vt.edu/SPES/spes-756.html) | Virginia Cooperative Extension | 2026 | microgreens | VCE reuse permission | In repo |
| `uky-ccd-microgreens` | [Microgreens (crop profile CCD-CP-104)](https://publications.ca.uky.edu/sites/publications.ca.uky.edu/files/microgreens.pdf) | University of Kentucky Center for Crop Diversification | 2018 | microgreens | All rights reserved (no license stated) | Downloaded |
| `utk-w346j` | [Small-scale Microgreen Production (W 346-J)](https://solutions.tennessee.edu/publication/W346J) | University of Tennessee Extension | 2017 | microgreens | All rights reserved (no license stated) | Downloaded |
| `unr-microgreens-safety` | [Microgreens and Produce Safety](https://extension.unr.edu/4h/pub.aspx?PubID=3468) | University of Nevada, Reno Extension (Desert Farming Initiative) | 2020 | microgreens | All rights reserved | Downloaded |
| `usda-ars-greens-2014` | [Specialty Greens Pack a Nutritional Punch](https://agresearchmag.ars.usda.gov/2014/jan/greens) | USDA Agricultural Research Service (Agricultural Research magazine) | 2014 | microgreens | Public domain (U.S. government work) | Downloaded |
| `vt-spes-751` | [What is Controlled Environment Agriculture?](https://www.pubs.ext.vt.edu/SPES/spes-751.html) | Virginia Cooperative Extension | 2026 | indoor farming | VCE reuse permission | In repo |
| `vt-spes-462` | [Hydroponic Production of Edible Crops: Management Basics](https://www.pubs.ext.vt.edu/SPES/spes-462/spes-462.html) | Virginia Cooperative Extension | 2023 | indoor farming | VCE reuse permission | In repo |
| `vt-spes-463` | [Hydroponic Production of Edible Crops: Nutrient Film Technique (NFT) Systems](https://www.pubs.ext.vt.edu/content/pubs_ext_vt_edu/en/SPES/spes-463/spes-463.html) | Virginia Cooperative Extension | 2023 | indoor farming | VCE reuse permission | In repo |
| `vt-spes-464` | [Hydroponic Production of Edible Crops: Deep Water Culture (DWC) Systems](https://www.pubs.ext.vt.edu/SPES/spes-464/spes-464.html) | Virginia Cooperative Extension | 2023 | indoor farming | VCE reuse permission | In repo |
| `vt-spes-466` | [Hydroponic Production of Edible Crops: System and Crop Comparisons](https://www.pubs.ext.vt.edu/SPES/spes-466/spes-466.html) | Virginia Cooperative Extension | 2023 | indoor farming | VCE reuse permission | In repo |

## License notes

### `vt-spes-756`

*Introduction to Microgreen Production in Indoor Vertical Farms and Greenhouses*, by Kaylee A. South, Grayson Snead, John Roark, Michael R. Evans, Amy Turner. Virginia Cooperative Extension, 2026.

- PDF: <https://pubs.ext.vt.edu/content/dam/pubs_ext_vt_edu/spes/spes-756/SPES-756.pdf>
- License: VCE reuse permission. The publication page says VCE materials are "available for public use, reprint, or citation without further permission", with credit to the authors, Virginia Cooperative Extension, Virginia Tech and Virginia State University.

### `uky-ccd-microgreens`

*Microgreens (crop profile CCD-CP-104)*, by Cheryl Kaiser, Matt Ernst. University of Kentucky Center for Crop Diversification, 2018.

- PDF: <https://publications.ca.uky.edu/sites/publications.ca.uky.edu/files/microgreens.pdf>
- License: All rights reserved (no license stated). The PDF carries no license or reuse statement, so default copyright applies.

### `utk-w346j`

*Small-scale Microgreen Production (W 346-J)*, by Natalie Bumgarner, Rosalie Metallo. University of Tennessee Extension, 2017.

- PDF: <https://solutions.tennessee.edu/?view_pub_pdf=982>
- License: All rights reserved (no license stated). Neither the PDF nor its publication page carries a license or reuse statement, so default copyright applies.

### `unr-microgreens-safety`

*Microgreens and Produce Safety*, by Jill Moe. University of Nevada, Reno Extension (Desert Farming Initiative), 2020.

- PDF: <https://naes.agnt.unr.edu/PMS/Pubs/2020-3468.pdf>
- License: All rights reserved. The PDF states "Copyright © 2020 Desert Farming Initiative, All rights reserved."

### `usda-ars-greens-2014`

*Specialty Greens Pack a Nutritional Punch*, by Rosalie Marion Bliss. USDA Agricultural Research Service (Agricultural Research magazine), 2014.

- PDF: <https://agresearchmag.ars.usda.gov/AR/archive/2014/Jan/greens0114.pdf>
- License: Public domain (U.S. government work). Written by ARS staff; works of the U.S. federal government are not subject to copyright in the United States (17 U.S.C. § 105). It is downloaded rather than committed only because the PDF is 10 MB of mostly photos.

### `vt-spes-751`

*What is Controlled Environment Agriculture?*, by Mitchell Doss, Kaylee A. South, J. Scott Lowman, Michael R. Evans. Virginia Cooperative Extension, 2026.

- PDF: <https://www.pubs.ext.vt.edu/content/dam/pubs_ext_vt_edu/spes/spes-751/SPES-751.pdf>
- License: VCE reuse permission. The publication page says VCE materials are "available for public use, reprint, or citation without further permission", with credit to the authors, Virginia Cooperative Extension, Virginia Tech and Virginia State University.

### `vt-spes-462`

*Hydroponic Production of Edible Crops: Management Basics*, by Joyce Latimer, Amber Vallotton, Toni Sperry, Chris Mullins, Holly Scoggins. Virginia Cooperative Extension, 2023.

- PDF: <https://www.pubs.ext.vt.edu/content/dam/pubs_ext_vt_edu/spes/spes-462/SPES-462.pdf>
- License: VCE reuse permission. The publication page says VCE materials are "available for public use, reprint, or citation without further permission", with credit to the authors, Virginia Cooperative Extension, Virginia Tech and Virginia State University.

### `vt-spes-463`

*Hydroponic Production of Edible Crops: Nutrient Film Technique (NFT) Systems*, by Chris Mullins, Amber Vallotton, Joyce Latimer, Toni Sperry, Holly Scoggins. Virginia Cooperative Extension, 2023.

- PDF: <https://www.pubs.ext.vt.edu/content/dam/pubs_ext_vt_edu/spes/spes-463/SPES-463.pdf>
- License: VCE reuse permission. The publication page says VCE materials are "available for public use, reprint, or citation without further permission", with credit to the authors, Virginia Cooperative Extension, Virginia Tech and Virginia State University.

### `vt-spes-464`

*Hydroponic Production of Edible Crops: Deep Water Culture (DWC) Systems*, by Chris Mullins, Amber Vallotton, Joyce Latimer, Toni Sperry, Holly Scoggins. Virginia Cooperative Extension, 2023.

- PDF: <https://www.pubs.ext.vt.edu/content/dam/pubs_ext_vt_edu/spes/spes-464/SPES-464.pdf>
- License: VCE reuse permission. The publication page says VCE materials are "available for public use, reprint, or citation without further permission", with credit to the authors, Virginia Cooperative Extension, Virginia Tech and Virginia State University.

### `vt-spes-466`

*Hydroponic Production of Edible Crops: System and Crop Comparisons*, by Toni Sperry, Amber Vallotton, Chris Mullins, Joyce Latimer, Holly Scoggins. Virginia Cooperative Extension, 2023.

- PDF: <https://www.pubs.ext.vt.edu/content/dam/pubs_ext_vt_edu/spes/spes-466/SPES-466.pdf>
- License: VCE reuse permission. The publication page says VCE materials are "available for public use, reprint, or citation without further permission", with credit to the authors, Virginia Cooperative Extension, Virginia Tech and Virginia State University.

## Considered and left out

- [Microgreens: A New Specialty Crop (UF/IFAS EDIS HS1164)](https://edis.ifas.ufl.edu/publication/HS1164): The publication page now returns HTTP 410 Gone, and the journal mirror refuses automated requests.
- [Growing Microgreens for the Mississippi Gardener (Mississippi State P2857)](https://extension.msstate.edu/sites/default/files/publications/publications/P2857_web.pdf): The PDF and its web page return HTTP 404.
- [Grow Your Own Microgreens (Utah State University Extension)](https://digitalcommons.usu.edu/extension_curall/2479): The PDF host refuses automated downloads, so it could not be fetched at setup time.
- [Growing Microgreens and The ABCs of Microgreens (Penn State Extension)](https://extension.psu.edu/growing-microgreens): Web articles only, with no PDF; leaving them out keeps one extraction path (PDF) and stable checksums.
- [Modern indoor farming and food safety (FAO, 2025)](https://doi.org/10.4060/cd6554en): The FAO repository refuses automated requests, so neither the file nor its license could be checked.
- [Farming Foundations in Hydroponics (Virginia Cooperative Extension SPES-468 to 472)](https://pubs.ext.vt.edu/SPES/spes-469/spes-469.html): Video only, with no text to retrieve from.
