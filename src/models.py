"""Du atskaitos ir trys intelektualieji klasifikavimo metodai."""
from __future__ import annotations

import numpy as np
from scipy.spatial.distance import pdist
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics.pairwise import rbf_kernel
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


class RBFNetwork(ClassifierMixin, BaseEstimator):
    """KMeans centrai -> Gauso RBF aktyvacijos -> Ridge išvesties sluoksnis."""

    def __init__(self, n_centers=16, width=1.0, alpha=0.01, random_state=2026):
        self.n_centers = n_centers
        self.width = width
        self.alpha = alpha
        self.random_state = random_state

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        self.classes_, encoded = np.unique(y, return_inverse=True)
        self.centers_ = KMeans(n_clusters=self.n_centers, random_state=self.random_state, n_init=10).fit(X).cluster_centers_
        squared = pdist(self.centers_, metric="sqeuclidean")
        median_sq = float(np.median(squared[squared > 0])) if np.any(squared > 0) else 1.0
        # phi_j(x)=exp(-gamma ||x-c_j||²), gamma=1/(2 * (width * sqrt(median_sq))²).
        self.gamma_ = 1.0 / (2.0 * self.width**2 * median_sq)
        activations = rbf_kernel(X, self.centers_, gamma=self.gamma_)
        targets = np.eye(len(self.classes_))[encoded]
        self.output_ = Ridge(alpha=self.alpha).fit(activations, targets)
        return self

    def decision_function(self, X):
        return self.output_.predict(rbf_kernel(np.asarray(X, dtype=float), self.centers_, gamma=self.gamma_))

    def predict(self, X):
        return self.classes_[np.argmax(self.decision_function(X), axis=1)]


class EncodedMLP(ClassifierMixin, BaseEstimator):
    """MLP su skaitinėmis vidinės validacijos žymomis ir tekstine išvestimi."""

    def __init__(self, hidden_layer_sizes=(32,), alpha=0.001, learning_rate_init=0.001,
                 random_state=2026):
        self.hidden_layer_sizes = hidden_layer_sizes
        self.alpha = alpha
        self.learning_rate_init = learning_rate_init
        self.random_state = random_state

    def fit(self, X, y):
        self.classes_, encoded = np.unique(y, return_inverse=True)
        self.network_ = MLPClassifier(hidden_layer_sizes=self.hidden_layer_sizes,
                                      alpha=self.alpha, learning_rate_init=self.learning_rate_init,
                                      activation="relu", solver="adam", early_stopping=True,
                                      max_iter=2000, random_state=self.random_state)
        self.network_.fit(X, encoded)
        return self

    def predict(self, X):
        return self.classes_[self.network_.predict(X)]


def build_pipeline(name: str, seed: int, *, scaled=True):
    if name == "centroid":
        model = NearestCentroid(metric="euclidean", shrink_threshold=None)
    elif name == "knn":
        model = KNeighborsClassifier(n_neighbors=5, metric="euclidean", weights="uniform")
    elif name == "svm":
        # SVC naudoja minkšto tarpo optimizavimą ir exp(-gamma ||z-z'||²) branduolį.
        # OVO balsų lygybę sprendžia bibliotekos predict; balai nėra tikimybės.
        model = SVC(kernel="rbf", decision_function_shape="ovo", random_state=seed)
    elif name == "svm_linear":
        model = SVC(kernel="linear", decision_function_shape="ovo", random_state=seed)
    elif name == "mlp":
        model = EncodedMLP(random_state=seed)
    elif name == "rbf":
        model = RBFNetwork(random_state=seed)
    else:
        raise ValueError(name)
    # Imputer ir scaler išmoksta parametrus tik fit gautoje mokymo dalyje.
    return Pipeline([("imputer", SimpleImputer(strategy="median")),
                     ("scaler", StandardScaler() if scaled else "passthrough"),
                     ("model", model)])


def grid_for(name, cfg):
    if name == "svm":
        return {"model__C": cfg["svm_C"], "model__gamma": cfg["svm_gamma"]}
    if name == "svm_linear":
        return {"model__C": cfg["svm_C"]}
    if name == "mlp":
        return {"model__hidden_layer_sizes": [tuple(v) if isinstance(v, list) else (v,) for v in cfg["mlp_hidden"]],
                "model__alpha": cfg["mlp_alpha"], "model__learning_rate_init": cfg["mlp_learning_rate"]}
    if name == "rbf":
        return {"model__n_centers": cfg["rbf_centers"], "model__width": cfg["rbf_width"],
                "model__alpha": cfg["rbf_alpha"]}
    return None
