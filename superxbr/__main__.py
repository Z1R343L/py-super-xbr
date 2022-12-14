def main():
    import os
    import argparse
    from PIL import Image

    parser = argparse.ArgumentParser(description='Upscale an image using the Super-xBR pixel art scaling algorithm.')

    parser.add_argument('input', metavar='INPUT', help='Input image file path')
    parser.add_argument('output', metavar='OUTPUT', help='Output image file path')
    parser.add_argument('-p', metavar='PASSES', dest='passes', type=int, default=1, choices=range(1, 10),
                        help='Number of times to apply the Super-xBR filter. The image scale is doubled each time the '
                             'filter is applied. (default: 1)')
    parser.add_argument('-m', metavar='MODE', dest='mode', type=str.upper, default='RGBA',
                        choices=['1', 'L', 'LA', 'I', 'P', 'RGB', 'RGBA', 'CMYK'],
                        help='Color mode of the output image file. Choices are 1, L, LA, I, P, RGB, '
                             'RGBA, or CMYK. Note that some color modes are not compatible with some image formats and '
                             'will raise an exception. (default: RGBA)')
    parser.add_argument('--quiet', dest='display_progress', action='store_false', help='Hide progress updates')

    args = parser.parse_args()

    # input file must exist
    if not os.path.exists(args.input):
        print(f"error: input file '{args.input}' does not exist")
        return

    # output file must end in a valid image file extension
    valid_extensions = tuple(Image.registered_extensions().keys())
    if not args.output.lower().endswith(valid_extensions):
        print(
            f"error: output file '{args.output}' does not end in a supported image file extension"
        )
        return

    # input must be an image
    try:
        im_input = Image.open(args.input)
    except IOError:
        print(f"error: '{args.input}' is not a valid image file")
        return

    # importing superxbr this takes a tiny bit of time, so don't do it until error checking is done
    from superxbr import superxbr

    im_output = superxbr.scale(im_input, args.passes, args.display_progress)

    if im_output.mode != args.mode:
        im_output = im_output.convert(args.mode)
    im_output.save(args.output)
    if args.display_progress:
        print(f'saved {args.output}')


if __name__ == '__main__':
    main()
