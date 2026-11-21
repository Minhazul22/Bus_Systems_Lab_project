#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 11:37:14 2026

@author: rasmus

Read a defined number of ADC samples from an Arduino,
save measurements to CSV, generate histograms, and calculate
statistical indicators for inputs A0 and A1.
"""

import serial
import time
import csv
import statistics
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

# --------------------------------------------------
# Configuration
# --------------------------------------------------

COM_PORT = '/dev/cu.usbserial-1460'
BAUD_RATE = 115200

NUM_SAMPLES = 1000
CSV_FILENAME = 'ads_measurements.csv'
SERIAL_TIMEOUT = 2

NUM_BINS = 30


# --------------------------------------------------
# Statistical analysis
# --------------------------------------------------

def calculate_statistics(data):
    """Calculate descriptive statistics for one ADC channel."""

    if not data:
        return None

    return {
        'N': len(data),
        'Mean_ADC': statistics.mean(data),
        'Median_ADC': statistics.median(data),
        'StdDev_ADC': (
            statistics.stdev(data) if len(data) >= 2 else 0.0
        ),
        'Min_ADC': min(data),
        'Max_ADC': max(data),
        'PeakToPeak_ADC': max(data) - min(data)
    }


def save_statistics(a0_data, a1_data, csv_filename):
    """Calculate and save statistics for both ADC inputs."""

    output_dir = Path(csv_filename).parent
    filename_stem = Path(csv_filename).stem
    output_file = output_dir / f'{filename_stem}_statistics.csv'

    channels = {
        'A0': a0_data,
        'A1': a1_data
    }

    with open(
        output_file, 'a', newline='', encoding='utf-8'
    ) as csvfile:

        fieldnames = [
            'Input',
            'N',
            'Mean_ADC',
            'Median_ADC',
            'StdDev_ADC',
            'Min_ADC',
            'Max_ADC',
            'PeakToPeak_ADC'
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for channel, data in channels.items():
            result = calculate_statistics(data)

            if result is None:
                continue

            row = {'Input': channel, **result}
            writer.writerow(row)

            print(f'\nStatistics for {channel}:')
            print(f"  Samples:              {result['N']}")
            print(f"  Mean:                 {result['Mean_ADC']:.3f} ADC")
            print(f"  Median:               {result['Median_ADC']:.3f} ADC")
            print(f"  Standard deviation:   {result['StdDev_ADC']:.3f} ADC")
            print(f"  Minimum:              {result['Min_ADC']} ADC")
            print(f"  Maximum:              {result['Max_ADC']} ADC")
            print(f"  Peak-to-peak:         {result['PeakToPeak_ADC']} ADC")

    print(f'\nStatistics saved to: {output_file}')


# --------------------------------------------------
# Histogram generation
# --------------------------------------------------

def generate_histograms(a0_data, a1_data, csv_filename):
    """Generate and save one histogram for each ADC input."""

    output_dir = Path(csv_filename).parent
    filename_stem = Path(csv_filename).stem

    channels = [
        ('A0', a0_data),
        ('A1', a1_data)
    ]

    for channel, data in channels:
        if not data:
            continue

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.hist(
            data,
            bins=NUM_BINS,
            edgecolor='black',
            alpha=0.75
        )

        result = calculate_statistics(data)

        ax.set_title(
            f'{channel} ADC Histogram (n={len(data)})'
        )
        ax.set_xlabel('ADC value [counts]')
        ax.set_ylabel('Frequency [samples]')

        # Display the mean and standard deviation
        ax.axvline(
            result['Mean_ADC'],
            linestyle='--',
            linewidth=2,
            label=f"Mean = {result['Mean_ADC']:.2f}"
        )

        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        fig.tight_layout()

        output_file = (
            output_dir /
            f'{filename_stem}_{channel}_histogram.png'
        )

        fig.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f'Histogram saved: {output_file}')

        plt.show()
        plt.close(fig)


# --------------------------------------------------
# Data acquisition
# --------------------------------------------------

def main():
    ser = None
    a0_data = []
    a1_data = []
    samples_collected = 0

    try:
        ser = serial.Serial(
            COM_PORT,
            BAUD_RATE,
            timeout=SERIAL_TIMEOUT
        )

        # Allow Arduino to reset
        time.sleep(2)
        ser.reset_input_buffer()

        print(f'Connected to {COM_PORT}')
        print(f'Collecting {NUM_SAMPLES} valid samples...')

        output_path = Path(CSV_FILENAME)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(
            output_path,
            'w',
            newline='',
            encoding='utf-8'
        ) as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow([
                'Sample',
                'Timestamp',
                'Elapsed_s',
                'A0_ADC',
                'A1_ADC'
            ])

            start_time = time.perf_counter()

            while samples_collected < NUM_SAMPLES:

                line = ser.readline().decode(
                    'utf-8',
                    errors='replace'
                ).strip()

                if not line:
                    continue

                values = line.split(',')

                if len(values) != 2:
                    continue

                try:
                    a0_val = int(values[0])
                    a1_val = int(values[1])
                except ValueError:
                    continue

                elapsed = time.perf_counter() - start_time
                timestamp = datetime.now().isoformat(
                    timespec='milliseconds'
                )

                samples_collected += 1
                a0_data.append(a0_val)
                a1_data.append(a1_val)

                writer.writerow([
                    samples_collected,
                    timestamp,
                    f'{elapsed:.6f}',
                    a0_val,
                    a1_val
                ])

                # Flush so collected samples survive interruption
                csvfile.flush()

                print(
                    f'{samples_collected:5d}/{NUM_SAMPLES} | '
                    f'A0: {a0_val:4d} | '
                    f'A1: {a1_val:4d} | '
                    f't: {elapsed:.3f} s'
                )

        print(f'\nMeasurement complete: {samples_collected} samples')
        print(f'Measurements saved to: {CSV_FILENAME}')

    except serial.SerialException as e:
        print(f'Serial error: {e}')

    except KeyboardInterrupt:
        print('\nMeasurement interrupted by user.')

    except OSError as e:
        print(f'File error: {e}')

    finally:
        if ser is not None and ser.is_open:
            ser.close()
            print('Serial port closed.')

    # Analyze all samples collected, including partial measurements
    if samples_collected > 0:
        save_statistics(a0_data, a1_data, CSV_FILENAME)
        generate_histograms(a0_data, a1_data, CSV_FILENAME)


if __name__ == '__main__':
    main()