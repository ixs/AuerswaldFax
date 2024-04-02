import pdf2image
from PIL import ImageOps
from PIL import TiffImagePlugin
from io import BytesIO

class AuerswaldFaxImage:
    """Image handling class"""
    def __init__(self):
        self.images = []

    def read_pdf(self, filename):
        """Read a PDF into a PIL image"""
        self.images = pdf2image.convert_from_path(filename)

    def display_images(self):
        """Show a PIL image for debugging"""
        print("Showing Images")
        for image in self.images:
            image.show()

    def convert(self, enhance=True):
        """
        Convert a PIL image into a something that has the right format for sending
        through an Auerswald PBX
        """
        images = []
        for image in self.images:
            size = image.size
            ratio = size[0] / size[1]
            ratio = 210 / 297
            if enhance:
                image = ImageOps.autocontrast(image)
            image = image.resize((1728, int(1728 / ratio)))
            image = image.convert(mode="1")
            images.append(image)
        self.images = images

    def as_tiff(self):
        byte_io = BytesIO()
        # Handle reversed photometrics
        SAVE_INFO = TiffImagePlugin.SAVE_INFO
        TiffImagePlugin.SAVE_INFO = {
            "1": ("1", TiffImagePlugin.II, 0, 1, (1,), None),
        }
        images = []
        for image in self.images:
            image = image.convert(mode="L")
            image = ImageOps.invert(image)
            image = image.convert(mode="1")
            images.append(image)
        images[0].save(
            byte_io,
            format="TIFF",
            compression="group3",
            save_all=True,
            append_images=images[1:],
            resolution_unit=2,
            dpi=(203, 196),
            tiffinfo={274: 1, 292: 0, 278: 1, 254: 0, 277: 1},
        )
        TiffImagePlugin.SAVE_INFO = SAVE_INFO
        self.fax = byte_io.getbuffer()

    def write_to_file(self, filename="fax.tiff"):
        with open(filename, "wb") as f:
            f.write(self.fax.tobytes())