#!/usr/bin/env python3
from time import sleep
import click
import csv
from contextlib import contextmanager


def get_core_cpufreq_info(core_id: int, property_name: str) -> str:
    with open(f"/sys/devices/system/cpu/cpu{core_id}/cpufreq/{property_name}") as property_file:
        return property_file.read()


def get_thermal_info(zone_id: int, property_name: str) -> str:
    with open(f"/sys/class/thermal/thermal_zone{zone_id}/{property_name}") as property_file:
        return property_file.read()


@contextmanager
def open_logfile(logfile):
    if logfile == '-':
        import sys
        yield sys.stdout
    else:
        with open(logfile, 'w', newline='') as logfile_fd:
            yield logfile_fd


@click.command()
@click.option("--logfile", default="cpu_info.csv", type=click.Path(allow_dash=True, dir_okay=False, exists=False), help="Log filename")
@click.option("--delay", default=1.0, type=float, help="Delay (in seconds) between readings")
@click.option("--core-count", default=8, type=int, help="Number of cores to monitor frequency")
@click.option("--thermal-zone-count", default=4, type=int, help="Number of thermal zones for temperature monitoring")
@click.option("--verbose/--no-verbose", default=False, help="Enable verbose output")
def main(logfile: str, delay: float, core_count: int, thermal_zone_count: int, verbose: bool):
    core_names = [f"core_{i}" for i in range(core_count)]
    zone_names = [f"thermal_zone_{i}" for i in range(thermal_zone_count)]
    csv_field_names = core_names + zone_names


    with open_logfile(logfile) as csv_file:
        if verbose:
            print("Writing CSV header")
        writer = csv.DictWriter(csv_file, fieldnames=csv_field_names)
        writer.writeheader()

    while True:
        cpu_data = {}
        for core_id in range(8):
            scaling_cur_freq = int(get_core_cpufreq_info(core_id, "scaling_cur_freq"))
            scaling_cur_freq /= 1000.0
            cpu_data[f"core_{core_id}"] = scaling_cur_freq
            if verbose:
                print(f"Core {core_id}: {scaling_cur_freq} GHz")

        for zone_id in range(4):
            temp = int(get_thermal_info(zone_id, "temp"))
            temp /= 1000.0
            cpu_data[f"thermal_zone_{zone_id}"] = temp
            if verbose:
                print(f"Zone {zone_id}: {temp}*C")

        with open_logfile(logfile) as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_field_names)
            writer.writerow(cpu_data)
        if verbose:
            print()
        sleep(delay)


if __name__ == "__main__":
    main()
