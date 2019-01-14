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

import sys
import os
import argparse

import json

from kplus.ksequence.applications.SimpleOCR import SimpleOCR

K.set_learning_phase(0)
"""
def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--model_name',
        type=str,
        help='The name of the model.',
        choices=['base', 'bidirectional', 'attention'],
        default='base')

    parser.add_argument(
        '--feature_extractor',
        type=str,
        help='The name of the feature extractor.',
        choices=['simple_vgg', 'resnet_50'],
        default='simple_vgg')

    parser.add_argument(
        '--train_root_dir',
        type=str,
        help='Input train root directory where model weights are saved.',
        default='./train')

    parser.add_argument(
        '--max_number_of_epoch',
        type=int,
        help='The maximum number of training epoch.',
        default=30)

    parser.add_argument(
        '--train_dataset_dir',
        type=str,
        help='The directory where the train dataset files are stored.',
        default='./datasets/train/')

    parser.add_argument(
        '--test_dataset_dir',
        type=str,
        help='The directory where the test dataset files are stored.',
        default='./datasets/test/')

    return (parser.parse_args(argv))


def main(args):
    if (not (args.model_name in ['base', 'bidirectional', 'attention'])):
        raise ValueError(
            'The model name should be either base, bidirectional or attention.'
        )

    if (not (args.feature_extractor in ['simple_vgg', 'resnet_50'])):
        raise ValueError(
            'The feature extractor should be either simple_vgg, or resnet_50.')

    if (not args.train_dataset_dir):
        raise ValueError(
            'You must supply the train dataset directory with --train_dataset_dir.'
        )
    if (not args.test_dataset_dir):
        raise ValueError(
            'You must supply the test dataset directory with --test_dataset_dir.'
        )

    train_file_path = args.train_dataset_dir
    valid_file_path = args.test_dataset_dir
    epoch = args.max_number_of_epoch

    sequence_model = ModelFactory.simple_model(args.model_name)
    sequence_model.use_feature_extractor(args.feature_extractor)
    keras_model = sequence_model.keras_model(is_training=True)

    try:
        keras_model.load_weights('LSTM+BN4--26--0.011.hdf5')
        print("...Previous weight data...")
    except:
        print("...New weight data...")
        pass

    tiger_train = SimpleGenerator(train_file_path, img_w, img_h, batch_size,
                                  downsample_factor)
    tiger_train.build_data()

    tiger_val = SimpleGenerator(valid_file_path, img_w, img_h, val_batch_size,
                                downsample_factor)
    tiger_val.build_data()

    ada = Adadelta()

    # Dummy lambda function for the loss
    keras_model.compile(
        loss={
            'ctc': lambda y_true, y_pred: y_pred
        },
        optimizer=ada,
        metrics=['accuracy'])

    early_stop = EarlyStopping(
        monitor='loss', min_delta=0.001, patience=4, mode='min', verbose=1)

    train_root_dir = os.path.expanduser(args.train_root_dir)
    checkpoint_path = os.path.join(train_root_dir,
                                   'model--{epoch:03d}--{val_loss:.5f}.hdf5')
    tensorboard_path = os.path.join(train_root_dir, 'tensorboard')

    checkpoint = ModelCheckpoint(
        filepath=checkpoint_path,
        monitor='loss',
        verbose=1,
        mode='min',
        period=1)

    tensor_board = TensorBoard(
        log_dir=tensorboard_path,
        histogram_freq=0,
        write_graph=True,
        write_images=False)

    keras_model.fit_generator(
        generator=tiger_train.next_batch(),
        steps_per_epoch=int(tiger_train.n / batch_size),
        callbacks=[checkpoint, early_stop, tensor_board],
        epochs=epoch,
        validation_data=tiger_val.next_batch(),
        validation_steps=int(tiger_val.n / val_batch_size))
"""


def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--parameter_filename',
        type=str,
        help='Input parameter file name.',
        default='./parameters/parameters.json')

    return (parser.parse_args(argv))


def main(args):
    parameter_filename = args.parameter_filename

    with open(parameter_filename) as input_buffer:
        parameters = json.loads(input_buffer.read())

    application = SimpleOCR()
    application.train(parameters)


if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
