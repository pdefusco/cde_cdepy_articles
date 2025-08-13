import os
import argparse
from urllib.parse import urlparse
from cdepy import cdeconnection, cdemanager, utils


class CDELogFetcher:
    def __init__(self, api_url, user, password):
        self.api_url = api_url
        self.user = user
        self.password = password
        self.connection = None
        self.cluster_manager = None

    def connect(self):
        self.connection = cdeconnection.CdeConnection(self.api_url, self.user, self.password)
        self.connection.setToken()
        self.cluster_manager = cdemanager.CdeClusterManager(self.connection)

    def list_job_runs(self, job_type="spark"):
        return self.cluster_manager.listJobRuns(job_type)

    def show_log_types(self, job_run_id):
        return self.cluster_manager.showAvailableLogTypes(job_run_id)

    def download_and_parse_logs(self, job_run_id, log_type):
        raw_logs = self.cluster_manager.downloadJobRunLogs(job_run_id, log_type)
        return utils.sparkEventLogParser(raw_logs)


def get_hostname_from_url(url):
    parsed = urlparse(url)
    return parsed.hostname.replace('.', '_')


def write_logs_to_file(job_id, log_type, hostname, log_data):
    safe_log_type = log_type.replace('/', '-')
    output_dir = os.path.join("logs", hostname, job_id, safe_log_type)
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, f"{hostname}.log")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(log_data)
    print(f"[✓] Saved log: {file_path}")


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch Spark job logs from multiple CDE clusters.")
    parser.add_argument("--user", required=True, help="CDE workload user")
    parser.add_argument("--password", required=True, help="CDE workload password")
    parser.add_argument("--api-urls", required=True, nargs="+", help="List of CDE API URLs")
    parser.add_argument("--log-type", help="Optional specific log type to fetch (e.g., driver/stdout)")
    return parser.parse_args()


def main():
    args = parse_args()

    for api_url in args.api_urls:
        hostname = get_hostname_from_url(api_url)
        print(f"\n=== Connecting to cluster: {api_url} ({hostname}) ===")

        try:
            fetcher = CDELogFetcher(api_url, args.user, args.password)
            fetcher.connect()

            job_runs = fetcher.list_job_runs()

            if not job_runs:
                print(f"[!] No job runs found on {hostname}")
                continue

            for job in job_runs:
                job_id = str(job.get("id") or job.get("jobRunId"))
                if not job_id:
                    print(f"[!] Skipping job run with missing ID on {hostname}")
                    continue

                print(f"\n→ Processing job run ID: {job_id}")

                try:
                    # If a specific log type is specified, just fetch that
                    if args.log_type:
                        print(f"  → Fetching specific log type: {args.log_type}")
                        try:
                            parsed_logs = fetcher.download_and_parse_logs(job_id, args.log_type)
                            write_logs_to_file(job_id, args.log_type, hostname, parsed_logs)
                        except Exception as log_err:
                            print(f"    [!] Failed to fetch {args.log_type} for job run {job_id}: {log_err}")
                    else:
                        # Otherwise fetch all available log types
                        available_log_types = fetcher.show_log_types(job_id)
                        if not available_log_types:
                            print(f"[!] No log types found for job run {job_id}")
                            continue

                        for log_info in available_log_types:
                            log_type = log_info.get("type")
                            if not log_type:
                                continue

                            print(f"  → Fetching log type: {log_type}")
                            try:
                                parsed_logs = fetcher.download_and_parse_logs(job_id, log_type)
                                write_logs_to_file(job_id, log_type, hostname, parsed_logs)
                            except Exception as log_err:
                                print(f"    [!] Failed to fetch {log_type} for job run {job_id}: {log_err}")

                except Exception as job_err:
                    print(f"[!] Failed to process job run {job_id} on {hostname}: {job_err}")

        except Exception as e:
            print(f"[!] Error processing cluster {api_url}: {e}")


if __name__ == "__main__":
    main()
