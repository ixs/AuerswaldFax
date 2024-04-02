# Auerswald FAX Client

The [Auerswald](https://www.auerswald.de/) COMpact and COMmander as well as the COMtrexx series of phone branch exchanges offer
an integrated fax server.  
These PBX systems support fax reception and will store incoming faxes on the PBX.  
Outgoing faxes are supported by Auerswald through a print driver for Windows which will enqueue the printed documents on the PBX for sending by the PBX.

For other operating systems, there's no driver, but Auerswald is offering a description of the interface on their FAQ page under the topic of [Auerswald Fax-Interface integration](https://www.auerswald.de/de/support/faq/wie-integriere-ich-die-auerswald-fax-schnittstelle-in-eigene-treiber-oder-software)

This repo contains a Python3 implementation of a Fax client for these Auerswald systems.

## Configuration

The configuration of the Fax client happens in the `aufax.json` file.
The file needs the following keys:

| Key Name | Example Value | Type | Description |
| -------- | ------------- | ---- | ----------- |
| pbx_address | 192.168.0.240 | _string_ | IP Address or hostname of the PBX system |
| pbx_username | 208 | _string_ | Username, usually the internal phone number of the owner of the fax box |
| pbx_password | secret | _string_ | Password for the corresponding username. Minimum 8 characters or a 6 digit PIN on the COMpact 3000. |
| access_number | 0 | _string_ | Phone number prefix needed to get an outside line, usually 0. |
| prepend_access_numer | false | _boolean_ | Whether to prepend the above suffix to the number dialed. Only set to `true` if automatic trunk access has been disabled. |
| use_ssl | false | _boolean_ | Use SSL to communicate with the PBX system |
| verify_ssl | false | _boolean_ | Whether to verify the SSL connection to the PBX system or not. Recommended to be false as the PBX uses a self-signed certificate |

## PBX configuration

- See the Auerswald tech note about [automatic trunk access and dial prefixes when using the fax driver](http://www.auerswald-root.de/download/datei/handbuch/Driver_Fax_Windows/Anlagenweite-automatische-Amtholung_plus_Faxtreiber_0816.pdf)
- Ensure at least one channel is reserved for fax or voicemail calls
- Ensure a faxbox has been created for the user configured in `aufax.json`

## Usage

TBD

## License

This code is licensed under the GPLv3 license.

## Further reading

1. https://docs.auerswald.de/COMpact_5200_5500_R/Help_de_12/index.html#page/Buch1/faxbox_versand_treibereinrichtung_task.html
2. https://www.auerswald-root.de/download/docs-xml/comtrexx/docs/1.2/de/COMtrexx/index.html#page/Help/vmf_faxbox_versand_topic.html
