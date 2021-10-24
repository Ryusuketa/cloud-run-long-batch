import gokart
import luigi
import os
import time


class RunTaskWithWait(gokart.TaskOnKart):
    workspace_directory = '' 
    wait_time: int = luigi.IntParameter()
    output_name: str = luigi.Parameter()
    rerun = True

    def output(self):
        return self.make_target(f'gs://{os.environ["GCS_BUCKET_NAME"]}/{self.output_name}.txt', use_unique_id=False)

    def run(self):
        print(f'Task {self.output_name} start.')
        time.sleep(self.wait_time)
        self.dump(f'{self.output_name} is done')
        print(f'Task {self.output_name} end.')


class Agg(gokart.TaskOnKart):
    workspace_directory = '' 
    rerun = True

    def output(self):
        return self.make_target(f'gs://{os.environ["GCS_BUCKET_NAME"]}/all_results.txt', use_unique_id=False)

    def requires(self):
        return [RunTaskWithWait(wait_time=wt, output_name=fname) for wt, fname in [(10, 'a'), (10, 'b'), (30, 'c'), (30, 'd')]]
 
    def run(self):
        res = self.load()
        self.dump(str(res))



def run_pipeline():
    gokart.build(Agg())


if __name__ == '__main__':
    run_pipeline()