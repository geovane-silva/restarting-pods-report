""""
    This scripts creates a report of restarting pods and general pods
    states on a Kubernetes cluster.

    It uses the kubernetes Python client to list the pods, authenticating
    using the present kube context.

    Arguments
    ---------
        namespace             : report namespace
        -p , --period         : period of time (in days) of the report
        -e, --export          : exports result to a .csv file
        -i, --ignore-warnings : ignores warnings
        -r, --remove-headers  : removes header and remaining information printing the report only
        -q, --quiet           : enters quiet mode
        -h, --help            : prints help message
"""
import argparse
from datetime import datetime, timedelta, date
import sys
import csv
import urllib3
import timeago
from pytz import timezone
from pods_list import PodsList

urllib3.disable_warnings()

class Report:
    """
        A class used to generates restarting pods reports

        ...

        Attributes
        ----------
        namespace : str
            The report namespace. If not set, generates a report for all anmespaces
        period : int
            The period of time (in days) of the report. If not set, generates a
            report for the previous 2 days
        ignore_warnings : bool
            Ignore or print warinings. Defauult is False.
        headerless : bool
            Removes headeers and remaining informations printing the report only.
        restarting_containers_report: dict
            The gemerated restarting pods report.

        Methods
        -------
        list_pods()
            Returns the pods list on the specified namespace. If not set, list pods for
            all namespaces
        format_date(finished_at)
            Formats and returns a container finished_at date to a standard time format.
        get_restarting_containers_report()
            Builds and returns the report based on the specified namespace and period.
        print_restarting_containers_report()
            Prints the generated report.
        export_restarting_containers_report()
            Exports report to a  .csv file
    """

    def __init__(self, namespace=False, period=2, ignore_warnings=False,
                 headerless=False, pods_list=[]):
        """
            Parameters
            ----------
            namespace : str
                The report namespace. If not set, generates a report for all anmespaces
            period: int
                The period of time (in days) of the report. If not set, generates a
                report for the previous 2 days
            ignore_warnings : bool
                Ignore or print warinings. Defauult is False.
            headerless : bool
                Removes headeers and remaining informations printing the report only.
            restarting_containers_report: dict
                The gemerated restarting pods report.
        """
        self.namespace = namespace
        self.period = period
        self.ignore_warnings = ignore_warnings
        self.headerless = headerless
        self.pods_list = pods_list
        self.restarting_containers_report = self.get_restarting_containers_report()

    def format_date(self, finished_at):
        """
            Formats and returns a container finished_at date to a standard time format.
        """
        time_format = '%Y/%m/%d, %H:%M:%S'
        formatted_date = finished_at.strftime(time_format)
        return formatted_date

    def get_restarting_containers_report(self):
        """
            Builds and returns the report based on the specified namespace and period.
        """
        if self.headerless:
            print('Listing pods with restarting containers on',
                    f'namespace {self.namespace}' if self.namespace\
                    else 'all namespaces')
            print(f'Report duration: {self.period} {"days" if self.period != 1 else "day"}.\n')
        restarting_containers = []
        not_running_containers = []
        warnings = []
        pods_list = self.pods_list.get()
        if len(pods_list.items) > 0:
            for pod in pods_list.items:
                if pod.status.phase.lower() == 'running':
                    for container in pod.status.container_statuses:
                        if container.restart_count > 0:
                            container_obj = dict(
                                pod = pod.metadata.name,
                                namespace = pod.metadata.namespace,
                                name = container.name,
                                restart_count = container.restart_count,
                                ready = container.ready
                            )
                            working_date = container.last_state.terminated.finished_at \
                                           if container.last_state.terminated \
                                           else container.state.running.started_at
                            container_time = working_date.astimezone(timezone("America/Sao_Paulo"))
                            terminated_date = datetime.date(container_time)
                            terminated_time = datetime.time(container_time)
                            container_obj['terminated_at'] = datetime.combine(terminated_date,
                                                                              terminated_time) \
                                                                              .replace(tzinfo=None)
                            if container.last_state.terminated:
                                container_obj['reason'] = container.last_state.terminated.reason
                            else:
                                container_obj['reason'] = 'N/A'

                            if not container.ready:
                                not_running_containers.append(container.name)
                            restarting_containers.append(container_obj)
                elif pod.status.phase.lower() != 'succeeded':
                    warnings.append(dict(
                                          name=pod.metadata.name,
                                          state=pod.status.phase
                                        ))
            restarting_containers_report = dict(
                                                restarting_containers = restarting_containers,
                                                not_running_containers = not_running_containers,
                                                warnings = warnings
                                            )
            return restarting_containers_report
        return []

    def print_restarting_containers_report(self):
        """
            Prints the generated report.
        """
        if self.headerless:
            header = f'{"POD":<60}\t{"CONTAINER":<35}\t{"NAMESPACE":<35}\t{"RESTARTS":<10}'
            header +=  f'\t{"READY":<5}\t{"LAST TERMINATION":<20}'

            print(header)

        for container in self.restarting_containers_report['restarting_containers']:
            today = date.today()
            begin_period = today - timedelta(days=self.period)
            if datetime.date(container['terminated_at']) > begin_period:
                line = ''
                line += f'{container["pod"].strip():<60}\t{container["name"]:<35}'
                ready = 'True' if container['ready'] else '\033[91mFalse\033[0m'

                if container['terminated_at'] != 'N/A':
                    time_string = self.format_date(container['terminated_at']) \
                                         if container['terminated_at'] != 'N/A' \
                                         else container['terminated_at']
                    terminated_at = timeago.format(container['terminated_at'],
                                                   datetime.now().replace(tzinfo=None))
                    time_string += f" [{terminated_at}]"

                line += f'\t{container["namespace"]:<35}\t{container["restart_count"]:<10}'
                line += f'\t{ready:<5}\t{time_string:<20}'
                print(line)

        if self.headerless:
            if not self.ignore_warnings:
                print('\n')
                for pod in self.restarting_containers_report['warnings']:
                    print(f'[WARNING] Pod {pod["name"]} state is {pod["state"]}')

            not_running_count = len(self.restarting_containers_report['not_running_containers'])

            print(f'\nFound {not_running_count}',
                f'{"containers" if not_running_count != 1 else "container"}',
                'not running\n')

    def export_restarting_containers_report(self):
        """
            Exports report to a  .csv file
        """
        csv_name = f'{datetime.now().strftime("%Y_%m_%d")}_restarting_pods_report.csv'
        print(f'Exporting {csv_name}')
        try:
            with open(csv_name, mode='w') as exported_report:
                report_writer = csv.writer(exported_report, \
                                        delimiter=',',
                                        quotechar='"',
                                        quoting=csv.QUOTE_MINIMAL)
                report_writer.writerow(['Pod', 'Container',
                                        'Namespace', 'Restart Count',
                                        'Terminated At', 'Reason'])
                for container_obj in self.restarting_containers_report['restarting_containers']:
                    report_writer.writerow([container_obj['pod'],
                                            container_obj['name'],
                                            container_obj['namespace'],
                                            container_obj['restart_count'],
                                            container_obj['terminated_at'],
                                            container_obj['reason']])
        except Exception as e:
            print('Failed to export report')
            print(e)

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(prog='restpods',
                                        usage='restpods [namespace] [-p]   ',
                                        description='Returns the list of pods\
                                                    with restarting containers.')
        parser.add_argument('namespace', action='store', nargs='?', default=False)
        parser.add_argument('-e',
                            '--export',
                            help='Exports result to a .csv file.',
                            action='store_true')
        parser.add_argument('-i',
                            '--ignore-warnings',
                            help='Ignores warnings.',
                            action='store_true',
                            required=False)
        parser.add_argument('-r',
                            '--remove-headers',
                            help='Removes header and remaining information \
                                printing the report only.',
                            action='store_false',
                            required=False)
        parser.add_argument('-p',
                            '--period',
                            help='Period (in days) that user wants to see the report.\
                                Default is 2 days',
                            action='store',
                            default=2,
                            type=int,
                            required=False)
        parser.add_argument('-q',
                            '--quiet',
                            help='Enter quiet mode, printing no result',
                            action='store_true',
                            required=False)

        args = parser.parse_args()

        pods_list = PodsList(auth_method='local', namespace=args.namespace)
        report = Report(args.namespace, args.period, args.ignore_warnings,
                        args.remove_headers, pods_list)

        if not args.quiet:
            report.print_restarting_containers_report()
        if args.export:
            report.export_restarting_containers_report()
    except KeyboardInterrupt:
        print('\nExecution aborted.')
        sys.exit(2)
