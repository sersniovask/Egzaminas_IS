import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import StratifiedKFold

from run_experiment import corrected_ci, make_outer_splits, metrics, perturbed_scores
from src.models import RBFNetwork, build_pipeline
from src.data import validate_record
from verify_results import manual_scores


def test_metrics_known_values():
    true = ["bus", "bus", "opel", "opel", "saab", "saab", "van", "van"]
    predicted = ["bus", "bus", "opel", "saab", "saab", "saab", "van", "van"]
    result = metrics(true, predicted)
    assert np.isclose(result["macro_f1"], (1 + 2/3 + 4/5 + 1) / 4)
    assert np.isclose(result["balanced_accuracy"], (1 + .5 + 1 + 1) / 4)
    independent_f1, independent_ba = manual_scores(true, predicted)
    assert np.isclose(independent_f1, (1 + 2/3 + 4/5 + 1) / 4)
    assert np.isclose(independent_ba, (1 + .5 + 1 + 1) / 4)


def test_outer_splits_do_not_overlap():
    X = np.arange(80).reshape(40, 2)
    y = np.repeat(["bus", "opel", "saab", "van"], 10)
    cfg = {"outer_folds": 5, "outer_seeds": [2026, 2027]}
    splits = list(make_outer_splits(X, y, cfg))
    assert len(splits) == 10
    for _, _, train, test in splits:
        assert not set(train) & set(test)
        assert set(train) | set(test) == set(range(40))


def test_pipeline_scaler_uses_training_only():
    X = pd.DataFrame({"a": [0., 2., 4., 100.], "b": [1., 3., 5., 100.]})
    y = ["bus", "opel", "bus", "opel"]
    pipeline = build_pipeline("centroid", 2026).fit(X.iloc[:3], y[:3])
    assert np.allclose(pipeline.named_steps["scaler"].mean_, [2., 3.])


def test_rbf_is_cloneable_and_predicts_labels():
    X = np.array([[0., 0.], [0., 1.], [5., 5.], [5., 6.]])
    y = np.array(["bus", "bus", "van", "van"])
    model = clone(RBFNetwork(n_centers=2)).fit(X, y)
    assert set(model.predict(X)) <= set(y)


def test_corrected_ci_is_finite():
    interval = corrected_ci([.02, .03, .01, .04], 84, 762)
    assert interval[0] < interval[1]
    assert all(np.isfinite(interval))


def test_unseen_record_schema():
    names = [f"feature_{i}" for i in range(18)]
    record = {name: i for i, name in enumerate(names)}
    record[names[3]] = None
    assert np.isnan(validate_record(record, names).iloc[0, 3])
    try:
        validate_record({"wrong": 1}, names)
    except ValueError:
        pass
    else:
        raise AssertionError("Neteisinga schema nebuvo atmesta")


def test_robustness_perturbations_are_identical_across_models():
    class Recorder:
        def __init__(self):
            self.inputs = []

        def predict(self, X):
            self.inputs.append(X.to_numpy().copy())
            return np.array(["bus", "opel", "saab", "van"])

    X = pd.DataFrame(np.arange(8).reshape(4, 2), columns=["a", "b"])
    y = ["bus", "opel", "saab", "van"]
    cfg = {"seed": 2026, "noise_sigmas": [.1], "missing_rates": [.05], "robustness_repeats": 2}
    first, second = Recorder(), Recorder()
    perturbed_scores(first, X, y, np.ones(2), cfg, 3, "svm")
    perturbed_scores(second, X, y, np.ones(2), cfg, 3, "mlp")
    assert len(first.inputs) == len(second.inputs) == 4
    for left, right in zip(first.inputs, second.inputs):
        assert np.array_equal(left, right, equal_nan=True)
    assert np.array_equal(X.to_numpy(), np.arange(8).reshape(4, 2))


def test_inner_search_audit_contains_all_candidates(tmp_path):
    from run_experiment import fit_model
    rng = np.random.default_rng(12)
    X = pd.DataFrame(rng.normal(size=(40, 3)))
    y = pd.Series(np.tile(["bus", "opel", "saab", "van"], 10))
    cfg = {"svm_C": [.1, 1], "svm_gamma": [.01], "inner_folds": 2}
    target = tmp_path / "search.csv"
    model, params = fit_model("svm", X, y, cfg, 2026, 1, target)
    audit = pd.read_csv(target)
    assert len(audit) == 2
    assert audit[["split0_test_score", "split1_test_score"]].notna().all().all()
    best = audit.loc[audit.rank_test_score.idxmin()]
    assert params["model__C"] == best.param_model__C
    assert len(model.predict(X)) == len(X)


def test_missing_test_feature_uses_training_median():
    X = pd.DataFrame({'a': [0., 2., 4., 6.], 'b': [1., 3., 5., 7.]})
    model = build_pipeline('centroid', 2026).fit(X, ['bus', 'bus', 'van', 'van'])
    test = pd.DataFrame({'a': [np.nan, 10000.], 'b': [2., 10000.]})
    imputer = model.named_steps['imputer']
    before = imputer.statistics_.copy()
    assert imputer.transform(test)[0, 0] == 3.
    model.predict(test)
    assert np.array_equal(before, imputer.statistics_)
