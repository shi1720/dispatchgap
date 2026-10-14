# revolutionary-networks
This is a public dataset of metadata created from documents from the University of Virginia Press's [Rotunda American History Collection](https://www.upress.virginia.edu/rotunda/), covering the period of 1771-1783. This data has been released in association with a grant from the National Endowment for the Humanities, for which we created a website exploring data visualisations of networks of communication through the revolutionary war. If you use this data for your research and want it included as a link on the project's main website, [revolutionary-networks.org](https://revolutionary-networks.org), contact [rotunda-upress@virginia.edu](mailto:rotunda-upress@virginia.edu).

## Available Metadata, pulled from 40,691 documents. This data has been created by interally by Rotunda and does not include any transcripts from the actual letters. 
* Document ID: Official identifer for within the Rotunda American History Collection
* Author: Author of document
* Recipient: Recipient of document
* Date: Date associated with the document
* Publication: Source publication from which this metadata was collected. Abbreviation (Key below)
* Founders Online: Link to full document transcription on Founders Online (where available)
* Rotunda: Link to document in the Rotunda collection (may require institutional access)
* authorIDs: Associated ID for person, pulled from Rotunda's [People of The Founding Era prosopography database](https://pfe.upress.virginia.edu). 
* recipientIDs: Associated ID for person, pulled from Rotunda's [People of The Founding Era prosopography database](https://pfe.upress.virginia.edu).
* Location: Through several levels of human and machine processing, the location selected for the origin of the document. 
* GeonameID: The returned ID for the geoname entry matching to the value in the location field. [https://www.geonames.org/](https://www.geonames.org/)
* Coordinates: Combined GPS coordinates, from the reconciled Geonames.org entry
* Latitude: latitude, from the reconciled Geonames.org entry
* Longitude: longitude, from the reconciled Geonames.org entry
* Country_code: country code, from the reconciled Geonames.org entry
* Country_name: Country name, from the reconciled Geonames.org entry
* Admin1: Administrative area, level 1, from the reconciled Geonames.org entry
* Admin2: Adminstrative area, level 2, from the reconciled Geonames.org entry
* Hierarchy: Full breadcrumb for location, from the reconciled Geonames.org entry

## Collections represented in metadata, by proportion of dataset, having content from Jan 1, 1771 through Dec 31, 1783. Including publication code, and original publisher and copyright holder of the volume containing the source material. 
* The Papers of George Washington - GEWN - (University of Virginia Press)
* The Papers of Benjamin Franklin - BNFN - (Yale University Press)
* The Adams Family Papers - ADMS - (Massachusetts Historical Society)
* The Papers of Thomas Jefferson - TSJN - (Princeton Univeristy Press and Thomas Jefferson Foundation)
* The Papers of James Madison - JSMN - (University of Virginia Press)
* The Selected Papers of John Jay - JNJY - (The Trustees of Columbia University in the City of New York)
* The Papers of Alexander Hamilton - ARHN - (Columbia University Press)
* The Papers of Eliza Lucas Pinckney and Harriott Pinckney Horry: Digital Edition - PIHO - (University of Virginia Press, Rotunda Digital Imprint)
* The Papers of the Revolutionary Era Pinckney Statesmen Digital Edition - PNKY - (University of Virginia Press, Rotunda Digital Imprint)
* The Letters of Benjamin Rush - RUSH - (American Philosophical Society)
* The Documentary History of the Ratification of the Constitution - RNCN - (The State Historical Society of Wisconsin)
* The Papers of John Marshall - JNML - (The University of North Carolina Press)

## License & Attribution

The dataset in this repository (`rotunda_data_1771-1783_full.csv`) is licensed under
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

The license applies to the **dataset compilation** and to the **metadata created by Rotunda** —
person disambiguation and identifiers drawn from
[People of the Founding Era](https://pfe.upress.virginia.edu), and location reconciliation
against [GeoNames](https://www.geonames.org/). The bibliographic fields (author, recipient,
date, source) are statements of fact and are not claimed as original work. The underlying
letter texts are **not included** in this dataset and the source editions (see *Collections Represented*) remain under the copyright of their
respective publishers.

**Please cite as:**

> Rotunda, University of Virginia Press. *Revolutionary Networks: Correspondence Metadata,
> 1771–1783* [dataset]. 2026. https://github.com/rotunda-uvap/revolutionary-networks

This dataset is corrected and expanded over time; the version in this repository is the
canonical, maintained copy.