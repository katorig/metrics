import argparse
from metrics.segmentation.health_monitoring import SegmentationHealthMonitoring
from metrics.segmentation.segm_models_metrics import SegmentationMetrics


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('model_id', metavar='model_id', type=int, help='Please type model_id')
    parser.add_argument('report_date', metavar='report_date', type=str,
                        help="Please type report_date in 'YYYY-MM-DD' format")
    args = parser.parse_args()
    return args.model_id, args.report_date


if __name__ == '__main__':
    model_id, report_date = parse_argument()
    # model_id = 135
    # report_date = '2021-05-28'
    # mon = SegmentationHealthMonitoring(model_id, report_date)
    # mon.set_monitoring_time_machine()
    metrics = SegmentationMetrics(model_id, report_date)
    metrics.check_number_of_rows()
