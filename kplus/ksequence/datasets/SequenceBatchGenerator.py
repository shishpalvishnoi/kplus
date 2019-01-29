# MIT License
#
# Copyright (c) 2018
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import cv2
import os, random
import numpy as np

from kplus.datasets.AbstractBatchGenerator import AbstractBatchGenerator


class SequenceBatchGenerator(AbstractBatchGenerator):
    def __init__(self):
        AbstractBatchGenerator.__init__(self)

        self._letters = ''

        self._patterns = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
        self._image_width = 0
        self._image_height = 0
        self._number_of_channels = 0

        self._maximum_text_length = 0
        self._downsample_factor = 1.0

        self._identifiers = []
        self._images = []
        self._texts = []

    def labels_to_text(self, labels):
        return ''.join(list(map(lambda x: self._letters[int(x)], labels)))

    def text_to_labels(self, text):
        return list(map(lambda x: self._letters.index(x), text))

    def _load_dataset(self, dataset_dir):
        if ((not os.path.exists(dataset_dir))
                or (not os.path.isdir(dataset_dir))):
            return (False)

        self._identifiers = []
        self._images = []
        self._texts = []

        image_filenames = os.listdir(dataset_dir)
        number_of_samples = 0
        for image_file in image_filenames:
            image_filename = os.path.join(dataset_dir, image_file)
            image = cv2.imread(image_filename, cv2.IMREAD_GRAYSCALE)
            if (image is None):
                continue

            image = cv2.resize(image, (self._image_width, self._image_height))
            image = image.astype(np.float32)
            image = (image / 255.0) * 2.0 - 1.0

            self._images.append(image.T)
            self._texts.append(image_file[0:-4])
            self._identifiers.append(number_of_samples)

            number_of_samples = number_of_samples + 1

        self.on_epoch_end()

        return (True)

    def _load_split(self, split_name, parameters):
        dataset_dir = parameters[split_name]['dataset_dir']
        dataset_dir = os.path.expanduser(dataset_dir)

        model_letters = parameters['model']['letters']
        self._letters = [letter for letter in model_letters]

        self._image_width = parameters['model']['image_width']
        self._image_height = parameters['model']['image_height']
        self._number_of_channels = parameters['model']['number_of_channels']

        self._batch_size = parameters[split_name]['batch_size']

        self._maximum_text_length = parameters['model']['maximum_text_length']
        self._downsample_factor = parameters['model']['downsample_factor']

        return (self._load_dataset(dataset_dir))

    def __getitem__(self, batch_index):

        lower_bound = batch_index * self._batch_size
        upper_bound = (batch_index + 1) * self._batch_size

        if (upper_bound > self.number_of_samples()):
            upper_bound = self.number_of_samples()
            lower_bound = upper_bound - self._batch_size

        X_data = np.zeros((self._batch_size, self._image_width,
                           self._image_height, self._number_of_channels))
        Y_data = np.zeros((self._batch_size, self._maximum_text_length))

        input_length = np.ones((self._batch_size, 1)) * (
            self._image_width // self._downsample_factor - 2)  # (bs, 1)
        label_length = np.zeros((self._batch_size, 1))  # (bs, 1)

        for index in range(lower_bound, upper_bound):
            target_index = index - lower_bound
            source_identifier = self._identifiers[index]

            input_image = self._images[self._identifiers[source_identifier]]
            input_image = input_image
            input_image = np.expand_dims(input_image, -1)

            text = self._texts[self._identifiers[source_identifier]]

            characters = self.text_to_labels(text)
            length = label_length[target_index] = len(text)

            X_data[target_index] = input_image
            Y_data[target_index][0:length] = characters[0:length]

        inputs = {
            'input_image': X_data,  # (bs, 128, 64, 1)
            'input_labels': Y_data,  # (bs, 8)
            'input_length': input_length,  # (bs, 1) -> value = 30
            'label_length': label_length  # (bs, 1) -> value = 8
        }

        outputs = {'ctc': np.zeros([self._batch_size])}

        return (inputs, outputs)