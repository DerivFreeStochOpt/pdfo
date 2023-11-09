# -*- coding: utf-8 -*-
import warnings
from inspect import stack

import numpy as np


def cobyla(fun, x0, args=(), bounds=None, constraints=(), options=None):
    r"""Constrained Optimization BY Linear Approximations.

    .. deprecated:: 1.3
        Calling the COBYLA solver via the `cobyla` function is deprecated.
        The COBYLA solver remains available in PDFO. Call the `pdfo` function
        with the argument ``method='cobyla'`` to use it.

    Parameters
    ----------
    fun : callable
        Objective function to be minimized.

            ``fun(x, *args) -> float``

        where ``x`` is an array with shape (n,) and `args` is a tuple.
    x0 : array_like, shape (n,)
        Initial guess.
    args : tuple, optional
        Extra arguments of the objective function. For example,

            ``cobyla(fun, x0, args, ...)``

        is equivalent to

            ``cobyla(lambda x: fun(x, *args), x0, ...)``

    bounds : {`scipy.optimize.Bounds`, array_like, shape (n, 2)}, optional
        Bound constraints of the problem. It can be one of the cases below.

        #. An instance of `scipy.optimize.Bounds`.
        #. An array with shape (n, 2). The bound constraints for ``x[i]`` are
           ``bounds[i, 0] <= x[i] <= bounds[i, 1]``. Set ``bounds[i, 0]`` to
           :math:`-\infty` if there is no lower bound, and set ``bounds[i, 1]``
           to :math:`\infty` if there is no upper bound.

    constraints : {dict, `scipy.optimize.LinearConstraint`, `scipy.optimize.NonlinearConstraint`, list}, optional
        Constraints of the problem. It can be one of the cases below.

        #. A dictionary with fields:

            type : {``'eq'``, ``'ineq'``}
                Whether the constraint is ``fun(x) = 0`` or ``fun(x) >= 0``.
            fun : callable
                Constraint function.

        #. An instance of `scipy.optimize.LinearConstraint`.
        #. An instance of `scipy.optimize.NonlinearConstraint`.
        #. A list, each of whose elements are described in 1, 2, and 3.

    options : dict, optional
        The options passed to the solver. Accepted options are:

            rhobeg: float, optional
                Initial value of the trust region radius, which should be a
                positive scalar. Typically, ``options['rhobeg']`` should be in
                the order of one tenth of the greatest expected change to a
                variable. By default, it is ``1`` if the problem is not scaled,
                and ``0.5`` if the problem is scaled.
            rhoend: float, optional
                Final value of the trust region radius, which should be a
                positive scalar. ``options['rhoend']`` should indicate the
                accuracy required in the final values of the variables.
                Moreover, ``options['rhoend']`` should be no more than
                ``options['rhobeg']`` and is by default ``1e-6``.
            maxfev: int, optional
                Upper bound of the number of calls of the objective function
                `fun`. Its value must be not less than ``options['npt'] + 1``.
                By default, it is ``500 * n``.
            ftarget: float, optional
                Target value of the objective function. If a feasible iterate
                achieves an objective function value lower or equal to
                ```options['ftarget']``, the algorithm stops immediately. By
                default, it is :math:`-\infty`.
            scale: bool, optional
                Whether to scale the problem according to the bound constraints.
                By default, it is ``False``. If the problem is to be scaled,
                then ``rhobeg`` and ``rhoend`` will be used as the initial and
                final trust region radii for the scaled problem.
            quiet: bool, optional
                Whether the interface is quiet. If it is set to ``True``, the
                output message will not be printed. This flag does not interfere
                with the warning and error printing.
            classical: bool, optional
                Whether to call the classical Powell code or not. It is not
                encouraged in production. By default, it is ``False``.
            eliminate_lin_eq: bool, optional
                Whether the linear equality constraints should be eliminated.
                By default, it is ``True``.
            debug: bool, optional
                Debugging flag. It is not encouraged in production. By default,
                it is ``False``.
            chkfunval: bool, optional
                Flag used when debugging. If both ``options['debug']`` and
                ``options['chkfunval']`` are ``True``, an extra
                function/constraint evaluation would be performed to check
                whether the returned values of objective function and constraint
                match the returned ``x``. By default, it is ``False``.

    Returns
    -------
    res : `scipy.optimize.OptimizeResult`
        Result of the optimization procedure, with the following fields:

            message : str
                Description of the cause of the termination.
            success : bool
                Whether the optimization procedure terminated successfully.
            status : int
                Termination status of the optimization procedure.
            fun : float
                Objective function value at the solution point.
            x : `numpy.ndarray`, shape (n,)
                Solution point.
            nfev : int
                Number of function evaluations.
            fun_history : `numpy.ndarray`, shape (nfev,)
                History of the objective function values.
            method : str
                Name of the Powell method used.

        For constrained problems, the following fields are also returned:

            maxcv : float
                Maximum constraint violation at the solution point.
            maxcv_history : `numpy.ndarray`, shape (nfev,)
                History of the maximum constraint violation.

        For linearly and nonlinearly constrained problems, the following field
        is also returned:

            constraints : {`numpy.ndarray`, list}
                The values of the constraints at the solution point. If a single
                constraint is passed, i.e., if the `constraints` argument is
                either a dict, a `scipy.optimize.LinearConstraint`, or a
                `scipy.optimize.NonlinearConstraint`, then the returned value is
                a `numpy.ndarray`. Otherwise, it is a list of `numpy.ndarray`,
                each of whose element corresponds to a constraint.

        If the optimization procedure terminated because the constraints are
        infeasible (i.e., when the exit status is -4), the following fields may
        also be returned:

            infeasible_bounds : `numpy.ndarray`
                Indices of the bounds that are infeasible.
            infeasible_linear_constraints : `numpy.ndarray`
                Indices of the linear constraints that are infeasible.
            infeasible_nonlinear_constraints : `numpy.ndarray`
                Indices of the nonlinear constraints that are infeasible.

        If warnings are raised during the optimization procedure, the following
        field is also returned:

            warnings : list
                A list of the warnings raised during the optimization procedure.

    References
    ----------
    .. [1] M. J. D. Powell. A direct search optimization method that models the
       objective and constraint functions by linear interpolation. In S. Gomez
       and J. P. Hennart, editors, *Advances in Optimization and Numerical
       Analysis*, pages 51–67, Dordrecht, The Netherlands, 1994. Springer.
    .. [2] T. M. Ragonneau and Z. Zhang. PDFO: a cross-platform package for
       Powell's derivative-free optimization solvers.
       arXiv:`2302.13246 [math.OC] <https://arxiv.org/abs/2302.13246>`_, 2023.

    See also
    --------
    pdfo : Powell's Derivative-Free Optimization solvers.
    uobyqa : Unconstrained Optimization BY Quadratic Approximation.
    newuoa : NEW Unconstrained Optimization Algorithm.
    bobyqa : Bounded Optimization BY Quadratic Approximations.
    lincoa : LINearly Constrained Optimization Algorithm.

    Examples
    --------
    The following example shows how to solve a simple optimization problem using
    `cobyla`. In practice, the  problem considered below should be solved with a
    derivative-based method as it is a smooth problem for which the derivatives
    are known. We solve it here using `cobyla` only as an illustration.

    We consider the 2-dimensional problem

    .. math::

        \min_{x, y \in \R} \quad x^2 + y^2 \quad \text{s.t.} \quad \left\{
        \begin{array}{l}
            0 \le x \le 2,\\
            1 / 2 \le y \le 3,\\
            0 \le x + y \le 1,\\
            x^2 - y \le 0.
        \end{array} \right.

    We solve this problem using `cobyla` starting from the initial guess
    :math:`(x_0, y_0) = (0, 1)` with at most 200 function evaluations.

    .. testsetup::

        import numpy as np
        np.set_printoptions(precision=1, suppress=True)

    >>> import numpy as np
    >>> from pdfo import pdfo
    >>> from scipy.optimize import Bounds, LinearConstraint, NonlinearConstraint
    >>>
    >>> # Build the constraints.
    >>> bounds = Bounds([0, 0.5], [2, 3])
    >>> linear_constraints = LinearConstraint([1, 1], 0, 1)
    >>> nonlinear_constraints = NonlinearConstraint(lambda x: x[0]**2 - x[1], -np.inf, 0)
    >>> constraints = [linear_constraints, nonlinear_constraints]
    >>>
    >>> # Solve the problem.
    >>> options = {'maxfev': 200}
    >>> res = pdfo(lambda x: x[0]**2 + x[1]**2, [0, 1], bounds=bounds, constraints=constraints, options=options)
    >>> res.x
    array([0. , 0.5])
    """
    try:
        from .gethuge import gethuge
    except ImportError:
        from ._common import import_error_so

        # If gethuge cannot be imported, the execution should stop because the package is most likely not built.
        import_error_so('gethuge')

    from ._common import prepdfo, _augmented_linear_constraint, postpdfo
    from ._settings import ExitStatus

    # This method is deprecated. Warn the user.
    warnings.warn('The `cobyla` function is deprecated. Use the `pdfo` function with the argument `method=\'cobyla\'` to use the COBYLA method.', DeprecationWarning, 2)

    fun_name = stack()[0][3]  # name of the current function
    if len(stack()) >= 3:
        invoker = stack()[1][3].lower()
    else:
        invoker = ''

    # A cell that records all the warnings.
    # Why do we record the warning message in output['warnings'] instead of prob_info['warnings']? Because, if cobyla is
    # called by pdfo, then prob_info will not be passed to postpdfo, and hence the warning message will be lost. To the
    # contrary, output will be passed to postpdfo anyway.
    output = dict()
    output['warnings'] = []

    # Preprocess the inputs.
    fun_c, x0_c, bounds_c, constraints_c, options_c, _, prob_info = \
        prepdfo(fun, x0, args, bounds=bounds, constraints=constraints, options=options)

    if invoker != 'pdfo' and prob_info['infeasible']:
        # The problem turned out infeasible during prepdfo.
        exitflag = ExitStatus.INFEASIBLE_ERROR.value
        nf = 1
        x = x0_c
        fx = fun_c(x)
        fhist = np.array([fx], dtype=np.float64)
        constrviolation = prob_info['constrv_x0']
        chist = np.array([constrviolation], dtype=np.float64)
        output['constr_value'] = prob_info['nlc_x0']
    elif invoker != 'pdfo' and prob_info['nofreex']:
        # x was fixed by the bound constraints during prepdfo
        exitflag = ExitStatus.FIXED_SUCCESS.value
        nf = 1
        x = prob_info['fixedx_value']
        fx = fun_c(x)
        fhist = np.array([fx], dtype=np.float64)
        constrviolation = prob_info['constrv_fixedx']
        chist = np.array([constrviolation], dtype=np.float64)
        output['constr_value'] = prob_info['nlc_fixedx']
    elif invoker != 'pdfo' and prob_info['feasibility_problem'] and \
            prob_info['refined_type'] != 'nonlinearly-constrained':
        # We could set fx=[], funcCount=0, and fhist=[] since no function evaluation occurred. But then we will have to
        # modify the validation of fx, funcCount, and fhist in postpdfo. To avoid such a modification, we set fx,
        # funcCount, and fhist as below and then revise them in postpdfo.
        nf = 1
        x = x0_c  # prepdfo has tried to set x0 to a feasible point (but may have failed)
        fx = fun_c(x)
        fhist = np.array([fx], dtype=np.float64)
        constrviolation = prob_info['constrv_x0']
        chist = np.array([constrviolation], dtype=np.float64)
        output['constr_value'] = np.asarray([], dtype=np.float64)
        if constrviolation < np.finfo(np.float64).eps:
            # Did prepdfo find a feasible point?
            exitflag = ExitStatus.FEASIBILITY_SUCCESS.value
        else:
            exitflag = ExitStatus.INFEASIBILITY_ERROR.value
    else:
        # The problem turns out 'normal' during prepdfo include all the constraints into one single nonlinear
        # constraint.
        n = x0_c.size
        a_aug, b_aug = _augmented_linear_constraint(n, bounds_c, constraints_c)

        # The constraint function received by COBYLA can return an array: in fact, the Fortran code interpret this
        # function as a subroutine from v1.0.
        def ctr(x_aug):
            c = np.array([], dtype=np.float64)

            if b_aug.size > 0:
                cx = np.dot(a_aug, x_aug) - b_aug
                c = np.concatenate((c, cx))

            if constraints_c['nonlinear'] is not None:
                cx = constraints_c['nonlinear']['fun'](x_aug)
                c = np.concatenate((c, cx))

            return -c

        conval_x0 = ctr(x0_c)
        m = conval_x0.size

        # Extract the options and parameters.
        maxfev = options_c['maxfev']
        rhobeg = options_c['rhobeg']
        rhoend = options_c['rhoend']
        ftarget = options_c['ftarget']

        # The largest integer in the fortran functions; the factor 0.99 provides a buffer.
        max_int = np.floor(0.99 * gethuge('integer'))

        # The smallest nw, i.e., the nw with npt = n + 2. If it is larger than a threshold (system dependent), the
        # problem is too large to be executed on the system.
        min_nw = n * (3 * n + 2 * m + 11) + 4 * m + 6
        if min_nw >= max_int:
            executor = invoker.lower() if invoker == 'pdfo' else fun_name
            # nw would suffer from overflow in the Fortran code, exit immediately.
            raise SystemError('{}: problem too large for {}. Try other '
                              'solvers.'.format(executor, fun_name))
        if maxfev > max_int:
            maxfev = max_int
            w_message = '{}: maxfev exceeds the upper limit of Fortran integer; it is set to ' \
                        '{}'.format(fun_name, maxfev)
            warnings.warn(w_message, Warning, 2)
            output['warnings'].append(w_message)

        # Call the Fortran code.
        try:
            if options_c['classical']:
                from . import fcobyla_classical as fcobyla
            else:
                from . import fcobyla
        except ImportError:
            from ._common import import_error_so
            import_error_so()

        # m should be precised not to raise any error if there is no linear constraints.
        x, fx, exitflag, fhist, chist, constrviolation, conval = \
            fcobyla.mcobyla(x0_c, rhobeg, rhoend, 0, maxfev, ftarget, conval_x0, fun_c, lambda m, x: ctr(x))
        nf = int(fcobyla.fcobyla.nf)

        if m > 0:
            output['constr_value'] = -conval[b_aug.size:]

    # Postprocess the result.
    return postpdfo(x, fx, exitflag, output, fun_name, nf, fhist, options_c, prob_info, constrviolation, chist)
