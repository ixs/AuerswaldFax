class AuerswaldFaxErrors:
    errors = {
        302: "In diesem Fall muss der Versand nochmals mit der in der Meldung angegebenen URL durchgeführt werden.",
        401: "Der Teilnehmer ist unbekannt, oder das Passwort passt nicht.",
        403: "Der Teilnehmer ist zwar bekannt, Fax-Versand ist aber nicht aktiviert.",
        404: "Fax-Versand ist mit dieser Telefonanlage nicht möglich.",
        405: "Das Fax konnte nicht versendet werden. Pro Fax-Dokument sind nur max. 50 Seiten erlaubt.",
        415: "Der mimetype ist falsch, oder das Fax hat nicht das richtige Format.",
        503: "Der Fax-Server steht derzeit nicht zur Verfügung.",
        507: "Der Fax-Puffer der Telefonanlage ist überfüllt.",
    }
