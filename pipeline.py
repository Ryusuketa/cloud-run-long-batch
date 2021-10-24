import gokart
import luigi
import os
import time


class RunTaskWithWait(gokart.TaskOnKart):
    workspace_directory = '' 
    wait_time: int = luigi.IntParameter()
    output_name: str = luigi.Parameter()

    def output(self):
        return self.make_target(f'gs://{os.environ["GCS_BUCKET_NAME"]}/{self.output_name}.txt', use_unique_id=False)

    def run(self):
        print(f'Task {self.output_name} start.')
        time.sleep(self.wait_time)
        self.dump(f'{self.output_name} is done')
        print(f'Task {self.output_name} end.')


class Agg(gokart.TaskOnKart):
    workspace_directory = '' 

    def output(self):
        return self.make_target(f'gs://{os.environ["GCS_BUCKET_NAME"]}/all_results.txt', use_unique_id=False)

    def requires(self):
        return [RunTaskWithWait(wait_time=100, output_name=f'{i}') for i in range(27)]
 
    def run(self):
        res = self.load()
        self.dump(str(res))


def run_pipeline():
    gokart.build(Agg())


if __name__ == '__main__':
    run_pipeline()