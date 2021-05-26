import argparse  # parse arguments via command line `python script.py -a 1 -b`
import numpy as np  # operate with arrays and matrices
import random
import sys  # interpreter objects
import time  # time manipulation
import uuid  # UIDs manipulation


# import LSL's Stream Info and Outlet classes, data and sampling rate types
from pylsl import StreamInfo, StreamOutlet, cf_float32


def add_arguments_get_values():
    """
    Add arguments to the command line and get the values passed.

    Returns:
        argparse.Namespace: Argument values passed.
    """
    # instanciate command line argument parser
    parser = argparse.ArgumentParser(prog=f"python {sys.argv[0]}")

    # add script arguments
    # documentation: https://docs.python.org/3.8/howto/argparse.html
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        default="EEGstream",
        help="LSL outlet stream name: EEGstream (default)",
    )
    parser.add_argument(
        "-c",
        "--channels",
        type=str,
        default=32,
        help="number of the EEG channels to simulate: 32 (default)",
    )
    parser.add_argument(
        "-sr",
        "--sampling_rate",
        type=str,
        default=1024,
        help="sampling rate (Hz) of the stream: 1024 (default)",
    )

    return parser.parse_args()


def send_sample(eeg_values):
    """
    Send a float array of simulated eeg values using the LSL stream created.

    Parameters:
        eeg_values (array): Trigger value to send (0.0 or 1.0).
    """
    # send sample, always as a list/array, even if only 1 value is sent
    outlet.push_sample(eeg_values)


if __name__ == "__main__":
    """Flow of the script."""

    # add command line arguments and get all values passed
    args = add_arguments_get_values()
    # store each argument values
    stream_name = args.name
    sampling_rate = int(args.sampling_rate)
    n_channels = int(args.channels)

    time_to_next_sample = 1 / sampling_rate

    # display parameters
    print("Setup")
    print("=====")
    print(f"Sampling rate: {sampling_rate}")
    print(f"Number of EEG channels: {n_channels}\n")
    print()

    # generate stream UID
    UID = str(uuid.uuid4())

    # instanciate StreamInfo - more info:
    # https://labstreaminglayer.readthedocs.io/projects/liblsl/ref/streaminfo.html
    info = StreamInfo(
        name=stream_name,  # name of the stream
        type="Markers",  # stream type
        channel_count=n_channels,  # number of values to stream
        nominal_srate=sampling_rate,  # sampling rate in Hz or IRREGULAR_RATE
        channel_format=cf_float32,  # data type sent (dobule, float, int, str)
        source_id=UID,  # unique identifier
    )

    # display LSL outlet stream information
    print("LSL stream")
    print("==========")
    print(f"ID: {UID}")
    print(f"Name: {stream_name}")
    print()

    # instanciate StreamOutlet - more info:
    # https://labstreaminglayer.readthedocs.io/projects/liblsl/ref/outlet.html
    outlet = StreamOutlet(info)
    print("LSL stream pushing samples...")

    try:
        print("Press Ctrl+C to finish the script")
        step = time_to_next_sample
        while True:
            sample = np.zeros(n_channels)
            for i, v in enumerate(sample):
                # amplitude = (i + random.random()) / random.randint(100, 200)
                amplitude = random.randint(-25, 25)
                freq = 12
                # print(amplitude)
                sample[i] = amplitude * np.sin(2 * np.pi * freq)

            send_sample(sample)
            time.sleep(time_to_next_sample)
            step += time_to_next_sample
    except KeyboardInterrupt:
        print()
        print("Script finished.")
