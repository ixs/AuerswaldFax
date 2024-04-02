from PIL import Image
from PIL import ImageFont, ImageDraw
#import datetime
from datetime import date, datetime, time
from babel.dates import format_date, format_datetime, format_time

class Tests:
    def __init__():
        pass

    def test_fax_simple(self, sender, destination):
        """Create a simple test fax using the python image library"""
        a4_size = (210, 297)
        fax_dpi = (203, 196)
        fax_px = (1728, None)

        image = Image.new("L", (1728, 2254), color="white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("Arial Bold.ttf", 300)
        text = "Testfax"
        size = draw.textbbox((0, 0), text, font)

        draw.text(((1728 - size[2] - size[3]) / 2, 50), "Test-Fax", font=font)
        font = ImageFont.truetype("Arial.ttf", 75)
        text = "Absender:\n" "Empfänger:\n" "Datum:\n" "Uhrzeit"
        size = draw.textbbox((100, 650), text, font, spacing=40)
        draw.multiline_text((100, 650), text, font=font, spacing=40)
        tzinfo = datetime.utcnow().astimezone().tzinfo
        text = (
            f"MSN {sender}\n"
            f"{destination}\n"
            f"{format_date(format='full', locale='de_DE')}\n"
            f"{format_time(format='HH:mm', tzinfo=tzinfo, locale='de')}"
        )
        draw.multiline_text((((size[0] + size[2])), 650), text, font=font, spacing=40)
        image = image.convert(mode="1")
        return image

    def test_fax_complex(self, sender, destination):
        """Create a complex pattern test fax using the python image library"""
        a4_size = (210, 297)
        fax_dpi = (203, 196)
        fax_px = (1728, 2254)

        image = Image.new("L", fax_px, color="white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("Arial Bold.ttf", 100)
        text = "Fax Test"
        size = draw.textbbox((0, 0), text, font)
        draw.text(((fax_px[0] - size[2] - size[3]) / 2, 10), text, font=font)
        font = ImageFont.truetype("Arial.ttf", 60)
        text = f"Datum: {format_date(format='full', locale='de_DE')}      Absender: {sender}"
        size = draw.textbbox((0, 0), text, font, spacing=40)
        draw.multiline_text(
            ((fax_px[0] - size[2] - size[3]) / 2, size[3] + 100),
            text,
            font=font,
            spacing=40,
        )

        padding = 75

        size = 650

        width = 1
        tlc = (padding, 350)
        color = 200
        color_stop = 0
        color_step = (color - color_stop) / (size / 2 / width)
        for i in range(0, int(size / 2), width):
            draw.ellipse(
                (tlc[0] + i, tlc[1] + i, tlc[0] + size - i, tlc[1] + size - i),
                fill=f"rgb({int(color)}, {int(color)}, {int(color)})",
                width=width,
            )
            color -= color_step

        width = 35
        tlc = (fax_px[0] - padding - size, 350)
        j = 0
        for i in range(0, int(size / 2), width):
            draw.ellipse(
                (tlc[0] + i, tlc[1] + i, tlc[0] + size - i, tlc[1] + size - i),
                fill="white" if j % 2 else "black",
                width=width,
            )
            j += 1

        width = 180
        tlc = ((fax_px[0] / 2) - (width / 2), 450)
        color = 0
        color_stop = 255
        color_step = (color_stop - color) / size
        for i in range(0, size):
            draw.line(
                [(tlc[0], tlc[1] + i), (tlc[0] + width, tlc[1] + i)],
                fill=round(color),
                width=width,
            )
            color += color_step

        height = 1000
        tlc = (padding, height)
        width = 50
        step = -10
        for i in range(width, 10, step):
            draw.line(
                [(padding, height + i * 6), (1728 - padding), height + i * 6],
                fill="black",
                width=i,
            )

        orig_height = 1350
        size = 100
        k = 0
        for width in [40, 20, 10, 5, 4, 3, 2, 1]:
            height = orig_height + ((size + 5) * k)
            j = 0
            for i in range(0, fax_px[0] - padding * 2, width):
                draw.line(
                    [(padding + i, height), (padding + i, height + size)],
                    fill="black" if j % 2 else "white",
                    width=width,
                )
                j += 1
            k += 1

        image = image.convert(mode="1")
        return image
