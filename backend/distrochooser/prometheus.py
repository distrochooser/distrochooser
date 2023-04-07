from prometheus_client import Gauge, Counter, CollectorRegistry
from .models import Distribution

registry = CollectorRegistry()
all_tests_gauge: Gauge = Gauge(
    name="all_test_count",
    documentation="Total number of tests opened on Distrochooser.de",
    registry=registry
)
answered_tests_v5_gauge: Gauge = Gauge(
    name="answered_tests_v5",
    documentation="Total number tests done by Distrochooser.de (this version)",
    registry=registry
)
empty_tests_v5_gauge: Gauge = Gauge(
    name="empty_tests_v5",
    documentation="Number of tests unanswered on Distrochooser.de (this version)",
    registry=registry
)
answered_tests_v_previous_gauge: Gauge = Gauge(
    name="answered_tests_v_previous",
    documentation="Total number tests done by Distrochooser.de (previous versions)",
    registry=registry
)
average_test_calculation_time: Gauge = Gauge(
    name="average_test_calculation_time",
    documentation="Average time needed for backend to process a test to a result",
    registry=registry
)

median_test_calculation_time: Gauge = Gauge(
    name="median_test_calculation_time",
    documentation="Median time needed for backend to process a test to a result",
    registry=registry
)
average_test_stay_time: Gauge = Gauge(
    name="average_test_stay_time",
    documentation="Average stay time from open to last result calculation",
    registry=registry
)

median_test_stay_time: Gauge = Gauge(
    name="median_test_stay_time",
    documentation="Median stay time from open to last result calculation",
    registry=registry
)

stdev_test_calculation_time: Gauge = Gauge(
    name="stdev_test_calculation_time",
    documentation="Standard deviation for the time needed for backend to process a test to a result",
    registry=registry
)

positive_ratings_gauge: Gauge = Gauge(
    name="positive_ratings",
    documentation="Positive ratings",
    registry=registry
)

negative_ratings_gauge: Gauge = Gauge(
    name="negative_ratings",
    documentation="Negative ratings",
    registry=registry
)


distro_gauges = {}
distros = Distribution.objects.all()
distro: Distribution
for distro in distros:
    distro_gauges[distro.identifier] = {}

    metrics = ["ratings", "positive_ratings", "percentage", "rank", "clicks"]
    for metric in metrics:
        new_metric = Gauge(
            name=f"distribution_{metric}_{distro.identifier}",
            documentation=f"{metric} for distribution {distro.name}",
            registry=registry
        )
        distro_gauges[distro.identifier][metric] = new_metric
