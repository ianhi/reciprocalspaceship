import pytest
import numpy as np
import pandas as pd
import reciprocalspaceship as rs
from pandas.tests.extension import base

array = {
    "HKL": rs.dtypes.hklindex.HKLIndexArray,
    "MTZInt": rs.dtypes.mtzint.MTZIntArray,
    "Batch": rs.dtypes.batch.BatchArray,
    "M/ISYM": rs.dtypes.m_isym.M_IsymArray
}

@pytest.fixture(
    params=[
        rs.HKLIndexDtype,
        rs.MTZIntDtype,
        rs.BatchDtype,
        rs.M_IsymDtype
    ]
)
def dtype(request):
    return request.param()

@pytest.fixture
def data(dtype):
    return array[dtype.name]._from_sequence(np.arange(0, 100), dtype=dtype)

@pytest.fixture
def data_for_twos(dtype):
    return array[dtype.name]._from_sequence(np.ones(100) * 2, dtype=dtype)

@pytest.fixture
def data_missing(dtype):
    return array[dtype.name]._from_sequence([np.nan, 1.], dtype=dtype)

@pytest.fixture
def data_for_sorting(dtype):
    return array[dtype.name]._from_sequence([1., 2., 0.], dtype=dtype)

@pytest.fixture
def data_missing_for_sorting(dtype):
    return array[dtype.name]._from_sequence([1., np.nan, 0.], dtype=dtype)

@pytest.fixture(params=['data', 'data_missing'])
def all_data(request, data, data_missing):
    """Parametrized fixture giving 'data' and 'data_missing'"""
    if request.param == 'data':
        return data
    elif request.param == 'data_missing':
        return data_missing
    
@pytest.fixture
def data_for_grouping(dtype):
    b = 1
    a = 0
    c = 2
    na = np.nan
    return array[dtype.name]._from_sequence([b, b, na, na, a, a, b, c], dtype=dtype)

class TestCasting(base.BaseCastingTests):
    pass

class TestConstructors(base.BaseConstructorsTests):
    pass

class TestDtype(base.BaseDtypeTests):
    pass

class TestGetitem(base.BaseGetitemTests):
    pass

class TestGroupby(base.BaseGroupbyTests):
    pass

class TestInterface(base.BaseInterfaceTests):
    pass

class TestIO(base.BaseParsingTests):
    pass

class TestMethods(base.BaseMethodsTests):

    @pytest.mark.parametrize("dropna", [True, False])
    def test_value_counts(self, all_data, dropna):
        all_data = all_data[:10]
        if dropna:
            other = all_data[~all_data.isna()]
        else:
            other = all_data

        result = rs.DataSeries(all_data).value_counts(dropna=dropna).sort_index()
        expected = rs.DataSeries(other).value_counts(dropna=dropna).sort_index()

        self.assert_series_equal(result, expected)

    def test_value_counts_with_normalize(self, data):
        # GH 33172
        data = data[:10].unique()
        values = np.array(data[~data.isna()])

        result = (
            rs.DataSeries(data, dtype=data.dtype).value_counts(normalize=True).sort_index()
        )

        expected = rs.DataSeries([1 / len(values)] * len(values), index=result.index)
        self.assert_series_equal(result, expected)

class TestComparisonOps(base.BaseComparisonOpsTests):
    # Copied from pandas/tests/extension/test_integer.py
    
    def _check_op(self, s, op, other, op_name, exc=NotImplementedError):
        if exc is None:
            result = op(s, other)
            # Override to do the astype to boolean
            expected = s.combine(other, op).astype("boolean")
            self.assert_series_equal(result, expected)
        else:
            with pytest.raises(exc):
                op(s, other)

    def check_opname(self, s, op_name, other, exc=None):
        super().check_opname(s, op_name, other, exc=None)

    def _compare_other(self, s, data, op_name, other):
        self.check_opname(s, op_name, other)

class TestMissing(base.BaseMissingTests):
    pass

class TestBooleanReduce(base.BaseBooleanReduceTests):
    pass

class TestNumericReduce(base.BaseNumericReduceTests):
    pass

class TestPrinting(base.BasePrintingTests):
    pass

class TestReshaping(base.BaseReshapingTests):
    pass

class TestSetitem(base.BaseSetitemTests):
    pass
