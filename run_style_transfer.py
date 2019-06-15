import os
import subprocess
from pathlib import Path
from optparse import OptionParser
from itertools import cycle


def parse_args():
    parser = OptionParser()
    parser.add_option('-d', '--day-image-folder', dest='day_image_folder', default='day',
                      help='path to daytime images directory')
    parser.add_option('-n', '--night-image-folder', dest='night_image_folder', default='night',
                      help='path to nighttime images directory')
    parser.add_option('-o', '--output-folder', dest='output_folder', default='output',
                      help='path to output directory')              
    (options, args) = parser.parse_args()
    return options, args


def run_style_transfer(options):
    day_image_folder = Path(options.day_image_folder)
    night_image_folder = Path(options.night_image_folder)
    output_folder = Path(options.output_folder)
    os.makedirs(output_folder, exist_ok=True)
    for day_image_path, night_image_path in zip(day_image_folder.glob('*.jpg'), 
                                                cycle(night_image_folder.glob('*.jpg'))):
        print(day_image_path, night_image_path)
        command = [
            'python', 'demo.py', 
            '--content_image_path ' + str(day_image_path),
            '--content_seg_path ' + str(day_image_path.parent / day_image_path.stem) + '_segmap.png',
            '--style_image_path ' +  str(night_image_path),
            '--style_seg_path ' +  str(night_image_path.parent / night_image_path.stem) + '_segmap.png'
            '--output_image_path ' +  str(output_folder / day_image_path.stem) \
                                  + '_' + str(night_image_path.stem) + '.jpg'
        ]
        subprocess.call(command)


if __name__ == '__main__':
    options, args = parse_args()
    run_style_transfer(options)