"""Validates every anomalies/<id>/anomaly.yaml, plus one negative test per validator rule --
mirroring feynlag-models' own tests/test_repo.py practice."""

import yaml
import pytest

from feynlag_anomalies.loader import AnomalyValidationError, load
from feynlag_anomalies.registry import anomaly_dirs
from feynlag_anomalies.schema import Anomaly


def _write(tmp_path, name, data):
    d = tmp_path / name
    d.mkdir(exist_ok=True)
    (d / "anomaly.yaml").write_text(yaml.safe_dump(data))
    return d


@pytest.mark.parametrize("anomaly_dir", anomaly_dirs(), ids=lambda p: p.name)
def test_every_anomaly_validates(anomaly_dir):
    anomaly = load(anomaly_dir)
    assert anomaly.id == anomaly_dir.name


def test_id_must_match_directory_name(tmp_path, valid_anomaly_dict):
    valid_anomaly_dict["id"] = "not_the_dirname"
    d = _write(tmp_path, "neutrino_mass", valid_anomaly_dict)
    with pytest.raises(AnomalyValidationError):
        load(d)


def test_bad_status_literal_rejected(valid_anomaly_dict):
    valid_anomaly_dict["status"] = "not_a_real_status"
    with pytest.raises(Exception):
        Anomaly.model_validate(valid_anomaly_dict)


def test_bad_sm_failure_type_rejected(valid_anomaly_dict):
    valid_anomaly_dict["sm_failure_type"] = "not_a_real_type"
    with pytest.raises(Exception):
        Anomaly.model_validate(valid_anomaly_dict)


def test_bad_maturity_rejected(valid_anomaly_dict):
    valid_anomaly_dict["maturity"] = "Z9"
    with pytest.raises(Exception):
        Anomaly.model_validate(valid_anomaly_dict)


def test_tensions_with_other_data_defaults_to_empty_list_not_absent(valid_anomaly_dict):
    del valid_anomaly_dict["tensions_with_other_data"]
    anomaly = Anomaly.model_validate(valid_anomaly_dict)
    assert anomaly.tensions_with_other_data == []


def test_unknown_model_id_rejected(tmp_path, valid_anomaly_dict):
    valid_anomaly_dict["candidate_models"] = [{"model_id": "does_not_exist_anywhere"}]
    d = _write(tmp_path, "neutrino_mass", valid_anomaly_dict)
    with pytest.raises(AnomalyValidationError):
        load(d)


def test_low_maturity_model_rejected_for_fit_level_anomaly(tmp_path, valid_anomaly_dict, monkeypatch):
    import feynlag_models.registry as fm_registry

    monkeypatch.setattr(fm_registry, "metadata", lambda model_id: {"maturity_level": 0})
    valid_anomaly_dict["maturity"] = "A3"
    valid_anomaly_dict["candidate_models"] = [{"model_id": "seesaw_type1"}]
    d = _write(tmp_path, "neutrino_mass", valid_anomaly_dict)
    with pytest.raises(AnomalyValidationError):
        load(d)


def test_todo_verify_sentinel_accepted_for_numeric_fields(valid_anomaly_dict):
    valid_anomaly_dict["sm_prediction"]["value"] = "TODO_VERIFY"
    anomaly = Anomaly.model_validate(valid_anomaly_dict)
    assert anomaly.sm_prediction.value == "TODO_VERIFY"


def test_candidate_model_needs_id_or_request():
    from feynlag_anomalies.schema import CandidateModel

    with pytest.raises(Exception):
        CandidateModel()


def _constraint(source):
    return {"name": "toy bound", "quantity": "sum_m_nu", "upper_limit": 0.1,
            "confidence_level": 0.95, "units": "eV", "source": source}


def test_constraint_with_known_source_accepted(tmp_path, valid_anomaly_dict):
    valid_anomaly_dict["constraints"] = [_constraint(valid_anomaly_dict["sources"][0]["identifier"])]
    d = _write(tmp_path, "neutrino_mass", valid_anomaly_dict)
    assert load(d).constraints[0].upper_limit == 0.1


def test_constraint_with_unknown_source_rejected(tmp_path, valid_anomaly_dict):
    valid_anomaly_dict["constraints"] = [_constraint("arXiv:0000.00000 (not in sources)")]
    d = _write(tmp_path, "neutrino_mass", valid_anomaly_dict)
    with pytest.raises(AnomalyValidationError):
        load(d)


def test_bad_constraint_quantity_rejected(valid_anomaly_dict):
    bad = _constraint(valid_anomaly_dict["sources"][0]["identifier"]) | {"quantity": "mass_of_everything"}
    valid_anomaly_dict["constraints"] = [bad]
    with pytest.raises(Exception):
        Anomaly.model_validate(valid_anomaly_dict)
