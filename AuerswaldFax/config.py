
    def __init__(self, configfile="aufax.json"):
        self.images = []
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
