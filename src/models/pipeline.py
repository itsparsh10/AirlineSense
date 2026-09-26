from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.features.feature_engineering import AirlineFeatureEngineer


def build_preprocessor(scale_numeric: bool) -> ColumnTransformer:
    numeric_steps = [("imputer", SimpleImputer(strategy="median"))]
    if scale_numeric:
        numeric_steps.append(("scaler", StandardScaler()))

    numeric_pipeline = Pipeline(numeric_steps)
    categorical_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        [
            (
                "numeric",
                numeric_pipeline,
                make_column_selector(dtype_include="number"),
            ),
            (
                "categorical",
                categorical_pipeline,
                make_column_selector(dtype_exclude="number"),
            ),
        ]
    )


def build_logistic_pipeline(max_iter: int, engineered: bool = False) -> Pipeline:
    return Pipeline(
        [
            ("features", AirlineFeatureEngineer(enabled=engineered)),
            ("preprocessor", build_preprocessor(scale_numeric=True)),
            (
                "model",
                LogisticRegression(max_iter=max_iter, class_weight="balanced"),
            ),
        ]
    )


def build_random_forest_pipeline(
    n_estimators: int,
    max_depth: int,
    min_samples_leaf: int,
    random_state: int,
    engineered: bool,
) -> Pipeline:
    return Pipeline(
        [
            ("features", AirlineFeatureEngineer(enabled=engineered)),
            ("preprocessor", build_preprocessor(scale_numeric=False)),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=n_estimators,
                    max_depth=max_depth,
                    min_samples_leaf=min_samples_leaf,
                    class_weight="balanced_subsample",
                    random_state=random_state,
                    n_jobs=-1,
                ),
            ),
        ]
    )

