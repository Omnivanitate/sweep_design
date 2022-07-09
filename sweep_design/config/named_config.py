from ..named_signals.defaults.methods import extract_input


class NamedConfig:
    """Configuration for named_signals.

    - - -

    **NAMING_BY_ASSIGNMENT_CREATE**: `bool`
    > If `True` then my_relation = `NamedRelation`(...) and `str`(my_relation) ==
    'my_relation', otherwise false then my_relation = `NamedRelation`(...) and
    `str`(my_relation) == 'R_1' using
    `sweep_design.named_signals.header_signals.defaults.names.make_default_relation_name`
    with parameter 1.

    > In both situations, if name param name is specified, then
    my_relation = `NamedRelation`(..., name='MyName') and `str`(my_relation) == 'MyName'.

    - - -

    **NAMING_BY_ASSIGNMENT_MATH_OPERATION**: `bool`
    > This veriable is similar to  **NAMING_BY_ASSIGNMENT**, but you can't send
    name to a math operation.

    > If **NAMING_BY_ASSIGNMENT_MATH_OPERATION** is `False` then
    > my_relation = `NamedRelation`(..., name = 'MyName')
    > sum_relation = my_relation + my_relation
    > `str`(sum_relation) == 'MyName + MyName'
    using default method
    `sweep_design.named_signals.header_signals.defaults.names.make_default_names_operations`

    > otherwise if `True` then result was `str`(sum_relation) == 'sum_relation'

    - - -

    **NAMING_BY_ASSIGNMENT_OTHER_OPERATION**: `bool`
    > This variable is similar above for other operations.

    - - -

    **extract_input**
    > The method to convert input data to tuple of `numpy.ndarray`
    **x** and **y**.
    > Default methods is from
    `sweep_design.named_signals.defaults.methods.extract_input`

    > It's a simple method, but you can override them yourself.

    > **input**:
    >> **x**: `Any`
       **y**: `Any`

    > **output**:
    >> `Typle`[
        **x**: `numpy.ndarray`,
        **y**: `numpy.ndarray`
        ]

    The above methods can be overridden with your own here, or you can import the
    class `NamedConfig` somewhere and override it there.
     (They must be written according to the rules corresponding to
     the input and output parameters)

    """

    NAMING_BY_ASSIGNMENT_CREATE = True
    NAMING_BY_ASSIGNMENT_MATH_OPERATION = False
    NAMING_BY_ASSIGNMENT_OTHER_OPERATION = False

    extract_input = staticmethod(extract_input)
