#!/usr/bin/env python3

import argparse
import mimetypes

import AuerswaldFax.client as AuerswaldFaxClient
import AuerswaldFax.tests as AuerswaldFaxTests

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-ne", "--no-enhance", help="Do not enhance contrast", action="store_false"
    )
    parser.add_argument(
        "-d", "--debug", help="Enable network debugging", action="store_true"
    )
    parser.add_argument(
        "--simple-test",
        help="Generate a simple test fax and send it",
        action="store_true",
    )
    parser.add_argument(
        "--complex-test",
        help="Generate a complex test fax and send it",
        action="store_true",
    )
    parser.add_argument(
        "--show",
        help="Only display faxes, do not send",
        action="store_true",
    )
    parser.add_argument("-p", "--pdf-file", help="PDF file to send")
    parser.add_argument("destination", help="Fax number to dial")
    return parser.parse_args()

def main():
    args = parse_args()
    fax = AuerswaldFaxClient.Client()
    if args.simple_test:
        fax.images = [AuerswaldFaxTests.Tests.test_fax_simple(AuerswaldFaxTests.Tests, fax.config["pbx_username"], args.destination)]
    if args.complex_test:
        fax.images = [AuerswaldFaxTests.Tests.test_fax_complex(AuerswaldFaxTests.Tests, fax.config["pbx_username"], args.destination)]
    elif args.pdf_file:
        mimetype = mimetypes.guess_type(args.filename)[0]
        if mimetype == "application/pdf":
            fax.read_pdf(args.filename)
        fax.convert(enhance=args.no_enhance)
    fax.as_tiff()
    if args.show:
        fax.display_images()
        return
    fax.write_to_file()
    if args.debug:
        fax.enable_debug()
    fax.enqueue(args.destination)


if __name__ == "__main__":
    main()