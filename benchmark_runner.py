
from __future__ import print_function
import argparse
import os

import logging
logging.basicConfig(level=logging.INFO)
from utils import metrics_manager
from utils import data_manager
try:
    import ConfigParser
    config = ConfigParser.ConfigParser()
except ImportError:
    import configparser
    config = configparser.ConfigParser()



# --metrics-policy metrics_paramaters_images --task-name custom.p316xlarge.fp32.bs32 --metrics-suffix nightly --num-gpus 8 --command-to-execute \"Hello world\"
CONFIG_TEMPLATE = './task_config_template.cfg'
CONFIG_DIR = './task_config.cfg'



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run a benchmark task.")
    parser.add_argument('--framework', type=str, help='Framework eg. mxnet')
    parser.add_argument('--metrics-policy', type=str, help='Metrics policy section name e.g. metrics_paramaters_images')
    parser.add_argument('--task-name', type=str, help='Task Name e.g. resnet50_cifar10_symbolic.')
    parser.add_argument('--metrics-suffix', type=str, help='Metrics suffix e.g. --metrics-suffix daily')
    parser.add_argument('--num-gpus', type=int, help='Numbers of gpus. e.g. --num-gpus 8')
    parser.add_argument('--command-to-execute', type=str, help='The script command that performs benchmarking')
    parser.add_argument('--data-set', type=str, help='The data set to use for benchmarking, eg. imagenet')
    
    args = parser.parse_args()    

   
    if(args.data_set == 'imagenet'): 
        data_manager.getImagenetData()
     

    config.read(CONFIG_TEMPLATE)

    for name, value in config.items(args.metrics_policy):
        if(name == 'patterns'):
            metric_patterns = value
        elif(name == 'metrics'):
            metric_names= value
        else:
            metric_compute_methods = value
        
    

    metrics_manager.benchmark(
        command_to_execute=args.command_to_execute,
        metric_patterns=metric_patterns,
        metric_names=metric_names,
        metric_compute_methods=metric_compute_methods,
        num_gpus=args.num_gpus,
        task_name=args.task_name,
        suffix=args.metrics_suffix,
        framework=args.framework
    )

    # clean up
    os.remove(CONFIG_DIR)
