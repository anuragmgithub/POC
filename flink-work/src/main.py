import argparse
from jobs import streaming_job, batch_job

def main():
    parser = argparse.ArgumentParser(description="Run PyFlink jobs.")
    parser.add_argument('--job', choices=['streaming', 'batch'], required=True,
                        help='Select the job to run: streaming or batch')
    args = parser.parse_args()

    if args.job == 'streaming':
        streaming_job.run()
    elif args.job == 'batch':
        batch_job.run()
    else:
        print("Unknown job type.")

if __name__ == '__main__':
    main()
