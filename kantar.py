import argparse
import csv
import datetime


parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()


def convert_dates_to_datetimes(sessions):
    for session in sessions:
        session['Starttime'] = datetime.datetime.strptime(
            session['Starttime'], '%Y%m%d%H%M%S')
    return sessions


def get_endtime(start_time):
    return start_time - datetime.timedelta(seconds=1)


def get_duration(end_time, start_time):
    diff = end_time - start_time
    return int(diff.total_seconds() + 1)


def get_end_of_day(start_time):
    return datetime.datetime(
        year=start_time.year,
        month=start_time.month,
        day=start_time.day,
        hour=23,
        minute=59,
        second=59)


def sort_sessions(sessions):
    return sorted(
        sessions, key=lambda k: (k['HomeNo'], k['Starttime'])
    )


def process_data(sessions):
    results = []
    for i, j in enumerate(sessions):
        output = {}
        output['HomeNo'] = j['HomeNo']
        output['Channel'] = j['Channel']
        output['Starttime'] = j['Starttime']
        output['Activity'] = j['Activity']
        try:
            if sessions[i+1]['HomeNo'] == j['HomeNo']:
                output['EndTime'] = get_endtime(sessions[i+1]['Starttime'])
            else:
                raise IndexError
        except IndexError:
            output['EndTime'] = get_end_of_day(j['Starttime'])

        output['Duration'] = get_duration(
            output['EndTime'], output['Starttime'])
        results.append(output)

    return results


def get_data_from_file():
    data = []
    with open(args.filename, 'r') as file:
        reader = csv.DictReader(file, delimiter='|')
        for row in reader:
            data.append(row)

    return data


def save_results_to_a_file(results):
    with open('sessions.psv', 'w') as file:
        writer = csv.DictWriter(
            file, fieldnames=list(results[0].keys()), delimiter='|')
        writer.writeheader()
        for session in results:
            writer.writerow(session)


def process():
    data = get_data_from_file()
    converted_data = convert_dates_to_datetimes(data)
    sorted_data = sort_sessions(converted_data)
    results = process_data(sorted_data)
    save_results_to_a_file(results)


if __name__ == "__main__":
    process()
