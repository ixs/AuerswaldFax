import requests
import logging
import json
from requests_toolbelt import MultipartEncoder
import AuerswaldFax.errors as AuerswaldFaxErrors
import AuerswaldFax.image as AuerswaldFaxImage

class Client:
    def __init__(self, configfile="aufax.json"):
        with open(configfile) as json_file:
            self.config = json.load(json_file)
        self.config.update(
            {
                "pbx_url": f"{'https' if self.config['use_ssl'] else 'http'}://{self.config['pbx_address']}"
            }
        )
        self.ssl_verify = self.config["verify_ssl"]
        if not self.ssl_verify:
            from requests.packages.urllib3.exceptions import InsecureRequestWarning
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def enable_debug(self):
        import http.client as http_client

        http_client.HTTPConnection.debuglevel = 1

        # You must initialize logging, otherwise you'll not see debug output.
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    def test_login_data(self):
        url = f"{self.config['pbx_url']}/daalogin"
        r = requests.get(
            url,
            auth=requests.auth.HTTPDigestAuth(
                self.config["pbx_username"], self.config["pbx_password"]
            ),
            verify=self.ssl_verify,
        )
        if r.status_code == 200 and r.text == "0":
            return True
        return False

    def enqueue(self, destination):
        files = {"": ("fax.tiff", self.fax.tobytes(), "image/tiff")}

        # We need to rewrite the MIME headers to add a faxdest field.
        # Ugly hack
        encoder = MultipartEncoder(fields=files)
        for part in encoder.parts:
            if "Content-Disposition" in part.headers.decode():
                new_header = []
                for header in part.headers.decode().split("\r\n"):
                    if header.startswith("Content-Disposition"):
                        fields = header.split("; ")
                        fields.insert(2, f'faxdest="{destination}"')
                        header = "; ".join(fields)
                    new_header.append(header)
                part.headers = "\r\n".join(new_header).encode()

        url = f"{self.config['pbx_url']}/faxupload"

        r = requests.post(
            url,
            auth=requests.auth.HTTPDigestAuth(
                self.config["pbx_username"], self.config["pbx_password"]
            ),
            verify=self.ssl_verify,
            # files=files
            data=encoder.to_string(),
            headers={"Content-Type": encoder.content_type},
        )
        if r.status_code == 200:
            print("Faxserver hat das Fax erfolgreich entgegengenommen")
        else:
            try:
                print(
                    f"Es ist ein Fehler aufgetreten: {AuerswaldFaxErrors.errors[int(r.status_code)]}"
                )
            except KeyError:
                print(
                    f"Es ist ein unbekannter Fehler aufgetreten: {r.status_code} {r.reason}"
                )

    def read_pdf(self, filename):
        return AuerswaldFaxImage.read_pdf(filename)
    
    def as_tiff(self):
        return AuerswaldFaxImage.AuerswaldFaxImage.as_tiff(self)
    
    def write_to_file(self, filename="fax.tiff"):
        return AuerswaldFaxImage.AuerswaldFaxImage.write_to_file(self, filename="fax.tiff")
    
    def display_images(self):
        return AuerswaldFaxImage.AuerswaldFaxImage.display_images(self)